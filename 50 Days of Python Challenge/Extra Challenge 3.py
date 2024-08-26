import time

a = range(100000)
x = set(a)
y = list(a)
num = 99999

start_time = time.time()
for i in x:
    if num == i:
        break
end_time = time.time()
elapsed_time_1 = end_time - start_time


start_time = time.time()
for i in y:
    if num == i:
        break
end_time = time.time()
elapsed_time_2 = end_time - start_time

# Print the elapsed time for each search
print("Elapsed time for search 1:", elapsed_time_1)
print("Elapsed time for search 2:", elapsed_time_2)

import time

a = range(1000000)
x = set(a)
y = list(a)
num = 999999

def measure_time(iterable, target):
    start_time = time.perf_counter()  # Use high-resolution timer
    for i in iterable:
        if num == i:
            break
    end_time = time.perf_counter()
    print(f"iteration {iterable}")
    return end_time - start_time

# Run multiple trials and take the average
trials = 1000
elapsed_time_1 = sum(measure_time(x, num) for _ in range(trials)) / trials
elapsed_time_2 = sum(measure_time(y, num) for _ in range(trials)) / trials

# Print the average elapsed time for each search
print("Average elapsed time for search 1 (set):", elapsed_time_1)
print("Average elapsed time for search 2 (list):", elapsed_time_2)
