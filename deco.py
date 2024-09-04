import time
import numpy as np
from copy import deepcopy

# Decorator to get execution time of algorithm
def calculate_time_taken(func):
    
    def get_time_taken(*args, **kwargs):
        begin: float = time.process_time()  # begin time count
        func(*args, **kwargs)
        end: float = time.process_time()  # end time count

        # using perf_counter is better than time as if the execution time is too low, time.time() wont be able to record the time
        # perf_counter is better for benchmarking compared to time.time
        # maybe try using process_time ? Better if want to know efficiency of a process

        # print(f"Time Taken: {end-begin} ns")
        return round(end-begin, 7)  # rounding to 7 decimal places

    return get_time_taken

# Decorator to test different kind of input test cases
def generate_random_test_case(length:int, input_type:str='random', display:bool=True, random_state:int=1023):
    np.random.seed(random_state)  # to fix the input

    def inner(func):

        def wrapper(*args, **kwargs):
            print(f'Test Case: type={input_type}, length={length}')

            random_list: list[int] = list(np.random.randint(low=0, high=int(1e7), size=(length,)))
            if input_type == 'sorted':
                random_list = sorted(random_list)
            elif input_type == 'reverse-sorted':
                random_list = sorted(random_list, reverse=True)

            result:list[int]|None = func(deepcopy(random_list), *args, **kwargs)

            if display: 
                print("Input Numbers: \t\t", random_list)
                print("Result after Sorting: \t", result)

            return result
        return wrapper
    return inner
