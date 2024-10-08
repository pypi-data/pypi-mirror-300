import concurrent.futures
import os
from functools import wraps 

def make_parallel(func):
    @wraps(func)
    def wrapper(lst):
        # the number of threads that can be max-spawned.
        # If the number of threads are too high, then the overhead of creating the threads will be significant.
        # Here we are choosing the number of CPUs available in the system and then multiplying it with a constant.
        # In my system, i have a total of 8 CPUs so i will be generating a maximum of 16 threads in my system.
        number_of_threads_multiple = 2 # You can change this multiple according to you requirement
        number_of_workers = int(os.cpu_count() * number_of_threads_multiple)
        if len(lst) < number_of_workers:
            # If the length of the list is low, we would only require those many number of threads.
            # Here we are avoiding creating unnecessary threads
            number_of_workers = len(lst)
        if not number_of_workers:
            return []
        if number_of_workers == 1:
            # If the length of the list that needs to be parallelized is 1, there is no point in
            # parallelizing the function.
            # So we run it serially.
            return [func(lst[0])]
        # Core Code, where we are creating max number of threads and running the decorated function in parallel.
        result = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executer:
            bag = {executer.submit(func, i): i for i in lst}
            for future in concurrent.futures.as_completed(bag):
                result.append(future.result())
        return result
    return wrapper
