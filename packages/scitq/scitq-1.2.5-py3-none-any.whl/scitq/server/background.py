from sqlalchemy import select, and_, func, distinct
from sqlalchemy.orm import Session, aliased
from sqlalchemy.exc import NoResultFound
import logging as log
import os
from subprocess import run, Popen, PIPE, TimeoutExpired
import json as json_module
from datetime import datetime
from argparse import Namespace
import math
from time import sleep, time
from signal import SIGKILL
import re

from .model import Worker, Task, Execution, Job, Recruiter, Requirement, Signal, worker_delete, find_flavor, Flavor
from .config import WORKER_IDLE_CALLBACK, SERVER_CRASH_WORKER_RECOVERY, WORKER_OFFLINE_DELAY, WORKER_CREATE_CONCURRENCY,\
    WORKER_CREATE, WORKER_CREATE_RETRY, MAIN_THREAD_SLEEP, IS_SQLITE, SCITQ_SHORTNAME, TERMINATE_TIMEOUT, KILL_TIMEOUT,\
    JOB_MAX_LIFETIME
from .db import db
from ..util import PropagatingThread, to_obj, validate_protofilter
from ..constants import PROTOFILTER_SEPARATOR, PROTOFILTER_SYNTAX

protofilter_syntax=re.compile(PROTOFILTER_SYNTAX)

def get_nodename(session):
    worker_names = list(map(lambda x: x[0], 
        session.execute(select(Worker.name))))
    log.warning(f'Worker names: {worker_names}')
    i=1
    while f'{SCITQ_SHORTNAME}-node{i}' in worker_names:
        i+=1
    return f'{SCITQ_SHORTNAME}-node{i}'


def create_worker_object(concurrency, flavor, region, provider, batch, prefetch, db_session):
    """Create a worker object in db - this must be called linearly not in async way
    """
    hostname = get_nodename(db_session)
    log.info(f'Creating a new worker {hostname}: concurrency:{concurrency}, \
flavor:{flavor}, region:{region}, provider:{provider}, prefetch:{prefetch}')
    w = Worker(name=hostname, hostname=hostname, concurrency=concurrency, status='offline', 
            batch=batch, permanent=False, prefetch=prefetch, 
            flavor=flavor,region=region, provider=provider)
    db_session.add(w)
    db_session.commit()
    return w
    

def background(app):
    # while some tasks are pending without executions:
    #   look for a running worker:
    #      create a pending execution of this task for this worker


    with app.app_context():
        session = Session(db.engine)
    worker_process_queue = {}
    other_process_queue = []
    log.info('Starting thread for {}'.format(os.getpid()))
    ansible_workers = list(session.query(Worker).filter(and_(
                    Worker.status=='running',
                    ~Worker.permanent)).with_entities(
                        Worker.hostname))
    if ansible_workers:
        log.warning(f'Making sure workers {",".join([w.hostname for w in ansible_workers])} has access to server')
        process = PropagatingThread(
                    target=run,
                    args = (SERVER_CRASH_WORKER_RECOVERY,),
                    kwargs= {'shell': True, 'check':True}
                )
        other_process_queue.append(('Worker access task',process))
        process.start()

    while True:
        log.warning('Starting main loop')
        pending_job = None
        try:

            # ########    ###     ######  ##    ##    ########  ########   #######   ######  ########  ######   ######  #### ##    ##  ######   
            #    ##      ## ##   ##    ## ##   ##     ##     ## ##     ## ##     ## ##    ## ##       ##    ## ##    ##  ##  ###   ## ##    ##  
            #    ##     ##   ##  ##       ##  ##      ##     ## ##     ## ##     ## ##       ##       ##       ##        ##  ####  ## ##        
            #    ##    ##     ##  ######  #####       ########  ########  ##     ## ##       ######    ######   ######   ##  ## ## ## ##   #### 
            #    ##    #########       ## ##  ##      ##        ##   ##   ##     ## ##       ##             ##       ##  ##  ##  #### ##    ##  
            #    ##    ##     ## ##    ## ##   ##     ##        ##    ##  ##     ## ##    ## ##       ##    ## ##    ##  ##  ##   ### ##    ##  
            #    ##    ##     ##  ######  ##    ##    ##        ##     ##  #######   ######  ########  ######   ######  #### ##    ##  ######  


            task_list = list(session.query(Task).filter(
                    Task.status=='pending').with_entities(Task.task_id, Task.batch))
            if task_list:
                task_attributions = False
                worker_list = list(session.query(Worker).filter(
                            Worker.status=='running').with_entities(
                            Worker.worker_id,Worker.batch,Worker.concurrency,Worker.prefetch,Worker.task_properties))
                execution_per_worker_list = session.query(Execution.worker_id,Task.batch,Execution.status).\
                                                join(Execution.task).filter(and_(
                                                Execution.worker_id.in_(list([w.worker_id for w in worker_list])),
                                                Execution.status.in_(['running','pending','accepted']))
                                            )
                worker_properties = {worker.worker_id: json_module.loads(worker.task_properties) for worker in worker_list}
                execution_per_worker = {}
                for worker_id,batch,status in execution_per_worker_list:
                    if worker_id not in execution_per_worker:
                        execution_per_worker[worker_id] = 0
                    weight,_ = worker_properties[worker_id].get(batch, (1,0) )
                    if status=='running':
                        # only running task have a relative weight
                        execution_per_worker[worker_id] += weight
                    else:
                        execution_per_worker[worker_id] += 1
                
                for task in task_list:
                    for worker in worker_list:
                        if worker.batch != task.batch:
                            continue
                        if execution_per_worker.get(worker.worker_id,0)<(worker.concurrency+worker.prefetch):
                            session.add(Execution(worker_id=worker.worker_id,
                                task_id=task.task_id))
                            session.query(Task).filter(Task.task_id==task.task_id).update(
                                {'status':'assigned'}
                            )
                            execution_per_worker[worker.worker_id] = execution_per_worker.get(worker.worker_id,0)+1
                            log.info(f'Execution of task {task.task_id} proposed to worker {worker.worker_id}')
                            task_attributions = True
                            break
                if task_attributions:
                    session.commit()
            now = datetime.utcnow()

            # managing timeouts
            if IS_SQLITE:
                status_change_time = '(unixepoch(:now)-unixepoch(status_date))'
            else:
                # initially this was done with current_timestamp
                # but then SQLAlchemy with PostgreSQL issues the same answer for minutes (when it's supposed to change each second)
                # anyway, it works this way
                status_change_time = 'extract(epoch from :now - status_date)'
            some_timeouts = False
            log.warning(f'Looking for task timouts...')
            for item in session.execute(f'''SELECT execution.execution_id,execution.worker_id,execution.task_id 
                        FROM task 
                        JOIN execution ON execution.task_id=task.task_id AND execution.latest
                        WHERE 
                            (task.status='accepted' AND download_timeout IS NOT NULL AND {status_change_time}>download_timeout)
                            OR
                            (task.status='running' AND run_timeout IS NOT NULL AND {status_change_time}>run_timeout)''',params={'now':now}):
                log.warning(f'Task {item.task_id} has reached a timeout, sending kill signal.')
                session.add(Signal(execution_id=item.execution_id, worker_id=item.worker_id, signal=SIGKILL))
                some_timeouts = True
            if some_timeouts:
                session.commit()
            


            log.warning('Looking for offline/online workers')
            session.expire_all()
            for worker in session.query(Worker).filter(Worker.status.in_(['offline','running'])):
                change = False
                log.warning(f'Assessing worker {worker.name}')
                if worker.last_contact_date is None or (
                            now - worker.last_contact_date
                        ).total_seconds() > WORKER_OFFLINE_DELAY:
                    log.warning(f'... late: {worker.last_contact_date}')
                    if worker.status=='running':
                        log.warning(f'Worker {worker.name} ({worker.worker_id}) lost, marked as offline')
                        worker.status = 'offline'
                        change = True
                else:
                    log.warning('... good')
                    if worker.status=='offline':
                        log.warning(f'Worker {worker.name} ({worker.worker_id}) recovered, marked as running')
                        worker.status = 'running'
                        change = True
                if change:
                    session.commit()
            

            #        ##  #######  ########     ########  ########   #######   ######  ########  ######   ######  #### ##    ##  ######   
            #        ## ##     ## ##     ##    ##     ## ##     ## ##     ## ##    ## ##       ##    ## ##    ##  ##  ###   ## ##    ##  
            #        ## ##     ## ##     ##    ##     ## ##     ## ##     ## ##       ##       ##       ##        ##  ####  ## ##        
            #        ## ##     ## ########     ########  ########  ##     ## ##       ######    ######   ######   ##  ## ## ## ##   #### 
            #  ##    ## ##     ## ##     ##    ##        ##   ##   ##     ## ##       ##             ##       ##  ##  ##  #### ##    ##  
            #  ##    ## ##     ## ##     ##    ##        ##    ##  ##     ## ##    ## ##       ##    ## ##    ##  ##  ##   ### ##    ##  
            #   ######   #######  ########     ##        ##     ##  #######   ######  ########  ######   ######  #### ##    ##  ######     

            change = False
            for job in list(session.query(Job).filter(Job.status == 'pending')):
                pending_job = job

                if job.action == 'worker_destroy':
                    change=True
                    if ('destroy',job.target) in worker_process_queue:
                        log.warning(f'A destruction job is already running for worker {job.target}, failing this one')
                        job.status='failed'
                        job.log='Another destruction job is already running, this job failed as a doublon.'
                        continue
                    if ('create',job.target) in worker_process_queue:
                        worker,worker_create_process,job_id,start_time = worker_process_queue[('create',job.target)]
                        if worker_create_process.poll() is None:
                            worker_create_process.terminate()
                            try:
                                worker_create_process.wait(timeout=TERMINATE_TIMEOUT)
                                log.warning(f'Worker {job.target} creation process has been terminated')
                            except TimeoutExpired:
                                worker_create_process.kill()
                                try:
                                    worker_create_process.wait(timeout=KILL_TIMEOUT)
                                    log.warning(f'Worker {job.target} creation process has been killed')
                                except TimeoutExpired:
                                    log.exception(f'Could not kill worker {job.target} creation process, giving up for this round!')
                                    continue
                            
                            del(worker_process_queue[('create',job.target)])
                            session.query(Job).get(job_id).status='failed'
                    worker = Namespace(**job.args)
                    real_worker = session.query(Worker).get(worker.worker_id)
                    if real_worker.ansible_active:
                        if len(worker_process_queue)<WORKER_CREATE_CONCURRENCY:
                            worker_destroy_command = WORKER_IDLE_CALLBACK.format(hostname=job.target)
                            log.warning(f'Launching destroy process for {job.target}, command is "{worker_destroy_command}"')
                            worker_delete_process = Popen(
                                    worker_destroy_command,
                                    stdout = PIPE,
                                    stderr = PIPE,
                                    shell = True,
                                    encoding = 'utf-8'
                                )
                            job.status='running'
                            worker_process_queue[('destroy',job.target)]=(worker, worker_delete_process, job.job_id, time())
                            log.warning(f'Worker {job.target} destruction process has been launched')
                    else:
                        #TODO: this should be a very rare event, we should do extra tests here
                        log.warning(f'Deleting worker {worker.name} ({worker.worker_id})')
                        if real_worker is not None:
                            change = True
                            worker_delete(real_worker, session, is_destroyed=True, commit=False)
                            #session.delete(real_worker)
                            job.log='Deleting unmanaged worker.'
                            job.status='succeeded'            
                
                if job.action == 'worker_create':
                    change = True
                    worker = create_worker_object(db_session=session,
                        **job.args)
                    
                    auto_deploy = False
                    if worker.provider=='auto' or worker.region=='auto' or worker.flavor.startswith('auto'):
                        try:
                            log.warning(' -> Auto deploy detected')
                            auto_deploy = True
                            provider = None if worker.provider=='auto' else worker.provider
                            region = None if worker.region=='auto' else worker.region
                            protofilters=''
                            if worker.flavor.startswith('auto'):
                                validate_protofilter(worker.flavor)
                                flavor=None
                                if PROTOFILTER_SEPARATOR in worker.flavor:
                                    protofilters = PROTOFILTER_SEPARATOR.join(
                                            worker.flavor.split(PROTOFILTER_SEPARATOR)[1:])
                            else:
                                flavor=worker.flavor
                            flavor_list=list(map(to_obj,find_flavor(session, provider=provider, region=region, 
                                                                flavor=flavor, protofilters=protofilters, limit=None)))
                            while flavor_list:
                                current_flavor=flavor_list[0]
                                if current_flavor.available is not None and current_flavor.available<=0:
                                    flavor_list.pop(0)
                                    continue
                                else:
                                    worker.flavor=current_flavor.name
                                    worker.region=current_flavor.region
                                    worker.provider=current_flavor.provider
                                    break
                            else:
                                raise RuntimeError(f'Could not find a flavor satisfying provider={worker.provider},region={worker.region},flavor={worker.flavor}')
                        except RuntimeError as re:
                            job.status='failed'
                            job.log=re.args[0]

                    if job.status!='failed':
                        job.action = 'worker_deploy'
                        job.target = worker.name
                        job.args = dict(job.args)
                        job.args['worker_id'] = worker.worker_id
                        if auto_deploy:
                            job.args['flavor'] = worker.flavor
                            job.args['provider'] = worker.provider
                            job.args['region'] = worker.region
                        job.retry = WORKER_CREATE_RETRY
                        job.status = 'pending'
                
                if job.action == 'worker_deploy':
                    if ('create',job.target) not in worker_process_queue and len(
                                worker_process_queue)<WORKER_CREATE_CONCURRENCY:
                        if ('destroy',job.target) in worker_process_queue:
                            log.warning(f'Trying to recreate worker {job.target} after destruction too soon, waiting a little bit...')
                            continue
                        change = True
                        log.warning(f'Launching creation process for worker {job.target}.')
                        worker = Namespace(**job.args)
                        try:
                            flavor = session.query(Flavor).filter(Flavor.provider==worker.provider, 
                                                                Flavor.name==worker.flavor).one()
                        except NoResultFound:
                            log_message = f'Could not find flavor {worker.flavor} in {worker.provider}: worker {job.target} deploy failed.'
                            log.exception(log_message)
                            job.status='failed'
                            job.log=log_message
                            session.query(Worker).filter(Worker.worker_id==worker.worker_id).update(
                                {'status':'failed'}
                            )
                            continue
                        log.exception(f'Launching command is "'+WORKER_CREATE.format(
                            hostname=job.target,
                            concurrency=worker.concurrency,
                            flavor=worker.flavor,
                            region=worker.region,
                            provider=worker.provider,
                            tags=flavor.tags
                        )+'"')
                        worker_create_process = Popen(
                            WORKER_CREATE.format(
                                hostname=job.target,
                                concurrency=worker.concurrency,
                                flavor=worker.flavor,
                                region=worker.region,
                                provider=worker.provider,
                                tags=flavor.tags
                            ),
                            stdout = PIPE,
                            stderr = PIPE,
                            shell = True,
                            encoding = 'utf-8'
                        )
                        worker.name = worker.hostname = job.target
                        job.status = 'running'
                        worker_process_queue[('create',job.target)]=(worker, worker_create_process, job.job_id, time())
                        log.warning(f'Worker {job.target} creation process has been launched')

            if change:
                session.commit()                
            pending_job = None

            change = False
            for ((action,worker_name),(worker,worker_process,job_id,start_time)) in list(worker_process_queue.items()):
                returncode = worker_process.poll()
                if returncode is not None:
                    change = True
                    job = session.query(Job).get(job_id)
                    del(worker_process_queue[(action,worker_name)])
                    if returncode == 0:
                        log.warning(f'Process {action} succeeded for worker {worker.name}.')
                        job.log = worker_process.stdout.read()
                        job.status = 'succeeded'

                        if action=='destroy':
                            #session.execute(Worker.__table__.delete().where(
                            #    Worker.__table__.c.worker_id==worker.worker_id))
                            log.warning(f'Deleting worker {worker.name} ({worker.worker_id}) after destruction')
                            real_worker = session.query(Worker).get(worker.worker_id)
                            if real_worker is not None:
                                #session.delete(real_worker)
                                worker_delete(real_worker, session, is_destroyed=True, commit=False)
                            else:
                                log.error(f'Could not find a worker with worker_id {worker.worker_id}')
                            #worker_dao.delete(worker.worker_id, is_destroyed=True)
                    else:
                        stderr = worker_process.stderr.read()
                        log.warning(f'Process {action} failed for worker {worker.name}: {stderr}')
                        job.log = worker_process.stdout.read() + stderr
                        log.warning(f'Job output is {job.log}')
                        if job.retry > 0:
                            job.retry -= 1
                            job.status = 'pending'
                        else:
                            job.status = 'failed'
                            if action=='create':
                                worker = session.query(Worker).get(job.args['worker_id'])
                                worker.status = 'failed'
                elif time() - start_time > JOB_MAX_LIFETIME:
                    log.warning(f'Process {action} is taking too long for worker {worker.name}, sending TERM signal.')
                    worker_process.terminate()
                elif time() - start_time > JOB_MAX_LIFETIME + TERMINATE_TIMEOUT:
                    log.warning(f'Process {action} is really taking too long for worker {worker.name}, sending KILL signal.')
                    worker_process.kill()

            for job in list(session.query(Job).filter(Job.status == 'running')):
                if job.action=='worker_deploy':
                    action='create'
                elif job.action=='worker_destroy':
                    action='destroy'
                else:
                    action=job.action
                if (action, job.target) not in worker_process_queue:
                    log.warning(f'Job {(job.action, job.target)} seems to have failed, not in {worker_process_queue}')
                    job.status='failed'
                    change = True

            if change:
                session.commit()
                
            for process_name, process in list(other_process_queue):
                try:
                    if not process.is_alive():
                        other_process_queue.remove((process_name, process))
                        log.warning(f'Job {process_name} is done.')
                except Exception as e:
                    log.exception(f'Job {process_name} failed: {e}')
                    other_process_queue.remove((process_name, process))

                                
            ########  ########  ######  ########  ##     ## #### ######## ######## ########   ######  
            ##     ## ##       ##    ## ##     ## ##     ##  ##     ##    ##       ##     ## ##    ## 
            ##     ## ##       ##       ##     ## ##     ##  ##     ##    ##       ##     ## ##       
            ########  ######   ##       ########  ##     ##  ##     ##    ######   ########   ######  
            ##   ##   ##       ##       ##   ##   ##     ##  ##     ##    ##       ##   ##         ## 
            ##    ##  ##       ##    ## ##    ##  ##     ##  ##     ##    ##       ##    ##  ##    ## 
            ##     ## ########  ######  ##     ##  #######  ####    ##    ######## ##     ##  ######  
                        
            change = False
            task1 = aliased(Task)
            task2 = aliased(Task)
            recyclable_worker_active_tasks = {}
            worker_task_properties = {}
            worker_active_batch = {}
            recyclable_worker_list = list(session.query(Worker,Task.batch,func.count(distinct(Task.task_id))).\
                    join(Execution,and_(Worker.worker_id==Execution.worker_id,Execution.status=='running'), isouter=True).\
                    join(Execution.task,isouter=True).group_by(Worker,Task.batch))
            worker_batch_task = dict(session.query(Worker,func.count(Task.task_id)).\
                                     join(Task, and_(Task.batch==Worker.batch, Task.status=='pending'),isouter=True).\
                                     group_by(Worker))
            for worker,batch,worker_tasks in recyclable_worker_list:
                if worker not in worker_batch_task or worker_batch_task[worker] == 0:
                    if worker not in recyclable_worker_active_tasks:
                        recyclable_worker_active_tasks[worker]=0
                        worker_task_properties[worker] = json_module.loads(worker.task_properties)
                        worker_active_batch[worker]=[]
                    weight,_ = worker_task_properties[worker].get(batch,(1,0))
                    recyclable_worker_active_tasks[worker] += weight * worker_tasks
            
                    if worker_tasks == 0:
                        if batch in worker_task_properties[worker]:
                            log.warning(f'-> Cleaning batch {batch} from worker {worker} task properties 1')
                            change=True
                            del worker_task_properties[worker][batch] 
                            worker.task_properties=json_module.dumps(worker_task_properties[worker])
                    else:
                        worker_active_batch[worker].append(batch)
            for worker,task_properties in worker_task_properties.items():
                for batch in list(task_properties.keys()):
                    if batch not in worker_active_batch[worker]:
                        log.warning(f'-> Cleaning batch {batch} from worker {worker} task properties 2 : {worker_task_properties}')
                        change=True
                        del worker_task_properties[worker][batch]
                        worker.task_properties=json_module.dumps(worker_task_properties[worker])
            active_recruiters = list(session.query(Recruiter,func.count(distinct(Task.task_id)),func.count(distinct(Worker.worker_id))).\
                    join(Task,and_(Task.batch==Recruiter.batch,Task.status=='pending')).\
                    join(Worker,Worker.batch==Recruiter.batch,isouter=True).\
                    group_by(Recruiter.batch,Recruiter.rank).order_by(Recruiter.batch,Recruiter.rank))
            #pending_workers = dict(session.query(Recruiter,func.count(distinct(Worker.worker_id))).\
            #        join(Task,and_(Task.batch==Recruiter.batch,Task.status=='pending')).\
            #        join(Worker,and_(Worker.batch==Recruiter.batch,Worker.status!='running'),isouter=True).\
            #        group_by(Recruiter.batch,Recruiter.rank).order_by(Recruiter.batch,Recruiter.rank))
            newly_recruited_workers = []   
            for recruiter,pending_tasks,workers in active_recruiters:
                log.warning(f'-> recruiting for recruiter {recruiter} with {pending_tasks} pending tasks and {workers} current workers')
                if recruiter.minimum_tasks and recruiter.minimum_tasks > pending_tasks:
                    log.warning(f'  --> not enough tasks, not recruiting ({pending_tasks} is below the minimum of {recruiter.minimum_tasks})')
                    continue
                if recruiter.maximum_workers and recruiter.maximum_workers <= workers:
                    log.warning(f'  --> too many workers already, not recruiting ({recruiter} has reached the maximum of {recruiter.maximum_workers})')
                    continue
                nb_workers = math.ceil(pending_tasks/recruiter.tasks_per_worker) - workers
                log.warning(f'  --> we need {nb_workers} because {pending_tasks} pending tasks ({recruiter.tasks_per_worker} expected per worker) and we already have {workers} workers.')
                if recruiter.maximum_workers and recruiter.maximum_workers < nb_workers + workers:
                    nb_workers = recruiter.maximum_workers - workers
                    log.warning(f'  --> adjusting to {nb_workers} because maximum is {recruiter.maximum_workers} and \
we already have {workers} workers')
                if nb_workers <= 0:
                    log.warning(f'  --> giving up')
                    continue
                
                if len(recyclable_worker_active_tasks.items())==0:
                    log.warning(f'  --> No recyclable workers {recyclable_worker_active_tasks}')
                for worker, active_tasks  in recyclable_worker_active_tasks.items():  
                    if worker.batch != recruiter.batch and recruiter.match_flavor(worker, session=session) \
                            and active_tasks<worker.concurrency and nb_workers>0 and worker not in newly_recruited_workers:
                        previous_batch = worker.batch
                        previous_concurrency = worker.concurrency
                        previous_task_properties = worker_task_properties[worker]

                        task_ratio = recruiter.worker_concurrency / previous_concurrency
                        task_properties = dict([(batch, ( max(ratio*task_ratio,recruiter.worker_concurrency) , prio+1 )) 
                                                for batch,(ratio,prio) in previous_task_properties.items()])
                        task_properties[previous_batch] = (task_ratio,1)

                        if recruiter.batch in task_properties:
                            log.warning(f'-> Recruiter {recruiter} tried to recycle {worker} but some task of the same batch from a previous recycling round are present, giving up')
                            continue
                        
                        log.warning(f'-> Recruiting worker {worker} from batch {previous_batch} to {recruiter.batch}')
                        newly_recruited_workers.append(worker)
                        change = True
                        worker.batch = recruiter.batch
                        worker.prefetch = recruiter.worker_prefetch
                        worker.concurrency = recruiter.worker_concurrency
                        worker.task_properties = json_module.dumps(task_properties)
                        session.add(worker)
                        nb_workers -= 1
                    else:
                        if worker.batch == recruiter.batch:
                            reason = 'already recruited'
                        elif worker.flavor != recruiter.worker_flavor:
                            reason = 'not the right flavor'
                        elif active_tasks>=worker.concurrency:
                            reason = f'too busy {active_tasks}>={worker.concurrency}'
                        elif nb_workers <= 0:
                            reason = f'no more workers needed'
                        elif worker in newly_recruited_workers:
                            reason = f'it was recently recruited by another recruiter'
                        else:
                            reason = f'something mysterious that should never occur'
                        log.warning(f'  --> {worker} not suitable because {reason} ')
                
                if recruiter.worker_provider is not None and recruiter.worker_region is not None and nb_workers>0:
                    if recruiter.worker_provider=='auto' or recruiter.worker_region=='auto' or recruiter.worker_flavor.startswith('auto'):
                        log.warning(' -> Auto recruiter detected')
                        worker_provider = None if recruiter.worker_provider=='auto' else recruiter.worker_provider
                        worker_region = None if recruiter.worker_region=='auto' else recruiter.worker_region
                        protofilters=''
                        if recruiter.worker_flavor.startswith('auto'):
                            worker_flavor=None
                            if PROTOFILTER_SEPARATOR in recruiter.worker_flavor:
                                protofilters = PROTOFILTER_SEPARATOR.join(
                                        recruiter.worker_flavor.split(PROTOFILTER_SEPARATOR)[1:])
                        else:
                            worker_flavor=recruiter.worker_flavor
                        worker_to_find=nb_workers
                        
                        while worker_to_find>0:
                            flavor_list=find_flavor(session, provider=worker_provider, region=worker_region, 
                                                            flavor=worker_flavor, protofilters=protofilters, limit=None)
                            for current_flavor in flavor_list:
                                if current_flavor['available']>0:
                                    break
                            else:
                                break
                            worker_to_find-=1
                            current_flavor=to_obj(current_flavor)
                            log.warning(f'-> Deploying one worker from {current_flavor.provider},{current_flavor.region} : {current_flavor.name}')
                            session.add(
                                Job(target='', 
                                    action='worker_create', 
                                    args={
                                        'concurrency': recruiter.worker_concurrency, 
                                        'prefetch': recruiter.worker_prefetch,
                                        'flavor': current_flavor.name,
                                        'region': current_flavor.region,
                                        'provider': current_flavor.provider,
                                        'batch': recruiter.batch
                                    }
                                )
                            )
                            change = True
                        if worker_to_find>0:
                            log.warning(f'-> Could not find enough available flavors of the right kind, missing {worker_to_find}')
                            
                                


                    else:
                        for _ in range(nb_workers):
                            log.warning(f'-> Deploying one worker from {recruiter.worker_provider}')
                            session.add(
                                Job(target='', 
                                    action='worker_create', 
                                    args={
                                        'concurrency': recruiter.worker_concurrency, 
                                        'prefetch': recruiter.worker_prefetch,
                                        'flavor': recruiter.worker_flavor,
                                        'region': recruiter.worker_region,
                                        'provider': recruiter.worker_provider,
                                        'batch': recruiter.batch
                                    }
                                )
                            )
                        change = True
                
            if change:
                session.commit()
                



            ########  ########  #######  ##     ## #### ########  ######## ##     ## ######## ##    ## ########  ######  
            ##     ## ##       ##     ## ##     ##  ##  ##     ## ##       ###   ### ##       ###   ##    ##    ##    ## 
            ##     ## ##       ##     ## ##     ##  ##  ##     ## ##       #### #### ##       ####  ##    ##    ##       
            ########  ######   ##     ## ##     ##  ##  ########  ######   ## ### ## ######   ## ## ##    ##     ######  
            ##   ##   ##       ##  ## ## ##     ##  ##  ##   ##   ##       ##     ## ##       ##  ####    ##          ## 
            ##    ##  ##       ##    ##  ##     ##  ##  ##    ##  ##       ##     ## ##       ##   ###    ##    ##    ## 
            ##     ## ########  ##### ##  #######  #### ##     ## ######## ##     ## ######## ##    ##    ##     ######  



            change = False
            task1 = aliased(Task)
            task2 = aliased(Task)
            active_requirements = session.query(task1,task2.status).\
                                    join(task1,Requirement.task).filter(task1.status == 'waiting').\
                                    join(task2,Requirement.other_task)
            candidate_tasks = []
            failed_requirements = []
            for task,status in list(active_requirements):
                if status=='succeeded' and task not in candidate_tasks:
                    candidate_tasks.append(task)
                if status!='succeeded' and task not in failed_requirements:
                    failed_requirements.append(task)
            for task in candidate_tasks:
                if task not in failed_requirements:
                    task.status='pending'
                    session.add(task)
                    change = True
            if change:
                session.commit()




                
        except Exception as e1:
            log.exception('An exception occured during server main loop:')
            while True:
                sleep(MAIN_THREAD_SLEEP)
                try:
                    log.warning('Trying to reconnect...')
                    session.close()
                    with app.app_context():
                        session = Session(db.engine)
                    break
                except Exception as e2:
                    log.exception(f'Error while trying to reconnect: {e2}')
            if pending_job is not None:
                session.query(Job).filter(Job.job_id==job.job_id).update(
                    {'status':'failed', 'log':f'Job failed due to exception {e1}, see logs for details'})
                session.commit()
        sleep(MAIN_THREAD_SLEEP)