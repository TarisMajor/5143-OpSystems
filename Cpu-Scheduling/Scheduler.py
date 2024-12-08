import requests
import json
import copy
import time
from contextlib import contextmanager
from rich import print
from cpu_jobs import getJob, getBurst, getBurstsLeft, getJobsLeft
from job import Job
from rich.table import Table
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.align import Align
import sys
from pynput import keyboard


def getConfig(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def init(config, seed):
    """
    This function will initialize the client and return the `client_id` and `session_id`
    """
    route = f"http://profgriffin.com:8000/init?seed={seed}"
    r = requests.post(route,json=config)
    if r.status_code == 200:
        response = r.json()
        return response
    else:
        print(f"Error: {r.status_code}")
        return " "

def update_row(table: Table, row_index: int, new_values: list):
    if row_index < len(table.rows):
        for column_index, new_value in enumerate(new_values):
            table.columns[column_index]._cells[row_index] = new_value

@contextmanager
def beat(length: int = 1):
    yield
    time.sleep(length * BEAT_TIME)
    
def on_press(key):
    global paused
    try:
        if key == keyboard.Key.space:  # If the spacebar is pressed
            paused = not paused  # Toggle pause state
    except AttributeError:
        pass

def myKwargs(argv):
    """This process command line arguments and lets you "configure" the current run.
       It takes parameters that look like: key=value or num_people=100 (with NO spaces between)
       and puts them into a python dictionary that looks like:
       {
           "key":"value",
           "num_people":100
       }

       If a parameter doesn't have an "=" sign in it, it puts it into a list
       Both the dictionary (kwargs) and list (args) get returned.
       See usage below under if__name__=='__main__'
    """
    kwargs = {}
    args = []
    for param in argv:
        if '=' in param:
            k, v = param.split('=')
            if v.isnumeric():
                kwargs[k] = int(v)
            else:
                kwargs[k] = v
        else:
            if param.isnumeric():
                param = int(param)
            args.append(param)

    return kwargs, args

if __name__ == "__main__":
    
    kwargs, args = myKwargs(sys.argv)

    # Extract command-line arguments
    sched = str(kwargs["sched"])  # First argument (sched)
    seed = int(kwargs["seed"])  # Second argument (seed)
    cpus = int(kwargs["cpus"])  # Third argument (cpus)
    ios = int(kwargs["ios"])   # Fourth argument (ios)
    config_json = kwargs["config"]  # Fifth argument (config)
    console = Console()
    layout = Layout()
    BEAT_TIME = 0.04
    
    console.clear()
    
    paused = False
    
    tables = []

    if sched == "FCFS" or sched == "ALL":
        table1 = Table(title="FCFS", show_header=True, show_footer=False, header_style="bold magenta")
        table1_centered = Align.center(table1)
        tables.append(table1_centered)
        
    if sched == "PB" or sched == "ALL":
        table2 = Table(title="PB", show_header=True, show_footer=False,header_style="bold magenta")
        table2_centered = Align.center(table2)
        tables.append(table2_centered)
        
        
    if sched == "RR" or sched == "ALL":
        table3 = Table(title="RR", show_header=True, show_footer=False,header_style="bold magenta")
        table3_centered = Align.center(table3)
        tables.append(table3_centered)
        
    if sched == "MLFQ" or sched == "ALL":
        table4 = Table(title="MLFQ", show_header=True, show_footer=False,header_style="bold magenta")
        table4_centered = Align.center(table4)
        tables.append(table4_centered)
    
    for table in tables:
        layout.split_column(
            Layout(table)
        )
        
    if sched == "ALL":
        layout.split_column(
            Layout(table1_centered),
            Layout(table2_centered),
            Layout(table3_centered),
            Layout(table4_centered)
        )
    
 
    """
    Initialize queues for different CPU scheduling algorithms:
    
    - FCFS (First-Come, First-Served)
    - RR (Round Robin)
    - PB (Priority-Based)
    - MLFQ (Multi-Level Feedback Queue)
    
    Each scheduling algorithm maintains separate queues for:
    - ReadyQueue: Jobs ready to be executed.
    - WaitingQueue: Jobs waiting for I/O operations.
    - IO_Queue: Jobs currently using I/O devices.
    - FinishedQueue: Jobs that have completed execution.
    - Running: Jobs currently being executed on the CPU.
    - NewQueue: Newly arrived jobs that are not yet ready.
    """
    # region Queues
    FCFS_ReadyQueue = []
    FCFS_WaitingQueue = []
    FCFS_IO_Queue = []
    FCFS_FinishedQueue = []
    FCFS_Running = []
    
    RR_ReadyQueue = []
    RR_WaitingQueue = []
    RR_IO_Queue = []
    RR_FinishedQueue = []
    RR_Running = []
    
    PB_ReadyQueue = []
    PB_WaitingQueue = []
    PB_IO_Queue = []
    PB_FinishedQueue = []
    PB_Running = []
    
    MLFQ_ReadyQueue_P1 = []
    MLFQ_ReadyQueue_P2 = []
    MLFQ_ReadyQueue_P3 = []
    MLFQ_ReadyQueue_P4 = []
    MLFQ_WaitingQueue = []
    MLFQ_IO_Queue = []
    MLFQ_FinishedQueue = []
    MLFQ_Running = []
    # endregion
    
    # General New Queue
    NewQueue = []
    
    preliminary_jobs = {}
    
    config = getConfig(config_json)
    base_url = 'http://profgriffin.com:8000/'
    response = init(config, seed)
      
    client_id = config['client_id']
    start_clock = response['start_clock']
    session_id = response['session_id']

    clock = start_clock   
    
    listener = keyboard.Listener(
        on_press=on_press
    )
    listener.start()
    with Live(layout, console=console, refresh_per_second=1750, vertical_overflow="visible") as live:
        
        if paused:
            print("Program paused. Press spacebar to resume.")
            while paused:  # Stay in this loop until spacebar is pressed again
                time.sleep(0.1)  # Avoid 100% CPU usage
        else:
            print("Program running...")
            time.sleep(1)  # Simulate work being done
    
        # region Setting up the tables to display the objects
        if sched == "FCFS" or sched == "ALL":
            with beat(1):
                table1.add_column("Arrival Time", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table1.add_column("New Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table1.add_column("Ready Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table1.add_column("Running", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table1.add_column("Waiting Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table1.add_column("IO Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table1.add_column("Finished Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table1.add_column("Exit Time", justify="center", style="cyan", no_wrap=True)
                
        if sched == "PB" or sched == "ALL":
            with beat(1):
                table2.add_column("Arrival Time", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table2.add_column("New Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table2.add_column("Ready Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table2.add_column("Running", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table2.add_column("Waiting Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table2.add_column("IO Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table2.add_column("Finished Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table2.add_column("Exit Time", justify="center", style="cyan", no_wrap=True)
                
        if sched == "RR" or sched == "ALL":
            with beat(1):
                table3.add_column("Arrival Time", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table3.add_column("New Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table3.add_column("Ready Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table3.add_column("Running", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table3.add_column("Waiting Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table3.add_column("IO Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table3.add_column("Finished Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table3.add_column("Exit Time", justify="center", style="cyan", no_wrap=True)
                
        if sched == "MLFQ" or sched == "ALL":
            with beat(1):
                table4.add_column("Arrival Time", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table4.add_column("New Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table4.add_column("Ready Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table4.add_column("Running", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table4.add_column("Waiting Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table4.add_column("IO Queue", justify="center", style="cyan", no_wrap=True)
            with beat(1):
                table4.add_column("Finished Queue", justify="center", style="cyan", no_wrap=True) 
            with beat(1):
                table4.add_column("Exit Time", justify="center", style="cyan", no_wrap=True)   
        # endregion
        
        totalTime = 0
    
        cpu_time = 0
        
        Working = True
        
        Num_CPUs = cpus
        
        once = 0
        # Getting the jobs and setting the scheduler in motion
        while(Working == True):
            while paused:
                time.sleep(0.1)

            #region Get job from API
            jobsleft = getJobsLeft(client_id, session_id) # Gets an integer
            
            response = " "
            
            if once < 1:
                once += 1
                num_jobs = jobsleft

            if jobsleft == 0:
                pass
            else:
                response = getJob(client_id,session_id,clock)
                if response and response['success']:
                    if response['data']:
                        for data in response['data']:
                            job_id = data['job_id']
                            if job_id not in preliminary_jobs:
                                # example data
                                # {
                                #   "job_id": 1,
                                #   "session_id": 9,
                                #   "arrival_time": 5275,
                                #   "priority": 1
                                # }
                                preliminary_jobs[job_id] = {'data': data, 'bursts':{}}
                            
                        for job_id in preliminary_jobs:
                            
                            burstsleft = getBurstsLeft(client_id, session_id, job_id) # Recieves an integer
                            if not burstsleft:
                                continue
                            for i in range(burstsleft):
                                bresp = getBurst(client_id, session_id, job_id) # recieves a dictionary
                                if isinstance(bresp, dict) and 'success' in bresp and bresp['success']:
                                    #"data": {
                                    #     "burst_id": 1,
                                    #     "burst_type": "CPU",
                                    #     "duration": 1
                                    #   }
                                    burst = bresp['data'] #gets the burst id, burst type and duration
                                    bid = burst['burst_id']
                                    preliminary_jobs[job_id]['bursts'][bid] = burst
                                
                        for job_id in preliminary_jobs:
                            job = preliminary_jobs[job_id]
                            if 'bursts' in job:
                                data = job['bursts']
                                arrival_time = job['data']['arrival_time']
                                id = job['data']['job_id']
                                priority =job['data']['priority']
                                temp_type = []
                                temp_time = []
                                for burst_id in data:
                                    temp_type.append(data[burst_id]['burst_type'])
                                    temp_time.append(data[burst_id]['duration'])
                                    
                                burst_type = temp_type
                                burst_time = temp_time
                                
                                # Creates a new job
                                newjob = Job(id, arrival_time, burst_type, burst_time, priority)
                                NewQueue.append(newjob)
                                # Add to all tables
                                with beat(5):
                                    if sched == "FCFS" or sched == "ALL":
                                        table1.add_row(str(newjob.get_arrival_time()),f"J{newjob.get_id()}, BT: {newjob.get_burst_type()}"," ", " ", " ", " ", " ")
                                    if sched == "PB" or sched == "ALL":
                                        table2.add_row(str(newjob.get_arrival_time()),f"J{newjob.get_id()}, BT: {newjob.get_burst_type()}"," ", " ", " ", " ", " ")
                                    if sched == "RR" or sched == "ALL":
                                        table3.add_row(str(newjob.get_arrival_time()),f"J{newjob.get_id()}, BT: {newjob.get_burst_type()}"," ", " ", " ", " ", " ")
                                    if sched == "MLFQ" or sched == "ALL":   
                                        table4.add_row(str(newjob.get_arrival_time()),f"J{newjob.get_id()}, BT: {newjob.get_burst_type()}"," ", " ", " ", " ", " ")
                                
                        preliminary_jobs.clear()
            #endregion
            
            if len(NewQueue) > 0:
                # Add newly arrived jobs to all queues
                # This is because we want to be able to simulate all scheduling algorithms
                # at the same time, and we want to use the same jobs for all of them.
                # So we add the job to all queues, and then remove it from the NewQueue
                for job in NewQueue:
                    if sched == "FCFS" or sched == "ALL":
                        FCFS_ReadyQueue.append(copy.deepcopy(job))  # Add to FCFS Ready Queue
                    if sched == "MLFQ" or sched == "ALL":
                        MLFQ_ReadyQueue_P1.append(copy.deepcopy(job))  # Add to MLFQ Ready Queue
                    if sched == "PB" or sched == "ALL":
                        PB_ReadyQueue.append(copy.deepcopy(job))   # Add to Priority Based Ready Queue
                    if sched == "RR" or sched == "ALL":
                        RR_ReadyQueue.append(copy.deepcopy(job))   # Add to Round Robin Ready Queue
                    
                    # Add to all tables
                    with beat(5):
                        if sched == "FCFS" or sched == "ALL":
                            update_row(table1, (job.get_id()-1), [str(job.get_arrival_time())," ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " ", " ", " "])
                        if sched == "PB" or sched == "ALL":
                            update_row(table2, (job.get_id()-1), [str(job.get_arrival_time())," ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " ", " ", " "])
                        if sched == "RR" or sched == "ALL":
                            update_row(table3, (job.get_id()-1), [str(job.get_arrival_time())," ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " ", " ", " "])
                        if sched == "MLFQ" or sched == "ALL":   
                            update_row(table4, (job.get_id()-1), [str(job.get_arrival_time())," ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " ", " ", " "])
                    NewQueue.remove(job)        # Remove from New Queue, since it's been added to all queues
            
            """
            FCFS (First Come First Served) - This is a scheduling algorithm that does not preempt the CPU while it is executing a job.
            It will simply execute the jobs in the order they arrive in the ReadyQueue.
            """
            #region FCFS
            if sched == "FCFS" or sched == "ALL":
                if len(FCFS_ReadyQueue) > 0:
                    for job in FCFS_ReadyQueue:
                        if len(FCFS_Running) < Num_CPUs:
                            FCFS_Running.append(job)
                            with beat(5):
                                update_row(table1, (job.get_id()-1), [str(job.get_arrival_time())," ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " ", " "])
                            FCFS_ReadyQueue.remove(job)
                            
                        else:
                            job.increment_ready_wait_time()
                            with beat(5):
                                update_row(table1, (job.get_id()-1), [str(job.get_arrival_time())," ",f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " ", " ", " "])
                            
                for job in FCFS_Running:
                    if job.get_burst_type() == "IO":
                        FCFS_WaitingQueue.append(job)
                        with beat(5):
                            update_row(table1, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " "])
                        FCFS_Running.remove(job)
                        continue
                    
                    if job.get_burst_type() == "CPU":
                        if job.get_burst_time() == 0:
                            job.get_next_burst()
                            FCFS_WaitingQueue.append(job)
                            with beat(5):
                                update_row(table1, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " "])
                        
                            FCFS_Running.remove(job)
                            continue
                            
                        else:
                            job.decrement_burst_time()
                            job.increment_running_time()
                            with beat(5):
                                update_row(table1, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " ", " "])
                        
                            if job.get_burst_time() == 0:
                                job.get_next_burst()
                                FCFS_WaitingQueue.append(job)
                                with beat(5):
                                    update_row(table1, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " "])
                        
                                FCFS_Running.remove(job)
                                continue
                            
                    if job.get_burst_type() == "EXIT":
                        job.set_exit_time(clock)
                        FCFS_FinishedQueue.append(job)
                        with beat(5):
                            update_row(table1, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", str(job.get_exit_time())])
                        FCFS_Running.remove(job)
                                    
                for job in FCFS_WaitingQueue:
                    if job.get_burst_type() == "IO":
                        if len(FCFS_IO_Queue) < ios:
                            FCFS_IO_Queue.append(job)
                            with beat(5):
                                update_row(table1, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " "])
                            FCFS_WaitingQueue.remove(job)
                        else:
                            job.increment_io_wait_time()
                            with beat(5):
                                update_row(table1, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " "])
                    
                    else:
                        FCFS_ReadyQueue.append(job)
                        with beat(5):
                            update_row(table1, (job.get_id()-1), [str(job.get_arrival_time()), " ",f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " ", " ", " "])
                        FCFS_WaitingQueue.remove(job)
                
                for job in FCFS_IO_Queue:
                    
                    if job.get_burst_time() == 0:
                        job.get_next_burst()
                        FCFS_ReadyQueue.append(job)
                        with beat(5):
                            update_row(table1, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " ", " ", " "])
                        FCFS_IO_Queue.remove(job)
                        
                    else:
                        job.decrement_burst_time()
                        
                        with beat(5):
                            update_row(table1, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " "])
                        if job.get_burst_time() == 0:
                            job.get_next_burst()
                            FCFS_ReadyQueue.append(job)
                            with beat(5):
                                update_row(table1, job.get_id()-1, [str(job.get_arrival_time()), " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " ", " ", " "])
                            FCFS_IO_Queue.remove(job)
            #endregion
            
            """
            Priority Based Scheduling (PB) is a scheduling algorithm that selects jobs to execute based on their priority levels.
            Each job is assigned a priority, and the scheduler selects the job with the highest priority to execute next.
            If two jobs have the same priority, they are typically scheduled in First-Come, First-Served (FCFS) order.
            This algorithm is pre-emptive, meaning that a higher-priority job can interrupt and take over the CPU from a running lower-priority job.
            The main advantage of priority scheduling is that it ensures critical tasks are completed earlier, improving response time for high-priority tasks.
            However, it can lead to starvation of lower-priority jobs if higher-priority jobs continuously enter the system.
            """
            # region Priority Based
            if sched == "PB" or sched == "ALL":
                
                if len(PB_ReadyQueue) > 0:
                    for job in PB_ReadyQueue:
                        # If there's room in the CPU
                        if len(PB_Running) < Num_CPUs:
                            PB_Running.append(job)
                            with beat(5):
                                update_row(table2, (job.get_id()-1), [str(job.get_arrival_time()), " ", " " ,f"J{job.get_id()} BT: {job.get_burst_type()} P: {job.get_priority()}", " ", " ", " ", " "])
                            PB_ReadyQueue.remove(job)
                        
                        else:
                            for PB_job in PB_Running:
                                # If the job has a higher priority
                                if PB_job.get_priority() > job.get_priority():
                                    PB_Running.append(job)
                                    with beat(5):
                                        update_row(table2, (job.get_id()-1), [str(job.get_arrival_time()), " ", " " ,f"J{job.get_id()} BT: {job.get_burst_type()} P: {job.get_priority()}", " ", " ", " ", " "])
                                    PB_ReadyQueue.remove(job)
                                    PB_WaitingQueue.append(PB_job)
                                    with beat(5):
                                        update_row(table2, (PB_job.get_id()-1), [str(PB_job.get_arrival_time()), " ", " ", "" ,f"J{PB_job.get_id()}, BT: {PB_job.get_burst_type()}", " ", " ", " "])
                                    PB_Running.remove(PB_job)
                                    break
                            
                                else:
                                    job.increment_ready_wait_time()
            
                for job in PB_Running:
                    if job.get_burst_type() == "IO":
                        PB_WaitingQueue.append(job)
                        with beat(5):
                            update_row(table2, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " " ,f"J{job.get_id()} BT: {job.get_burst_type()} P: {job.get_priority()}", " ", " ", " "])
                        PB_Running.remove(job)
                        continue
                    
                    if job.get_burst_type() == "CPU":
                        if job.get_burst_time() == 0:
                            job.get_next_burst()
                            PB_WaitingQueue.append(job)
                            with beat(5):
                                update_row(table2, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " " ,f"J{job.get_id()} BT: {job.get_burst_type()} P: {job.get_priority()}", " ", " ", " "])
                            PB_Running.remove(job)
                            continue
                            
                        else:
                            job.decrement_burst_time()
                            job.increment_running_time()
                            with beat(5):
                                update_row(table2, (job.get_id()-1), [str(job.get_arrival_time()), " ", " " ,f"J{job.get_id()} BT: {job.get_burst_type()} P: {job.get_priority()}", " ", " ", " ", " "])
                            if job.get_burst_time() == 0:
                                job.get_next_burst()
                                PB_WaitingQueue.append(job)
                                with beat(5):
                                    update_row(table2, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " " ,f"J{job.get_id()} BT: {job.get_burst_type()} P: {job.get_priority()}", " ", " ", " "])
                                PB_Running.remove(job)
                                continue
                            
                    if job.get_burst_type() == "EXIT":
                        job.set_exit_time(clock)
                        PB_FinishedQueue.append(job)
                        with beat(5):
                            update_row(table2, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", " ", " " ,f"J{job.get_id()} BT: {job.get_burst_type()} P: {job.get_priority()}", str(job.get_exit_time())])
                        PB_Running.remove(job)
                    
                for job in PB_WaitingQueue:
                    if job.get_burst_type() == "IO":
                        if len(PB_IO_Queue) < ios:
                            PB_IO_Queue.append(job)
                            with beat(5):
                                update_row(table2, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", " " ,f"J{job.get_id()} BT: {job.get_burst_type()} P: {job.get_priority()}", " ", " "])
                            PB_WaitingQueue.remove(job)
                        else:
                            job.increment_io_wait_time()
                            
                    else:
                        PB_ReadyQueue.append(job)
                        with beat(5):
                            update_row(table2, (job.get_id()-1), [str(job.get_arrival_time()), " " ,f"J{job.get_id()} BT: {job.get_burst_type()} P: {job.get_priority()}"," ", " ", " ", " ", " "])
                        PB_WaitingQueue.remove(job)
                
                    
                for job in PB_IO_Queue:
                    if job.get_burst_time() == 0:
                        job.get_next_burst()
                        PB_ReadyQueue.append(job)
                        with beat(5):
                            update_row(table2, (job.get_id()-1), [str(job.get_arrival_time()), " " ,f"J{job.get_id()} BT: {job.get_burst_type()} P: {job.get_priority()}"," ", " ", " ", " ", " "])
                        PB_IO_Queue.remove(job)
                        
                    else:
                        job.decrement_burst_time()
                        with beat(5):
                            update_row(table2, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", " " ,f"J{job.get_id()} BT: {job.get_burst_type()} P: {job.get_priority()}", " ", " "])
                        if job.get_burst_time() == 0:
                            job.get_next_burst()
                            PB_ReadyQueue.append(job)
                            with beat(5):
                                update_row(table2, (job.get_id()-1), [str(job.get_arrival_time()), " " ,f"J{job.get_id()} BT: {job.get_burst_type()} P: {job.get_priority()}"," ", " ", " ", " ", " "])
                            PB_IO_Queue.remove(job)
            #endregion
            """
            Round Robin Scheduling (RR) is a scheduling algorithm that assigns a fixed number of CPU time slots to each job.
            """
            #region Round Robin
            if sched == "RR" or sched == "ALL":
                if len(RR_ReadyQueue) > 0:
                    for job in RR_ReadyQueue:
                        if len(RR_Running) < Num_CPUs:
                            RR_Running.append(job)
                            with beat(5):
                                update_row(table3, (job.get_id()-1), [str(job.get_arrival_time()), " ", " " ,f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " ", " "])
                            RR_ReadyQueue.remove(job)
                            
                        else:
                            job.increment_ready_wait_time()
                            
                for job in RR_Running:
                    if job.get_burst_type() == "IO":
                        RR_WaitingQueue.append(job)
                        with beat(5):
                            update_row(table3, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " "])
                        RR_Running.remove(job)
                        continue
                    
                    if job.get_burst_type() == "CPU":
                        if job.get_cpu_time() <= 5:
                            if job.get_burst_time() == 0:
                                job.get_next_burst()
                                job.reset_cpu_time()
                                RR_WaitingQueue.append(job)
                                with beat(5):
                                    update_row(table3, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " "])
                                RR_Running.remove(job)
                                continue
                                
                            else:
                                job.decrement_burst_time()
                                job.increment_running_time()
                                job.increment_cpu_time()
                                if job.get_burst_time() == 0:
                                    job.get_next_burst()
                                    job.reset_cpu_time()
                                    RR_WaitingQueue.append(job)
                                    with beat(5):
                                        update_row(table3, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " "])
                                    RR_Running.remove(job)
                                    continue
                        else:
                            job.reset_cpu_time()
                            RR_WaitingQueue.append(job)
                            with beat(5):
                                update_row(table3, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " "])          
                            RR_Running.remove(job)
                            
                    if job.get_burst_type() == "EXIT":
                        job.set_exit_time(clock)
                        RR_FinishedQueue.append(job)
                        with beat(5):
                            update_row(table3, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", str(job.get_exit_time())])
                        RR_Running.remove(job)
                        
                        
                for job in RR_WaitingQueue:
                    if job.get_burst_type() == "IO":
                        if len(RR_IO_Queue) < ios:
                            RR_IO_Queue.append(job)
                            with beat(5):
                                update_row(table3, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " "])
                            RR_WaitingQueue.remove(job)
                        else:
                            job.increment_io_wait_time()
                            
                    else:
                        RR_ReadyQueue.append(job)
                        with beat(5):
                            update_row(table3, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " ", " ", " "])
                        RR_WaitingQueue.remove(job)
                
                    
                for job in RR_IO_Queue:
                    
                    if job.get_burst_time() == 0:
                        job.get_next_burst()
                        RR_ReadyQueue.append(job)
                        with beat(5):
                            update_row(table3, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " ", " ", " "])
                        RR_IO_Queue.remove(job)
                        
                    else:
                        job.decrement_burst_time()
                        with beat(5):
                            update_row(table3, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " "])
                        if job.get_burst_time() == 0:
                            job.get_next_burst()
                            RR_ReadyQueue.append(job)
                            with beat(5):
                                update_row(table3, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} BT: {job.get_burst_type()}", " ", " ", " ", " ", " "])
                            RR_IO_Queue.remove(job)
            #endregion
            
            """
                MLFQ Scheduling (MLFQ) is a scheduling algorithm that assigns a fixed number of CPU time slots to each job.
            """
            
            # region MLFQ
            if sched == "MLFQ" or sched == "ALL":
                if len(MLFQ_ReadyQueue_P1) > 0:
                    for job in MLFQ_ReadyQueue_P1:
                        job.set_priority(1)
                        # If there's room in the CPU
                        if len(MLFQ_Running) < Num_CPUs:
                            MLFQ_Running.append(job)
                            with beat(5):
                                update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " "])
                            MLFQ_ReadyQueue_P1.remove(job)
                        
                        else:
                            job.increment_ready_wait_time()
                            
                elif len(MLFQ_ReadyQueue_P2) > 0:
                    for job in MLFQ_ReadyQueue_P2:
                        job.set_priority(2)
                        # If there's room in the CPU
                        if len(MLFQ_Running) < Num_CPUs:
                            MLFQ_Running.append(job)
                            with beat(5):
                                update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " "])
                            MLFQ_ReadyQueue_P2.remove(job)
                        
                        else:
                            job.increment_ready_wait_time()
                            job.increment_ML_wait_time()
                            if job.get_ML_wait_time() == 25:
                                MLFQ_ReadyQueue_P1.append(job)
                                with beat(5):
                                    update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                                job.reset_ML_wait_time()
                                MLFQ_ReadyQueue_P2.remove(job)
                            
                elif len(MLFQ_ReadyQueue_P3) > 0:
                    for job in MLFQ_ReadyQueue_P3:
                        job.set_priority(3)
                        # If there's room in the CPU
                        if len(MLFQ_Running) < Num_CPUs:
                            MLFQ_Running.append(job)
                            with beat(5):
                                update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " "])
                            MLFQ_ReadyQueue_P3.remove(job)
                        
                        else:
                            job.increment_ready_wait_time()
                            job.increment_ML_wait_time()
                            if job.get_ML_wait_time() == 50:
                                MLFQ_ReadyQueue_P2.append(job)
                                with beat(5):
                                    update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                                job.reset_ML_wait_time()
                                MLFQ_ReadyQueue_P3.remove(job)
                                
                elif len(MLFQ_ReadyQueue_P4) > 0:
                    for job in MLFQ_ReadyQueue_P4:
                        job.set_priority(4)
                        # If there's room in the CPU
                        if len(MLFQ_Running) < Num_CPUs:
                            MLFQ_Running.append(job)
                            with beat(5):
                                update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " "])
                            MLFQ_ReadyQueue_P4.remove(job)
                        
                        else:
                            job.increment_ready_wait_time()
                            job.increment_ML_wait_time()
                            if job.get_ML_wait_time() == 75:
                                MLFQ_ReadyQueue_P3.append(job)
                                with beat(5):
                                    update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                                job.reset_ML_wait_time()
                                MLFQ_ReadyQueue_P4.remove(job)
            
                for job in MLFQ_Running:
                    if job.get_burst_type() == "IO":
                        MLFQ_WaitingQueue.append(job)
                        with beat(5):
                            update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " "])
                        MLFQ_Running.remove(job)
                        continue
                    
                    if job.get_burst_type() == "CPU":
                        if job.get_priority() == 1:
                            if job.cpu_time <= 3:
                                if job.get_burst_time() == 0:
                                    job.get_next_burst()
                                    job.reset_cpu_time()
                                    MLFQ_WaitingQueue.append(job)
                                    with beat(5):
                                        update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " "])
                                    MLFQ_Running.remove(job)
                                    continue
                                    
                                else:
                                    job.decrement_burst_time()
                                    job.increment_running_time()
                                    job.increment_cpu_time()
                                    if job.get_burst_time() == 0:
                                        job.get_next_burst()
                                        job.reset_cpu_time()
                                        MLFQ_WaitingQueue.append(job)
                                        with beat(5):
                                            update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " "])
                                        MLFQ_Running.remove(job)
                                        continue
                            else:
                                job.reset_cpu_time()
                                job.set_priority(2)
                                MLFQ_WaitingQueue.append(job)
                                with beat(5):
                                    update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " "])
                                MLFQ_Running.remove(job)
                                continue
                            
                        elif job.get_priority() == 2:
                            if job.cpu_time <= 5:
                                if job.get_burst_time() == 0:
                                    job.get_next_burst()
                                    job.reset_cpu_time()
                                    MLFQ_WaitingQueue.append(job)
                                    with beat(5):
                                        update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " "])
                                    MLFQ_Running.remove(job)
                                    continue
                                    
                                else:
                                    job.decrement_burst_time()
                                    job.increment_running_time()
                                    job.increment_cpu_time()
                                    if job.get_burst_time() == 0:
                                        job.get_next_burst()
                                        job.reset_cpu_time()
                                        MLFQ_WaitingQueue.append(job)
                                        with beat(5):
                                            update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " "])
                                        MLFQ_Running.remove(job)
                                        continue
                            else:
                                job.reset_cpu_time()
                                job.set_priority(3)
                                MLFQ_WaitingQueue.append(job)
                                with beat(5):
                                    update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " "])
                                MLFQ_Running.remove(job)
                                continue      
                        elif job.get_priority() == 3:
                            if job.cpu_time <= 7:
                                if job.get_burst_time() == 0:
                                    job.get_next_burst()
                                    job.reset_cpu_time()
                                    MLFQ_WaitingQueue.append(job)
                                    with beat(5):
                                        update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " "])
                                    MLFQ_Running.remove(job)
                                    continue
                                    
                                else:
                                    job.decrement_burst_time()
                                    job.increment_running_time()
                                    job.increment_cpu_time()
                                    if job.get_burst_time() == 0:
                                        job.get_next_burst()
                                        job.reset_cpu_time()
                                        MLFQ_WaitingQueue.append(job)
                                        with beat(5):
                                            update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " "])
                                        MLFQ_Running.remove(job)
                                        continue
                            else:
                                job.reset_cpu_time()
                                job.set_priority(4)
                                MLFQ_WaitingQueue.append(job)
                                with beat(5):
                                    update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " "])
                                MLFQ_Running.remove(job)
                                continue     
                        elif job.get_priority() == 4:
                            if job.cpu_time <= 9:
                                if job.get_burst_time() == 0:
                                    job.get_next_burst()
                                    job.reset_cpu_time()
                                    MLFQ_WaitingQueue.append(job)
                                    with beat(5):
                                        update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " "])
                                    MLFQ_Running.remove(job)
                                    continue
                                
                                else:
                                    job.decrement_burst_time()
                                    job.increment_running_time()
                                    job.increment_cpu_time()
                                    if job.get_burst_time() == 0:
                                        job.get_next_burst()
                                        job.reset_cpu_time()
                                        MLFQ_WaitingQueue.append(job)
                                        with beat(5):
                                            update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " "])
                                        MLFQ_Running.remove(job)
                                        continue
                            
                    if job.get_burst_type() == "EXIT":
                        job.set_exit_time(clock)
                        MLFQ_FinishedQueue.append(job)
                        with beat(5):
                            update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", str(job.get_exit_time())])
                        MLFQ_Running.remove(job)
                        
                        
                for job in MLFQ_WaitingQueue:
                    if job.get_burst_type() == "IO":
                        if len(MLFQ_IO_Queue) < ios:
                            MLFQ_IO_Queue.append(job)
                            with beat(5):
                                update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " "])
                            MLFQ_WaitingQueue.remove(job)
                        else:
                            job.increment_io_wait_time()
                            
                    else:
                        if job.get_priority() == 1:
                            MLFQ_ReadyQueue_P1.append(job)
                            with beat(5):
                                update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                            MLFQ_WaitingQueue.remove(job)
                        elif job.get_priority() == 2:
                            MLFQ_ReadyQueue_P2.append(job)
                            with beat(5):
                                update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                            MLFQ_WaitingQueue.remove(job)
                        elif job.get_priority() == 3:
                            MLFQ_ReadyQueue_P3.append(job)
                            with beat(5):
                                update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                            MLFQ_WaitingQueue.remove(job)
                        elif job.get_priority() == 4:
                            MLFQ_ReadyQueue_P4.append(job)
                            with beat(5):
                                update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                            MLFQ_WaitingQueue.remove(job)
                
                    
                for job in MLFQ_IO_Queue:
                    if job.get_burst_time() == 0:
                        job.get_next_burst()
                        if job.get_priority() == 1:
                            MLFQ_ReadyQueue_P1.append(job)
                            with beat(5):
                                update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                        elif job.get_priority() == 2:
                            MLFQ_ReadyQueue_P2.append(job)
                            with beat(5):
                                update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                        elif job.get_priority() == 3:
                            MLFQ_ReadyQueue_P3.append(job)
                            with beat(5):
                                update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                        elif job.get_priority() == 4:
                            MLFQ_ReadyQueue_P4.append(job)
                            with beat(5):
                                update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                        
                        MLFQ_IO_Queue.remove(job)
                        
                    else:
                        job.decrement_burst_time()
                        with beat(5):
                            update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", " ", " ", " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " "])
                        if job.get_burst_time() == 0:
                            job.get_next_burst()
                            if job.get_priority() == 1:
                                MLFQ_ReadyQueue_P1.append(job)
                                with beat(5):
                                    update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                            elif job.get_priority() == 2:
                                MLFQ_ReadyQueue_P2.append(job)
                                with beat(5):
                                    update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                            elif job.get_priority() == 3:
                                MLFQ_ReadyQueue_P3.append(job)
                                with beat(5):
                                    update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                            elif job.get_priority() == 4:
                                MLFQ_ReadyQueue_P4.append(job)
                                with beat(5):
                                    update_row(table4, (job.get_id()-1), [str(job.get_arrival_time()), " ", f"J{job.get_id()} P: {job.get_priority()}", " ", " ", " ", " ", " "])
                            
                            MLFQ_IO_Queue.remove(job)
               
            #endregion
            
            #region Ending Conditions
            if sched == "ALL":
                if len(FCFS_FinishedQueue) == num_jobs and len(PB_FinishedQueue) == num_jobs and len(RR_FinishedQueue) == num_jobs and len(MLFQ_FinishedQueue) == num_jobs:
                    Working = False
                    
            elif sched == "FCFS":
                if len(FCFS_FinishedQueue) == num_jobs:
                    Working = False
            elif sched == "PB":
                if len(PB_FinishedQueue) == num_jobs:
                    Working = False
            elif sched == "RR":
                if len(RR_FinishedQueue) == num_jobs:
                    Working = False
                    
            elif sched == "MLFQ":
                if len(MLFQ_FinishedQueue) == num_jobs:
                    Working = False 
            #endregion
               
            clock += 1
            totalTime += 1
            live.update(layout)
        
        FCFS_sum = 0   
        PB_sum = 0
        RR_sum = 0
        MLFQ_sum = 0
        
        FCFS_ready_sum = 0
        PB_ready_sum = 0
        RR_ready_sum = 0
        MLFQ_ready_sum = 0
        
        FCFS_io_sum = 0
        PB_io_sum = 0
        RR_io_sum = 0
        MLFQ_io_sum = 0
         
        if sched == "ALL" or sched == "FCFS":
            console.print("FCFS")
            for job in FCFS_FinishedQueue:
                util_percentage = (job.get_running_time() / totalTime) * 100
                turnaround = job.get_exit_time() - job.get_arrival_time()
                FCFS_ready_sum += job.get_ready_wait_time()
                FCFS_io_sum += job.get_io_wait_time()
                console.print(f"J{job.get_id()} | Running Time: {job.get_running_time()} | Utilization: {util_percentage:.2f}% | Turnaround: {turnaround}")
                FCFS_sum += turnaround
            average_turnaround = FCFS_sum / len(FCFS_FinishedQueue)
            console.print(f"FCFS Average Turnaround: {average_turnaround} | FCFS Average Ready Wait Time: {FCFS_ready_sum / len(FCFS_FinishedQueue)} | FCFS Average IO Wait Time: {FCFS_io_sum / len(FCFS_FinishedQueue)}")
        
        if sched == "PB" or sched == "ALL":
            console.print("PB")
            for job in PB_FinishedQueue:
                util_percentage = (job.get_running_time() / totalTime) * 100
                turnaround = job.get_exit_time() - job.get_arrival_time()
                console.print(f"J{job.get_id()} | Running Time: {job.get_running_time()} | Utilization: {util_percentage:.2f}% | Turnaround: {turnaround}")
                PB_sum += turnaround
                PB_ready_sum += job.get_ready_wait_time()
                PB_io_sum += job.get_io_wait_time()
            average_turnaround = PB_sum / len(PB_FinishedQueue)
            console.print(f"PB Average Turnaround: {average_turnaround} | PB Average Ready Wait Time: {PB_ready_sum / len(PB_FinishedQueue)} | PB Average IO Wait Time: {PB_io_sum / len(PB_FinishedQueue)}")
        
        if sched == "RR" or sched == "ALL":
            console.print("RR")
            for job in RR_FinishedQueue:
                util_percentage = (job.get_running_time() / totalTime) * 100
                turnaround = job.get_exit_time() - job.get_arrival_time()
                console.print(f"J{job.get_id()} | Running Time: {job.get_running_time()} | Utilization: {util_percentage:.2f}% | Turnaround: {turnaround}")
                RR_sum += turnaround
                RR_ready_sum += job.get_ready_wait_time()
                RR_io_sum += job.get_io_wait_time()
            average_turnaround = RR_sum / len(RR_FinishedQueue)
            console.print(f"RR Average Turnaround: {average_turnaround} | RR Average Ready Wait Time: {RR_ready_sum / len(RR_FinishedQueue)} | RR Average IO Wait Time: {RR_io_sum / len(RR_FinishedQueue)}")
        
        if sched == "MLFQ" or sched == "ALL":
            console.print("MLFQ")
            for job in MLFQ_FinishedQueue:
                util_percentage = (job.get_running_time() / totalTime) * 100
                turnaround = job.get_exit_time() - job.get_arrival_time()
                console.print(f"J{job.get_id()} | Running Time: {job.get_running_time()} | Utilization: {util_percentage:.2f}% | Turnaround: {turnaround}")
                MLFQ_sum += turnaround
                MLFQ_ready_sum += job.get_ready_wait_time()
                MLFQ_io_sum += job.get_io_wait_time()
            average_turnaround = MLFQ_sum / len(MLFQ_FinishedQueue)
            console.print(f"MLFQ Average Turnaround: {average_turnaround} | MLFQ Average Ready Wait Time: {MLFQ_ready_sum / len(MLFQ_FinishedQueue)} | MLFQ Average IO Wait Time: {MLFQ_io_sum / len(MLFQ_FinishedQueue)}")
            
        if sched == "ALL":
            console.print("ALL")
            all_sum = FCFS_sum + PB_sum + RR_sum + MLFQ_sum
            all_ready_sum = FCFS_ready_sum + PB_ready_sum + RR_ready_sum + MLFQ_ready_sum
            all_io_sum = FCFS_io_sum + PB_io_sum + RR_io_sum + MLFQ_io_sum
            average_turnaround = all_sum / num_jobs
            console.print(f"ALL Average Turnaround: {average_turnaround} | ALL Average Ready Wait Time: {all_ready_sum / num_jobs} | ALL Average IO Wait Time: {all_io_sum / num_jobs}")
            