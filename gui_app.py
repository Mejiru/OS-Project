import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import cpu_schedule
import part3
import BankersAlgorithm


class OSSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Simulator")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        self.selected_algorithm = tk.StringVar(value="First Come First Serve, FCFS")
        self.arrival_times = tk.StringVar()
        self.burst_times = tk.StringVar()
        self.quantum = tk.StringVar()
        self.reference_string = tk.StringVar()
        self.frame_size = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        input_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        input_title = tk.Label(input_frame, text="Input", font=("Arial", 18, "bold"), bg="white")
        input_title.pack(pady=(20, 30))
        
        algo_label = tk.Label(input_frame, text="Algorithm", font=("Arial", 12), bg="white", anchor="w")
        algo_label.pack(fill=tk.X, padx=20, pady=(0, 5))
        
        self.algo_combo = ttk.Combobox(input_frame, textvariable=self.selected_algorithm, 
                                      state="readonly", font=("Arial", 11), width=30)
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
        self.algo_combo.pack(fill=tk.X, padx=20, pady=(0, 20))
        self.algo_combo.bind("<<ComboboxSelected>>", self.on_algorithm_change)
        
        self.arrival_label = tk.Label(input_frame, text="Arrival Times", font=("Arial", 12), bg="white", anchor="w")
        self.arrival_label.pack(fill=tk.X, padx=20, pady=(0, 5))
        
        self.arrival_entry = tk.Entry(input_frame, textvariable=self.arrival_times, font=("Arial", 11))
        self.arrival_entry.pack(fill=tk.X, padx=20, pady=(0, 20))
        self.arrival_entry.insert(0, "e.g. 0 2 4 6 8")
        self.arrival_entry.config(fg="gray")
        self.arrival_entry.bind("<FocusIn>", self.clear_placeholder)
        self.arrival_entry.bind("<FocusOut>", self.restore_placeholder)
        
        self.burst_label = tk.Label(input_frame, text="Burst Times", font=("Arial", 12), bg="white", anchor="w")
        self.burst_label.pack(fill=tk.X, padx=20, pady=(0, 5))
        
        self.burst_entry = tk.Entry(input_frame, textvariable=self.burst_times, font=("Arial", 11))
        self.burst_entry.pack(fill=tk.X, padx=20, pady=(0, 20))
        self.burst_entry.insert(0, "e.g. 2 4 6 8 10")
        self.burst_entry.config(fg="gray")
        self.burst_entry.bind("<FocusIn>", self.clear_placeholder_burst)
        self.burst_entry.bind("<FocusOut>", self.restore_placeholder_burst)
        
        self.quantum_label = tk.Label(input_frame, text="Quantum (for Round Robin)", font=("Arial", 12), bg="white", anchor="w")
        self.quantum_label.pack(fill=tk.X, padx=20, pady=(0, 5))
        self.quantum_label.pack_forget()
        
        self.quantum_entry = tk.Entry(input_frame, textvariable=self.quantum, font=("Arial", 11))
        self.quantum_entry.pack(fill=tk.X, padx=20, pady=(0, 20))
        self.quantum_entry.pack_forget()
        
        self.ref_label = tk.Label(input_frame, text="Reference String", font=("Arial", 12), bg="white", anchor="w")
        self.ref_label.pack_forget()
        
        self.ref_entry = tk.Entry(input_frame, textvariable=self.reference_string, font=("Arial", 11))
        self.ref_entry.pack_forget()
        
        self.frame_label = tk.Label(input_frame, text="Frame Size", font=("Arial", 12), bg="white", anchor="w")
        self.frame_label.pack_forget()
        
        self.frame_entry = tk.Entry(input_frame, textvariable=self.frame_size, font=("Arial", 11))
        self.frame_entry.pack_forget()
        
        button_frame = tk.Frame(input_frame, bg="white")
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        solve_btn = tk.Button(button_frame, text="Solve", font=("Arial", 12, "bold"), 
                             bg="#007bff", fg="white", command=self.solve, 
                             relief=tk.FLAT, padx=20, pady=10, cursor="hand2")
        solve_btn.pack(fill=tk.X, pady=(0, 10))
        
        reset_btn = tk.Button(button_frame, text="Reset", font=("Arial", 12), 
                             bg="#6c757d", fg="white", command=self.reset, 
                             relief=tk.FLAT, padx=20, pady=10, cursor="hand2")
        reset_btn.pack(fill=tk.X)
        
        output_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        output_title = tk.Label(output_frame, text="Output", font=("Arial", 18, "bold"), bg="white")
        output_title.pack(pady=(20, 10))
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                                     font=("Consolas", 10), 
                                                     bg="white", fg="black",
                                                     relief=tk.FLAT, padx=10, pady=10)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.output_text.insert("1.0", "Gantt chart and table will be shown here")
        self.output_text.config(state=tk.DISABLED)
        
        self.on_algorithm_change()
    
    def clear_placeholder(self, event):
        if self.arrival_entry.get() == "e.g. 0 2 4 6 8":
            self.arrival_entry.delete(0, tk.END)
            self.arrival_entry.config(fg="black")
    
    def restore_placeholder(self, event):
        if not self.arrival_entry.get():
            self.arrival_entry.insert(0, "e.g. 0 2 4 6 8")
            self.arrival_entry.config(fg="gray")
    
    def clear_placeholder_burst(self, event):
        if self.burst_entry.get() == "e.g. 2 4 6 8 10":
            self.burst_entry.delete(0, tk.END)
            self.burst_entry.config(fg="black")
    
    def restore_placeholder_burst(self, event):
        if not self.burst_entry.get():
            self.burst_entry.insert(0, "e.g. 2 4 6 8 10")
            self.burst_entry.config(fg="gray")
    
    def on_algorithm_change(self, event=None):
        algo = self.selected_algorithm.get()
        
        self.arrival_label.pack_forget()
        self.arrival_entry.pack_forget()
        self.burst_label.pack_forget()
        self.burst_entry.pack_forget()
        self.quantum_label.pack_forget()
        self.quantum_entry.pack_forget()
        self.ref_label.pack_forget()
        self.ref_entry.pack_forget()
        self.frame_label.pack_forget()
        self.frame_entry.pack_forget()
        
        if "FCFS" in algo or "SJF" in algo or "SRTF" in algo or "Round Robin" in algo:
            self.arrival_label.pack(fill=tk.X, padx=20, pady=(0, 5))
            self.arrival_entry.pack(fill=tk.X, padx=20, pady=(0, 20))
            self.burst_label.pack(fill=tk.X, padx=20, pady=(0, 5))
            self.burst_entry.pack(fill=tk.X, padx=20, pady=(0, 20))
            
            if "Round Robin" in algo:
                self.quantum_label.pack(fill=tk.X, padx=20, pady=(0, 5))
                self.quantum_entry.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        elif "FIFO" in algo or "LRU" in algo or "Optimal" in algo:
            self.ref_label.config(text="Reference String")
            self.ref_label.pack(fill=tk.X, padx=20, pady=(0, 5))
            self.ref_entry.pack(fill=tk.X, padx=20, pady=(0, 20))
            self.frame_label.pack(fill=tk.X, padx=20, pady=(0, 5))
            self.frame_entry.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        elif "Banker" in algo:
            pass
    
    def solve(self):
        algo = self.selected_algorithm.get()
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        
        try:
            if "FCFS" in algo or "SJF" in algo or "SRTF" in algo or "Round Robin" in algo:
                self.solve_cpu_scheduling(algo)
            elif "FIFO" in algo or "LRU" in algo or "Optimal" in algo:
                self.solve_page_replacement(algo)
            elif "Banker" in algo:
                messagebox.showinfo("Info", "Banker's Algorithm requires interactive input.\nPlease use the console version.")
                self.output_text.insert("1.0", "Banker's Algorithm requires interactive input.\nPlease use the console version.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.output_text.insert("1.0", f"Error: {str(e)}")
        
        self.output_text.config(state=tk.DISABLED)
    
    def solve_cpu_scheduling(self, algo):
        arrival_str = self.arrival_entry.get()
        burst_str = self.burst_entry.get()
        
        if arrival_str == "e.g. 0 2 4 6 8" or not arrival_str:
            arrival_str = "0"
        if burst_str == "e.g. 2 4 6 8 10" or not burst_str:
            messagebox.showerror("Error", "Please enter burst times")
            return
        
        try:
            arrivals = list(map(int, arrival_str.split()))
            bursts = list(map(int, burst_str.split()))
            
            if len(arrivals) != len(bursts):
                if len(arrivals) == 1 and arrivals[0] == 0:
                    arrivals = [0] * len(bursts)
                else:
                    messagebox.showerror("Error", "Arrival times and burst times must have the same count")
                    return
            
            processes = []
            for i in range(len(bursts)):
                pid = f"P{i+1}"
                processes.append(cpu_schedule.Process(pid, arrivals[i], bursts[i]))
            
            cpu_schedule.reset(processes)
            
            if "FCFS" in algo:
                gantt = cpu_schedule.fcfs(processes)
                algo_name = "First Come First Serve (FCFS)"
            elif "SJF" in algo and "Preemptive" not in algo:
                gantt = cpu_schedule.sjf_non_preemptive(processes)
                algo_name = "Shortest Job First - Non-Preemptive (SJF)"
            elif "SRTF" in algo or "Preemptive" in algo:
                gantt = cpu_schedule.sjf_preemptive(processes)
                algo_name = "Shortest Remaining Time First - Preemptive (SRTF)"
            elif "Round Robin" in algo:
                quantum_str = self.quantum_entry.get()
                if not quantum_str:
                    messagebox.showerror("Error", "Please enter quantum for Round Robin")
                    return
                quantum = int(quantum_str)
                gantt = cpu_schedule.round_robin(processes, quantum)
                algo_name = "Round Robin (RR)"
            
            output = f"{'='*60}\n"
            output += f"{algo_name:^60}\n"
            output += f"{'='*60}\n\n"
            
            output += "Process | Arr | Burst | Start | End | Waiting | Turnaround\n"
            output += "-" * 60 + "\n"
            for p in processes:
                output += f"{p.pid:7} {p.arrival:5} {p.burst:7} {str(p.start):6} {str(p.completion):5} {str(p.waiting):8} {str(p.turnaround):11}\n"
            
            avg_w = sum(p.waiting for p in processes) / len(processes)
            avg_t = sum(p.turnaround for p in processes) / len(processes)
            output += "-" * 60 + "\n"
            output += f"Average Waiting Time   = {round(avg_w, 2)}\n"
            output += f"Average Turnaround Time = {round(avg_t, 2)}\n\n"
            
            output += "Gantt Chart:\n"
            bar = ""
            time_line = ""
            
            for pid, s, e in gantt:
                bar += "|" + str(pid).center(5)
                time_line += str(s).ljust(6)
            time_line += str(gantt[-1][2])
            
            output += bar + "|\n"
            output += time_line + "\n"
            
            self.output_text.insert("1.0", output)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers separated by spaces.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def solve_page_replacement(self, algo):
        ref_str = self.ref_entry.get()
        frame_str = self.frame_entry.get()
        
        if not ref_str or not frame_str:
            messagebox.showerror("Error", "Please enter reference string and frame size")
            return
        
        try:
            reference = list(map(int, ref_str.split()))
            frame_size = int(frame_str)
            
            import io
            import sys
            
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            if "FIFO" in algo:
                part3.run_FIFO(reference, frame_size)
                algo_name = "First In First Out (FIFO)"
            elif "LRU" in algo:
                part3.run_LRU(reference, frame_size)
                algo_name = "Least Recently Used (LRU)"
            elif "Optimal" in algo:
                part3.run_optimal(reference, frame_size)
                algo_name = "Optimal Page Replacement"
            
            sys.stdout = old_stdout
            output = buffer.getvalue()
            
            formatted_output = f"{'='*60}\n"
            formatted_output += f"{algo_name:^60}\n"
            formatted_output += f"{'='*60}\n\n"
            formatted_output += f"Reference String: {reference}\n"
            formatted_output += f"Frame Size: {frame_size}\n\n"
            formatted_output += output
            
            self.output_text.insert("1.0", formatted_output)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def reset(self):
        self.arrival_times.set("")
        self.burst_times.set("")
        self.quantum.set("")
        self.reference_string.set("")
        self.frame_size.set("")
        
        self.arrival_entry.delete(0, tk.END)
        self.arrival_entry.insert(0, "e.g. 0 2 4 6 8")
        self.arrival_entry.config(fg="gray")
        
        self.burst_entry.delete(0, tk.END)
        self.burst_entry.insert(0, "e.g. 2 4 6 8 10")
        self.burst_entry.config(fg="gray")
        
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", "Gantt chart and table will be shown here")
        self.output_text.config(state=tk.DISABLED)
        
        self.selected_algorithm.set("First Come First Serve, FCFS")
        self.on_algorithm_change()


def main():
    root = tk.Tk()
    app = OSSimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

