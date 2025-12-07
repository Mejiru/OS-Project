import cpu_schedule  # Hatem
import BankersAlgorithm  # Mohammad and Ahmad
import part3  # Irfan
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_main_menu():
    print("\n" + "=" * 50)
    print("              OS Simulator              ")
    print("=" * 50)
    print("[1] CPU Scheduling Algorithms")
    print("[2] Banker's Algorithm")
    print("[3] Page Replacement Algorithms")
    print("[0] Exit")
    print("=" * 50)


def show_cpu_scheduling_menu():
    print("\n" + "=" * 50)
    print("        CPU Scheduling Algorithms        ")
    print("=" * 50)
    print("[1] First Come First Serve (FCFS)")
    print("[2] Shortest Job First - Non-Preemptive (SJF)")
    print("[3] Shortest Remaining Time First - Preemptive (SRTF)")
    print("[4] Round Robin (RR)")
    print("[0] Return to Main Menu")
    print("=" * 50)


def show_page_replacement_menu():
    print("\n" + "=" * 50)
    print("      Page Replacement Algorithms       ")
    print("=" * 50)
    print("[1] First In First Out (FIFO)")
    print("[2] Least Recently Used (LRU)")
    print("[3] Optimal Page Replacement")
    print("[0] Return to Main Menu")
    print("=" * 50)


def cpu_scheduling_handler():
    print("\n" + "=" * 50)
    print("          CPU Scheduling Simulator          ")
    print("=" * 50)
    n = int(input("Enter number of processes: "))
    procs = []
    for i in range(n):
        pid = f"P{i+1}"
        at = int(input(f"Arrival time for {pid} (default 0): ") or 0)
        bt = int(input(f"Burst time for {pid}: "))
        procs.append(cpu_schedule.Process(pid, at, bt))
    
    quantum = None
    
    while True:
        show_cpu_scheduling_menu()
        choice = input("Select an algorithm: ").strip()
        
        if choice == "0":
            break
            
        elif choice == "1":
            cpu_schedule.reset(procs)
            print("\n" + "=" * 50)
            print("          First Come First Serve (FCFS)          ")
            print("=" * 50)
            g = cpu_schedule.fcfs(procs)
            cpu_schedule.print_table(procs)
            cpu_schedule.print_gantt(g)
            
        elif choice == "2":
            cpu_schedule.reset(procs)
            print("\n" + "=" * 50)
            print("     Shortest Job First - Non-Preemptive (SJF)     ")
            print("=" * 50)
            g = cpu_schedule.sjf_non_preemptive(procs)
            cpu_schedule.print_table(procs)
            cpu_schedule.print_gantt(g)
            
        elif choice == "3":
            cpu_schedule.reset(procs)
            print("\n" + "=" * 50)
            print("  Shortest Remaining Time First - Preemptive (SRTF)  ")
            print("=" * 50)
            g = cpu_schedule.sjf_preemptive(procs)
            cpu_schedule.print_table(procs)
            cpu_schedule.print_gantt(g)
            
        elif choice == "4":
            if quantum is None:
                quantum = int(input("Enter quantum for Round Robin: "))
            cpu_schedule.reset(procs)
            print("\n" + "=" * 50)
            print("          Round Robin (RR)          ")
            print("=" * 50)
            g = cpu_schedule.round_robin(procs, quantum)
            cpu_schedule.print_table(procs)
            cpu_schedule.print_gantt(g)
            
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")
            continue
        
        # After running algorithm, show options
        print("\n" + "=" * 50)
        print("Options:")
        print("[1] Try Another Algorithm")
        print("[2] Reset & Enter New Processes")
        print("[0] Return to Main Menu")
        print("=" * 50)
        
        next_action = input("Choose an option: ").strip()
        
        if next_action == "1":
            continue
        elif next_action == "2":
            clear_screen()
            print("\n" + "=" * 50)
            print("          CPU Scheduling Simulator          ")
            print("=" * 50)
            n = int(input("Enter number of processes: "))
            procs = []
            for i in range(n):
                pid = f"P{i+1}"
                at = int(input(f"Arrival time for {pid} (default 0): ") or 0)
                bt = int(input(f"Burst time for {pid}: "))
                procs.append(cpu_schedule.Process(pid, at, bt))
            quantum = None
            continue
        elif next_action == "0":
            break
        else:
            print("\nInvalid option. Returning to algorithm menu...")
            continue


def page_replacement_handler():
    print("\n" + "=" * 50)
    print("      Page Replacement Algorithms       ")
    print("=" * 50)
    reference = list(map(int, input("Please enter the reference string separated by space: ").split()))
    frame_size = int(input("Enter frame size: "))
    
    while True:
        show_page_replacement_menu()
        choice = input("Select an algorithm: ").strip()
        
        if choice == "0":
            break
            
        elif choice == "1":
            print("\n" + "=" * 50)
            print("          First In First Out (FIFO)          ")
            print("=" * 50)
            print("Reference:", reference)
            part3.run_FIFO(reference, frame_size)
            
        elif choice == "2":
            print("\n" + "=" * 50)
            print("       Least Recently Used (LRU)        ")
            print("=" * 50)
            print("Reference:", reference)
            part3.run_LRU(reference, frame_size)
            
        elif choice == "3":
            print("\n" + "=" * 50)
            print("      Optimal Page Replacement       ")
            print("=" * 50)
            print("Reference:", reference)
            part3.run_optimal(reference, frame_size)
            
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")
            continue
        
        print("\n" + "=" * 50)
        print("Options:")
        print("[1] Try Another Algorithm")
        print("[2] Reset & Enter New Data")
        print("[0] Return to Main Menu")
        print("=" * 50)
        
        next_action = input("Choose an option: ").strip()
        
        if next_action == "1":
            continue
        elif next_action == "2":
            clear_screen()
            print("\n" + "=" * 50)
            print("      Page Replacement Algorithms       ")
            print("=" * 50)
            reference = list(map(int, input("Please enter the reference string separated by space: ").split()))
            frame_size = int(input("Enter frame size: "))
            continue
        elif next_action == "0":
            break
        else:
            print("\nInvalid option. Returning to algorithm menu...")
            continue


def show_menu():
    while True:
        clear_screen()
        show_main_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            clear_screen()
            cpu_scheduling_handler()
            input("\nPress Enter to return to main menu...")

        elif choice == "2":
            clear_screen()
            print("\n" + "=" * 50)
            print("          Banker's Algorithm          ")
            print("=" * 50)
            algo = BankersAlgorithm.BankersAlgorithm()
            algo.run()
            input("\nPress Enter to return to main menu...")

        elif choice == "3":
            clear_screen()
            page_replacement_handler()
            input("\nPress Enter to return to main menu...")

        elif choice == "0":
            print("\nExiting program...")
            break

        else:
            print("\nInvalid input, try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        from gui_app import main as gui_main
        gui_main()
    else:
        show_menu()
