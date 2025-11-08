def FIFO(processes, frame_size):
    tracker = [["-" for _ in range(frame_size)] for i in range(len(processes))]
    replace = 0
    page_fault = 0
    for i in range(len(processes)):
        process = processes[i]
        if i >= 1:
            tracker[i] = list(tracker[i - 1])
        if process not in tracker[i]:
            page_fault += 1
            tracker[i][replace] = process
            replace = (replace + 1) % frame_size
    print("First In First Out")
    print("Page Faults:", page_fault)
    for i in tracker:
        print(i)


def LRU(processes, frame_size):
    tracker = [["-" for _ in range(frame_size)] for i in range(len(processes))]
    page_fault = 0
    for i in range(len(processes)):
        process = processes[i]
        if i >= 1:
            tracker[i] = list(tracker[i - 1])
        if process not in tracker[i]:
            page_fault += 1
            if "-" in tracker[i]:
                ind = tracker[i].index("-")
                tracker[i][ind] = process
            else:
                recent = list(processes[:i])[::-1]
                ind_to_replace = None
                for p in tracker[i]:
                    temp_index = recent.index(p)
                    if ind_to_replace is None:
                        ind_to_replace = temp_index
                    if temp_index > ind_to_replace:
                        ind_to_replace = temp_index
                element_to_replace = recent[ind_to_replace]
                ind = tracker[i].index(element_to_replace)
                tracker[i][ind] = process
    print("Least Recently Used")
    print("Page Faults:", page_fault)
    for i in tracker:
        print(i)


def optimal(processes, frame_size):
    tracker = [["-" for _ in range(frame_size)] for i in range(len(processes))]
    page_fault = 0
    for i in range(len(processes)):
        process = processes[i]
        if i >= 1:
            tracker[i] = list(tracker[i - 1])
        if process not in tracker[i]:
            page_fault += 1
            if "-" in tracker[i]:
                ind = tracker[i].index("-")
                tracker[i][ind] = process
            else:
                element_to_replace = None
                ind_to_replace = None
                for p in tracker[i]:
                    if p in processes[i + 1:]:
                        temp_ind = processes[i + 1:].index(p)
                        if ind_to_replace is None or temp_ind > ind_to_replace:
                            ind_to_replace = temp_ind
                    else:
                        element_to_replace = p
                if element_to_replace is None:
                    if ind_to_replace is None:
                        element_to_replace = tracker[i][0]
                    else:
                        element_to_replace = processes[i + 1:][ind_to_replace]
                    ind = tracker[i].index(element_to_replace)
                    tracker[i][ind] = process
                else:
                    ind = tracker[i].index(element_to_replace)
                    tracker[i][ind] = process
    print("Optimal Page Replacement")
    print("Page Faults:", page_fault)
    for i in tracker:
        print(i)


import random

if __name__ == "__main__":
    reference = [random.choice([1, 2, 3, 4, 5, 6, 7]) for _ in range(15)]
    frame_size = 4
    print("Reference:", reference)
    FIFO(reference, frame_size)
    print("Reference:", reference)
    LRU(reference, frame_size)
    print("Reference:", reference)
    optimal(reference, frame_size)
