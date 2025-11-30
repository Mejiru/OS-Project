from collections import deque

# ---------------- Process Class ----------------
class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.start = None
        self.completion = None
        self.waiting = None
        self.turnaround = None

# ---------------- Helper Functions ----------------
def reset(processes):
    for p in processes:
        p.remaining = p.burst
        p.start = None
        p.completion = None
        p.waiting = None
        p.turnaround = None

def print_table(processes):
    print("\nProcess | Arr | Burst | Start | End | Waiting | Turnaround")
    print("-----------------------------------------------------------")
    for p in processes:
        print(f"{p.pid:7} {p.arrival:5} {p.burst:7} {str(p.start):6} {str(p.completion):5} {str(p.waiting):8} {str(p.turnaround):11}")
    avg_w = sum(p.waiting for p in processes)/len(processes)
    avg_t = sum(p.turnaround for p in processes)/len(processes)
    print("-----------------------------------------------------------")
    print("Average Waiting Time   =", round(avg_w, 2))
    print("Average Turnaround Time=", round(avg_t, 2))

def print_gantt(gantt):
    print("\nGantt Chart:")
    bar = ""
    time_line = ""

    for pid, s, e in gantt:
        bar += "|" + pid.center(5)
        time_line += str(s).ljust(6)
    time_line += str(gantt[-1][2])

    print(bar + "|")
    print(time_line)

# ---------------- FCFS ----------------
def fcfs(processes):
    time = 0
    gantt = []
    procs = sorted(processes, key=lambda p: p.arrival)

    for p in procs:
        if time < p.arrival:
            gantt.append(("idle", time, p.arrival))
            time = p.arrival

        p.start = time
        time += p.burst
        p.completion = time
        p.turnaround = p.completion - p.arrival
        p.waiting = p.start - p.arrival
        gantt.append((p.pid, p.start, p.completion))

    return gantt

# ------------ SJF Non-Preemptive --------------
def sjf_non_preemptive(processes):
    time = 0
    finished = 0
    n = len(processes)
    gantt = []

    while finished < n:
        ready = [p for p in processes if p.arrival <= time and p.completion is None]

        if not ready:
            next_arr = min(p.arrival for p in processes if p.completion is None)
            gantt.append(("idle", time, next_arr))
            time = next_arr
            continue

        ready.sort(key=lambda p: p.burst)
        cur = ready[0]

        cur.start = time
        time += cur.burst
        cur.completion = time
        cur.turnaround = cur.completion - cur.arrival
        cur.waiting = cur.start - cur.arrival
        gantt.append((cur.pid, cur.start, cur.completion))
        finished += 1

    return gantt

# -------------- SJF Preemptive (SRTF) ---------------
def sjf_preemptive(processes):
    time = 0
    finished = 0
    gantt = []

    while finished < len(processes):
        ready = [p for p in processes if p.arrival <= time and p.remaining > 0]

        if not ready:
            next_arr = min(p.arrival for p in processes if p.remaining > 0)
            gantt.append(("idle", time, next_arr))
            time = next_arr
            continue

        ready.sort(key=lambda p: p.remaining)
        cur = ready[0]

        if cur.start is None:
            cur.start = time

        gantt.append((cur.pid, time, time+1))
        cur.remaining -= 1
        time += 1

        if cur.remaining == 0:
            cur.completion = time
            cur.turnaround = cur.completion - cur.arrival
            cur.waiting = cur.turnaround - cur.burst
            finished += 1

    # Merge consecutive same processes in Gantt
    merged = []
    for pid, s, e in gantt:
        if merged and merged[-1][0] == pid and merged[-1][2] == s:
            merged[-1] = (pid, merged[-1][1], e)
        else:
            merged.append((pid, s, e))

    return merged

# ---------------- Round Robin ----------------
def round_robin(processes, quantum):
    time = 0
    gantt = []
    queue = deque()
    added = set()

    while True:
        for p in processes:
            if p.arrival <= time and p.pid not in added:
                queue.append(p)
                added.add(p.pid)

        if not queue:
            if all(p.remaining == 0 for p in processes):
                break
            next_arr = min(p.arrival for p in processes if p.pid not in added)
            gantt.append(("idle", time, next_arr))
            time = next_arr
            continue

        cur = queue.popleft()

        if cur.start is None:
            cur.start = time

        run = min(cur.remaining, quantum)
        gantt.append((cur.pid, time, time+run))
        time += run
        cur.remaining -= run

        for p in processes:
            if p.arrival <= time and p.pid not in added:
                queue.append(p)
                added.add(p.pid)

        if cur.remaining > 0:
            queue.append(cur)
        else:
            cur.completion = time
            cur.turnaround = time - cur.arrival
            cur.waiting = cur.turnaround - cur.burst

    return gantt

# ---------------- Main Function ----------------
def main():
    print("CPU Scheduling Simulator")

    n = int(input("Enter number of processes: "))
    procs = []
    for i in range(n):
        pid = f"P{i+1}"
        at = int(input(f"Arrival time for {pid} (default 0): ") or 0)
        bt = int(input(f"Burst time for {pid}: "))
        procs.append(Process(pid, at, bt))

    quantum = int(input("Enter quantum for Round Robin: "))

    # FCFS
    print("\n===== FCFS =====")
    reset(procs)
    g = fcfs(procs)
    print_table(procs)
    print_gantt(g)

    # SJF Non-preemptive
    print("\n===== SJF (Non-Preemptive) =====")
    reset(procs)
    g = sjf_non_preemptive(procs)
    print_table(procs)
    print_gantt(g)

    # SRTF
    print("\n===== SJF (Preemptive - SRTF) =====")
    reset(procs)
    g = sjf_preemptive(procs)
    print_table(procs)
    print_gantt(g)

    # Round Robin
    print("\n===== ROUND ROBIN =====")
    reset(procs)
    g = round_robin(procs, quantum)
    print_table(procs)
    print_gantt(g)

def run():
    main()

if __name__ == "__main__":
    main()
