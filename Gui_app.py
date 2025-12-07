import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import cpu_schedule
import part3
import BankersAlgorithm
import io
import sys

class OSSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Simulator Project")
        self.root.geometry("1200x850") 
        self.root.configure(bg="#f0f0f0")
        
     
        self.selected_algorithm = tk.StringVar(value="First Come First Serve, FCFS")
        self.arrival_times = tk.StringVar()
        self.burst_times = tk.StringVar()
        self.quantum = tk.StringVar()
        self.reference_string = tk.StringVar()
        self.frame_size = tk.StringVar()
        
       
        self.banker_resources = tk.StringVar() 
        self.request_process_id = tk.StringVar()
        self.request_vector = tk.StringVar()
        
       
        self.banker_instance = None 
        
        self.setup_ui()
    
    def setup_ui(self):
       
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
       
        input_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(input_frame, text="Configuration", font=("Arial", 16, "bold"), bg="white").pack(pady=(20, 15))
        
       
        tk.Label(input_frame, text="Select Algorithm:", font=("Arial", 11, "bold"), bg="white", anchor="w").pack(fill=tk.X, padx=20)
        self.algo_combo = ttk.Combobox(input_frame, textvariable=self.selected_algorithm, state="readonly", width=30)
        self.algo_combo['values'] = (
            "First Come First Serve, FCFS",
            "Shortest Job First - Non-Preemptive, SJF",
            "Shortest Remaining Time First - Preemptive, SRTF",
            "Round Robin, RR",
            "First In First Out, FIFO",
            "Least Recently Used, LRU",
            "Optimal Page Replacement",
            "Banker's Algorithm"
        )
        self.algo_combo.pack(fill=tk.X, padx=20, pady=(5, 20))
        self.algo_combo.bind("<<ComboboxSelected>>", self.on_algorithm_change)
        
       
        self.dynamic_frame = tk.Frame(input_frame, bg="white")
        self.dynamic_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
       
        self.cpu_frame = tk.Frame(self.dynamic_frame, bg="white")
        tk.Label(self.cpu_frame, text="Arrival Times (space separated):", bg="white", anchor="w").pack(fill=tk.X)
        self.entry_arrival = tk.Entry(self.cpu_frame, textvariable=self.arrival_times)
        self.entry_arrival.pack(fill=tk.X, pady=(0, 10))
        self.entry_arrival.insert(0, "0 2 4 6 8")
        
        tk.Label(self.cpu_frame, text="Burst Times (space separated):", bg="white", anchor="w").pack(fill=tk.X)
        self.entry_burst = tk.Entry(self.cpu_frame, textvariable=self.burst_times)
        self.entry_burst.pack(fill=tk.X, pady=(0, 10))
        self.entry_burst.insert(0, "2 4 6 8 10")
        
        self.lbl_quantum = tk.Label(self.cpu_frame, text="Quantum (Round Robin only):", bg="white", anchor="w")
        self.entry_quantum = tk.Entry(self.cpu_frame, textvariable=self.quantum)
        
        self.mem_frame = tk.Frame(self.dynamic_frame, bg="white")
        tk.Label(self.mem_frame, text="Reference String (space separated):", bg="white", anchor="w").pack(fill=tk.X)
        tk.Entry(self.mem_frame, textvariable=self.reference_string).pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(self.mem_frame, text="Frame Size (integer):", bg="white", anchor="w").pack(fill=tk.X)
        tk.Entry(self.mem_frame, textvariable=self.frame_size).pack(fill=tk.X, pady=(0, 10))

        
        self.banker_frame = tk.Frame(self.dynamic_frame, bg="white")
        
        tk.Label(self.banker_frame, text="Available Resources Vector (Resource Types determined by length):", font=("Arial", 10, "bold"), bg="white", anchor="w").pack(fill=tk.X)
        tk.Label(self.banker_frame, text="Example (3 resource types): 3 3 2", font=("Arial", 8), fg="gray", bg="white", anchor="w").pack(fill=tk.X)
        self.entry_banker_resources = tk.Entry(self.banker_frame, textvariable=self.banker_resources)
        self.entry_banker_resources.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(self.banker_frame, text="Allocation Matrix (Processes determined by rows/lines):", font=("Arial", 10, "bold"), bg="white", anchor="w").pack(fill=tk.X)
        tk.Label(self.banker_frame, text="Enter each process on a new line or separate by ';'", font=("Arial", 8), fg="gray", bg="white", anchor="w").pack(fill=tk.X)
        self.text_banker_alloc = scrolledtext.ScrolledText(self.banker_frame, height=4, width=30)
        self.text_banker_alloc.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(self.banker_frame, text="Max Matrix (Must have same number of rows as Allocation):", font=("Arial", 10, "bold"), bg="white", anchor="w").pack(fill=tk.X)
        self.text_banker_max = scrolledtext.ScrolledText(self.banker_frame, height=4, width=30)
        self.text_banker_max.pack(fill=tk.X, pady=(0, 10))

       
        self.request_frame = tk.LabelFrame(self.banker_frame, text="Resource Request Simulation (Run SOLVE first)", bg="white", padx=10, pady=10)
        
        tk.Label(self.request_frame, text="Process ID (e.g., 0, 1, 2...):", bg="white", anchor="w").pack(fill=tk.X, pady=(5, 0))
        tk.Entry(self.request_frame, textvariable=self.request_process_id).pack(fill=tk.X, pady=(0, 5))

        tk.Label(self.request_frame, text="Request Vector (e.g., 1 0 1):", bg="white", anchor="w").pack(fill=tk.X, pady=(5, 0))
        tk.Entry(self.request_frame, textvariable=self.request_vector).pack(fill=tk.X, pady=(0, 10))

        tk.Button(self.request_frame, text="MAKE REQUEST", font=("Arial", 10, "bold"), bg="#ffc107", fg="black", 
                 command=self.make_banker_request, relief=tk.FLAT, pady=5).pack(fill=tk.X)
      

       
        btn_frame = tk.Frame(input_frame, bg="white")
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)
        
        tk.Button(btn_frame, text="SOLVE INITIAL STATE", font=("Arial", 12, "bold"), bg="#007bff", fg="white", 
                 command=self.solve, relief=tk.FLAT, pady=10).pack(fill=tk.X, pady=(0, 10))
                 
        tk.Button(btn_frame, text="RESET", font=("Arial", 12), bg="#6c757d", fg="white", 
                 command=self.reset, relief=tk.FLAT, pady=5).pack(fill=tk.X)

      
        output_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(output_frame, text="Simulation Output", font=("Arial", 16, "bold"), bg="white").pack(pady=(20, 10))
        
        self.output_text = scrolledtext.ScrolledText(output_frame, font=("Consolas", 10), state=tk.DISABLED, padx=10, pady=10)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        
        self.on_algorithm_change()

    def on_algorithm_change(self, event=None):
        
        algo = self.selected_algorithm.get()
        
       
        self.cpu_frame.pack_forget()
        self.mem_frame.pack_forget()
        self.banker_frame.pack_forget()
        self.lbl_quantum.pack_forget()
        self.entry_quantum.pack_forget()
        self.request_frame.pack_forget()
        self.banker_instance = None 
        
      
        if "FCFS" in algo or "SJF" in algo or "SRTF" in algo or "Round Robin" in algo:
            self.cpu_frame.pack(fill=tk.BOTH, expand=True)
            if "Round Robin" in algo:
                self.lbl_quantum.pack(fill=tk.X, pady=(5,0))
                self.entry_quantum.pack(fill=tk.X, pady=(0,10))
                
        elif "FIFO" in algo or "LRU" in algo or "Optimal" in algo:
            self.mem_frame.pack(fill=tk.BOTH, expand=True)
            
        elif "Banker" in algo:
            self.banker_frame.pack(fill=tk.BOTH, expand=True)


    def write_output(self, text, append=False):
        self.output_text.config(state=tk.NORMAL)
        if not append:
            self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state=tk.DISABLED)

    def solve(self):
        algo = self.selected_algorithm.get()
        try:
            if "FCFS" in algo or "SJF" in algo or "SRTF" in algo or "Round Robin" in algo:
                self.solve_cpu(algo)
            elif "FIFO" in algo or "LRU" in algo or "Optimal" in algo:
                self.solve_memory(algo)
            elif "Banker" in algo:
                self.solve_banker()
        except Exception as e:
            self.write_output(f"Error occurred:\n{str(e)}\n\nPlease check your inputs.")

    def solve_cpu(self, algo):
        # ... (CPU scheduling logic remains the same) ...
        arr_str = self.arrival_times.get().strip() or "0"
        burst_str = self.burst_times.get().strip()
        
        if not burst_str:
            messagebox.showwarning("Input Error", "Burst times are required.")
            return

        arrivals = list(map(int, arr_str.split()))
        bursts = list(map(int, burst_str.split()))
        
        if len(arrivals) == 1 and len(bursts) > 1:
            arrivals = [arrivals[0]] * len(bursts)
            
        if len(arrivals) != len(bursts):
            messagebox.showerror("Input Error", "Count of Arrival times and Burst times must match.")
            return

        processes = []
        for i in range(len(bursts)):
            processes.append(cpu_schedule.Process(f"P{i+1}", arrivals[i], bursts[i]))
        
        cpu_schedule.reset(processes)
        
        gantt = []
        algo_name = ""
        
        if "FCFS" in algo:
            gantt = cpu_schedule.fcfs(processes)
            algo_name = "First Come First Serve"
        elif "SJF" in algo and "Non-Preemptive" in algo:
            gantt = cpu_schedule.sjf_non_preemptive(processes)
            algo_name = "SJF Non-Preemptive"
        elif "SRTF" in algo or "Preemptive" in algo:
            gantt = cpu_schedule.sjf_preemptive(processes)
            algo_name = "SRTF Preemptive"
        elif "Round Robin" in algo:
            q = self.quantum.get()
            if not q:
                messagebox.showerror("Input Error", "Quantum is required for Round Robin.")
                return
            gantt = cpu_schedule.round_robin(processes, int(q))
            algo_name = f"Round Robin (Q={q})"

        output = f"=== {algo_name} ===\n\n"
        output += "PID | Arr | Burst | Start | End | Wait | Turnaround\n"
        output += "-"*60 + "\n"
        
        avg_wait = 0
        avg_turn = 0
        
        for p in processes:
            output += f"{p.pid:3} | {p.arrival:3} | {p.burst:5} | {str(p.start):5} | {str(p.completion):3} | {str(p.waiting):4} | {str(p.turnaround):10}\n"
            if p.waiting is not None: avg_wait += p.waiting
            if p.turnaround is not None: avg_turn += p.turnaround
            
        if processes:
            avg_wait /= len(processes)
            avg_turn /= len(processes)
            
        output += "-"*60 + "\n"
        output += f"Average Waiting Time: {avg_wait:.2f}\n"
        output += f"Average Turnaround Time: {avg_turn:.2f}\n\n"
        
        output += "Gantt Chart Execution Sequence:\n"
        for item in gantt:
            output += f"[{item[1]} -> {item[2]}]: {item[0]}\n"
            
        self.write_output(output)

    def solve_memory(self, algo):
       
        ref_str = self.reference_string.get()
        frame_str = self.frame_size.get()
        
        if not ref_str or not frame_str:
            messagebox.showwarning("Input Error", "Please provide Reference String and Frame Size.")
            return
            
        reference = list(map(int, ref_str.split()))
        f_size = int(frame_str)
        
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        if "FIFO" in algo:
            part3.run_FIFO(reference, f_size)
        elif "LRU" in algo:
            part3.run_LRU(reference, f_size)
        elif "Optimal" in algo:
            part3.run_optimal(reference, f_size)
            
        sys.stdout = old_stdout
        self.write_output(buffer.getvalue())

    def solve_banker(self):
       
        avail_str = self.banker_resources.get().strip()
        alloc_str = self.text_banker_alloc.get('1.0', tk.END).strip()
        max_str = self.text_banker_max.get('1.0', tk.END).strip()
        
        if not avail_str or not alloc_str or not max_str:
            messagebox.showwarning("Input Error", "Please fill all Banker's Algorithm fields.")
            return

     
        self.banker_instance = BankersAlgorithm.BankersAlgorithm()
        ba = self.banker_instance 
        
        try:
           
            ba.available = list(map(int, avail_str.split()))
            ba.num_resources = len(ba.available)
            
          
            alloc_str = alloc_str.replace('\n', ';')
            rows_alloc = [r.strip() for r in alloc_str.split(';') if r.strip()]
            ba.allocation = [list(map(int, r.split())) for r in rows_alloc]
            ba.num_processes = len(ba.allocation)
            
          
            max_str = max_str.replace('\n', ';')
            rows_max = [r.strip() for r in max_str.split(';') if r.strip()]
            ba.max_demand = [list(map(int, r.split())) for r in rows_max]

        except ValueError:
             raise ValueError("Matrix data contains non-integer or poorly formatted values.")
        
      
        if len(ba.max_demand) != ba.num_processes:
            raise ValueError(f"Max Matrix rows ({len(ba.max_demand)}) must match Allocation Matrix rows ({ba.num_processes}).")
        if any(len(row) != ba.num_resources for row in ba.allocation) or \
           any(len(row) != ba.num_resources for row in ba.max_demand):
            raise ValueError("All matrix rows must match the number of resources defined by the Available vector.")
        
        ba.calculate_need()
        is_safe, sequence = ba.is_safe_state()
        
       
        output = "=== Banker's Algorithm Initial State Results ===\n\n"
        output += f"Calculated Resource Types (m): {ba.num_resources}\n"
        output += f"Calculated Number of Processes (n): {ba.num_processes}\n"
        output += "-"*40 + "\n\n"
        
        output += "Current System State:\n"
        output += f"Available Resources: {ba.available}\n\n"

        output += "Calculated Need Matrix (Max - Allocation):\n"
        for i, row in enumerate(ba.need):
            output += f"P{i}: {row}\n"
        output += "\n"
        
        if is_safe:
            output += "RESULT: System is in a SAFE STATE. ✅\n"
            output += f"Safe Sequence: <{', '.join([f'P{i}' for i in sequence])}>\n"
        else:
            output += "RESULT: System is in an UNSAFE STATE. ❌\n"
            output += "Deadlock is possible.\n"
        
        self.write_output(output)
        
       
        self.request_frame.pack(fill=tk.X, padx=10, pady=(15, 0))
        self.request_frame.config(text=f"Resource Request Simulation (Processes 0 to {ba.num_processes - 1})")


    def make_banker_request(self):
        if not self.banker_instance:
            messagebox.showerror("Error", "Please run 'SOLVE INITIAL STATE' first.")
            return

        try:
            pid = int(self.request_process_id.get().strip())
            request = list(map(int, self.request_vector.get().strip().split()))
        except ValueError:
            messagebox.showerror("Input Error", "Invalid Process ID or Request Vector format.")
            return

        ba = self.banker_instance
        
       
        if not (0 <= pid < ba.num_processes):
            messagebox.showerror("Input Error", f"Process ID must be between 0 and {ba.num_processes - 1}.")
            return
        if len(request) != ba.num_resources:
            messagebox.showerror("Input Error", f"Request vector must have {ba.num_resources} resource values.")
            return

       
        success, message = ba.request_resources(pid, request)

        request_output = f"\n\n=== Resource Request: P{pid} requests {request} ===\n"
        request_output += f"Result: {message}\n"
        
        if success:
            request_output += "Request granted. System state updated.\n"
            is_safe, sequence = ba.is_safe_state()
            request_output += f"New Available Resources: {ba.available}\n"
            request_output += f"System remains in SAFE STATE. ✅\n"
            request_output += f"New Safe Sequence: <{', '.join([f'P{i}' for i in sequence])}>\n"
        else:
            request_output += "Request denied. System state remains unchanged.\n"
            
        self.write_output(request_output, append=True)
       
        self.request_process_id.set("")
        self.request_vector.set("")


    def reset(self):
     
        self.arrival_times.set("0 2 4 6 8")
        self.burst_times.set("2 4 6 8 10")
        self.quantum.set("")
        self.reference_string.set("")
        self.frame_size.set("")
        self.banker_resources.set("")
        self.request_process_id.set("")
        self.request_vector.set("")
        
     
        self.text_banker_alloc.delete('1.0', tk.END)
        self.text_banker_max.delete('1.0', tk.END)
        
        
        self.request_frame.pack_forget()
        self.banker_instance = None
        
        self.write_output("Ready.")

def main():
    root = tk.Tk()
    app = OSSimulatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
