class Process:
    def __init__(self, pid, at, bt):
        self.pid = pid  # Process ID
        self.at = at    # Arrival Time
        self.bt = bt    # Burst Time
        self.ct = 0     # Completion Time
        self.tat = 0    # Turnaround Time
        self.wt = 0     # Waiting Time

def display_table(processes, title):
    print(f"\n--- {title} ---")
    print("PID\tAT\tBT\tCT\tTAT\tWT")
    for p in processes:
        print(f"{p.pid}\t{p.at}\t{p.bt}\t{p.ct}\t{p.tat}\t{p.wt}")
    
    avg_tat = sum(p.tat for p in processes) / len(processes)
    avg_wt = sum(p.wt for p in processes) / len(processes)
    print(f"\nAverage Turnaround Time: {avg_tat:.2f}")
    print(f"Average Waiting Time: {avg_wt:.2f}")

def draw_gantt_chart(history):
    print("\nGantt Chart:")
    # Print the process sequence
    print("|", end="")
    for entry in history:
        print(f"  P{entry[0]}  |", end="")
    print("\n0", end="")
    # Print the time intervals
    for entry in history:
        print(f"      {entry[2]}", end="")
    print("\n")

def fcfs(processes):
    # Task 2: Sort by Arrival Time
    procs = sorted(processes, key=lambda x: x.at)
    current_time = 0
    history = []

    for p in procs:
        if current_time < p.at:
            current_time = p.at
        
        start_time = current_time
        current_time += p.bt
        p.ct = current_time
        p.tat = p.ct - p.at
        p.wt = p.tat - p.bt
        history.append((p.pid, start_time, p.ct))
    
    return procs, history

def sjf_non_preemptive(processes):
    # Task 3: Shortest Job First
    n = len(processes)
    procs = [Process(p.pid, p.at, p.bt) for p in processes] # Copy
    completed = []
    current_time = 0
    history = []
    
    while len(completed) < n:
        # Get processes that have arrived and are not yet completed
        ready_queue = [p for p in procs if p.at <= current_time and p not in completed]
        
        if not ready_queue:
            current_time += 1
            continue
        
        # Pick process with shortest Burst Time
        current_proc = min(ready_queue, key=lambda x: x.bt)
        
        start_time = current_time
        current_time += current_proc.bt
        current_proc.ct = current_time
        current_proc.tat = current_proc.ct - current_proc.at
        current_proc.wt = current_proc.tat - current_proc.bt
        
        completed.append(current_proc)
        history.append((current_proc.pid, start_time, current_proc.ct))
        
    return completed, history

# Task 1: Input Handling
def main():
    n = int(input("Enter number of processes (4-5 recommended): "))
    processes = []
    for i in range(n):
        pid = i + 1
        at = int(input(f"Enter Arrival Time for P{pid}: "))
        bt = int(input(f"Enter Burst Time for P{pid}: "))
        processes.append(Process(pid, at, bt))

    # Run FCFS
    fcfs_res, fcfs_hist = fcfs([Process(p.pid, p.at, p.bt) for p in processes])
    display_table(fcfs_res, "FCFS Results")
    draw_gantt_chart(fcfs_hist)

    # Run SJF
    sjf_res, sjf_hist = sjf_non_preemptive(processes)
    display_table(sjf_res, "SJF (Non-Preemptive) Results")
    draw_gantt_chart(sjf_hist)

if __name__ == "__main__":
    main()
