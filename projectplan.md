# OS-Project
Group Project for OS


Week 1 (Nov 1 – Nov 7): CPU Scheduling

Goal: Make the part that handles how processes are scheduled on the CPU.

What to do:

Learn/review how FCFS, SJF (preemptive and non-preemptive), and Round Robin work.

Write a program that:

Takes the number of processes.

Asks for arrival time and burst time for each.

For RR, also asks for the quantum.

Make it calculate:

Waiting time and turnaround time for each process.

Average waiting and turnaround time.

Draw a simple Gantt chart showing order of execution.

Test everything with small examples.

✅ By end of week: All CPU scheduling algorithms working and tested.

🗓️ Week 2 (Nov 8 – Nov 14): Banker’s Algorithm

Goal: Simulate how the system avoids deadlock using resource allocation.

What to do:

Write a program that:

Reads number of processes and resources.

Takes Allocation, Max, and Available matrices as input.

Calculates Need = Max - Allocation.

Check if the system is in a safe state (find safe sequence).

Ask user for a resource request, and check if it can be granted safely.

Print updated matrices if request is accepted.

✅ By end of week: Banker's algorithm working with safe sequence and request check.

🗓️ Week 3 (Nov 15 – Nov 21): Page Replacement

Goal: Simulate how memory handles pages (what stays, what gets replaced).

What to do:

Write three algorithms:

FIFO, Optimal, LRU.

Take frame size and reference string as input.

For each algorithm:

Show page replacements as they happen.

Count page faults, hits, and misses.

Show final hit/miss ratios.

✅ By end of week: All three page replacement algorithms tested and results compared.

🗓️ Week 4 (Nov 22 – Nov 28): Combine & Report

Goal: Put everything together and write your report.

What to do:

Make a main menu like:
