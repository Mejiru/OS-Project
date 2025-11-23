class BankersAlgorithm:
    def __init__(self):
        self.num_processes = 0
        self.num_resources = 0
        self.available = []
        self.max_demand = []
        self.allocation = []
        self.need = []
    
    def input_data(self):
        self.num_processes = int(input("Enter number of processes: "))
        self.num_resources = int(input("Enter number of resource types: "))
        
        print("\nEnter available resources vector:")
        self.available = [int(x) for x in input().split()]
        
        print("\nEnter Max Matrix (row by row):")
        self.max_demand = []
        for i in range(self.num_processes):
            row = [int(x) for x in input(f"Process {i}: ").split()]
            self.max_demand.append(row)
        
        print("\nEnter Allocation Matrix (row by row):")
        self.allocation = []
        for i in range(self.num_processes):
            row = [int(x) for x in input(f"Process {i}: ").split()]
            self.allocation.append(row)
        
        # Calculate Need Matrix
        self.calculate_need()
    
    def calculate_need(self):
        self.need = []
        for i in range(self.num_processes):
            row = []
            for j in range(self.num_resources):
                row.append(self.max_demand[i][j] - self.allocation[i][j])
            self.need.append(row)
    
    def is_safe_state(self):
        work = self.available.copy()
        finish = [False] * self.num_processes
        safe_sequence = []
        
        while len(safe_sequence) < self.num_processes:
            found = False
            for i in range(self.num_processes):
                if not finish[i]:
                    # Check if need[i] <= work
                    can_allocate = True
                    for j in range(self.num_resources):
                        if self.need[i][j] > work[j]:
                            can_allocate = False
                            break
                    
                    if can_allocate:
                        # Simulate resource allocation
                        for j in range(self.num_resources):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
                        safe_sequence.append(i)
                        found = True
            
            if not found:
                return False, []  # Unsafe state
        
        return True, safe_sequence
    
    def request_resources(self, process_id, request):
        # Check if request <= need
        for j in range(self.num_resources):
            if request[j] > self.need[process_id][j]:
                return False, "Error: Request exceeds maximum claim"
        
        # Check if request <= available
        for j in range(self.num_resources):
            if request[j] > self.available[j]:
                return False, "Error: Resources not available"
        
        # Try to allocate resources temporarily
        old_available = self.available.copy()
        old_allocation = [row.copy() for row in self.allocation]
        old_need = [row.copy() for row in self.need]
        
        for j in range(self.num_resources):
            self.available[j] -= request[j]
            self.allocation[process_id][j] += request[j]
            self.need[process_id][j] -= request[j]
        
        # Check if system is in safe state
        is_safe, sequence = self.is_safe_state()
        
        if not is_safe:
            # Revert changes
            self.available = old_available
            self.allocation = old_allocation
            self.need = old_need
            return False, "System would be in unsafe state"
        
        return True, "Request granted"
    
    def display_matrices(self):
        print("\nAllocation Matrix:")
        for row in self.allocation:
            print(row)
        
        print("\nMax Matrix:")
        for row in self.max_demand:
            print(row)
        
        print("\nNeed Matrix:")
        for row in self.need:
            print(row)
        
        print("\nAvailable Resources:")
        print(self.available)
