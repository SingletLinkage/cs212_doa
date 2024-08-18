import time
import numpy as np
from copy import deepcopy
import sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(100000)

def calculate_time_taken(func):
    
    def get_time_taken(*args, **kwargs):
        begin = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()

        # print(f"Time Taken: {end-begin} ns")
        return round(end-begin, 7)

    return get_time_taken

# Not needed now
def generate_random_test_case(length, input_type='random', display=True, random_state=1023):
    np.random.seed(random_state)

    def inner(func):

        def wrapper(*args, **kwargs):
            print(f'Test Case: type={input_type}, length={length}')

            random_list = list(np.random.randint(low=0, high=int(1e7), size=(length,)))
            if input_type == 'sorted':
                random_list = sorted(random_list)
            elif input_type == 'reverse-sorted':
                random_list = sorted(random_list, reverse=True)

            result = func(deepcopy(random_list), *args, **kwargs)

            if display: 
                print("Input Numbers: \t\t", random_list)
                print("Result after Sorting: \t", result)

            return result
        return wrapper
    return inner



def complete_analysis(func):

    def get_test_set(length: int):
        # [random, sorted, reverse-sorted, many_duplicates]
        _random = list(np.random.randint(low=0, high=10**7, size=(length, )))
        _sorted = sorted(_random)
        _reverse = _sorted[::-1]
        _duplicates = _random[:int(length//3)]*4
        np.random.shuffle(_duplicates)
        _duplicates = _duplicates[:length]

        return _random, _sorted, _reverse, _duplicates

    def inner(*args, **kwargs):

        _len_test_cases = kwargs.get('test_len', 1000)
        _test_case_set = get_test_set(_len_test_cases)
        _time_taken = [-1]*4

        for _idx, _case in enumerate(_test_case_set):
            _time = calculate_time_taken(func)(array=_case)
            _time_taken[_idx] = _time
        
        print(f'''
Sorting Technique: {func.__name__}
Number of Elements: {_len_test_cases}
Cases:
    1. Random Order: \t\t{_time_taken[0]} s
    2. Sorted Order: \t\t{_time_taken[1]} s
    3. Reverse Sorted Order: \t{_time_taken[2]} s
    4. With many duplicates: \t{_time_taken[3]} s
        ''')
        plt.bar(['Random', 'Sorted', "Reverse-Sorted", 'Duplicates'], _time_taken)
        plt.xlabel('Type of Data')
        plt.ylabel('Time Taken in seconds')
        plt.title(f'{func.__name__} with n={_len_test_cases}')
        plt.show()
            
    return inner

# @generate_random_test_case(length=int(1e4), input_type='random', display=False)
# @calculate_time_taken
def insertion_sort(array: list[int]):
    n: int = len(array)  # number of elements in the array
    for i  in range(1, n):   # since 1st element is already sorted
        key: int = array[i]
        j: int = i-1

        while(array[j] > key and j >= 0):
            array[j+1] = array[j]
            j = j-1

        array[j+1] = key
    
    return array

# @generate_random_test_case(length=int(1e4), input_type='random', display=False)
# @calculate_time_taken
def merge_sort_wrapper(array: list[int]):
    begin=0
    end = len(array)
    merge_sort(array, begin, end)

def merge_sort(array: list[int], begin:int=0, end:int|None=None):
    if end is None:
        end=len(array)
        
    if end - begin <= 1:
        return
    else:
        mid = int(begin + (end-begin)//2)
        merge_sort(array, begin, mid)
        merge_sort(array, mid, end)
        merge(array, begin, mid, end)


def merge(array, begin, mid, end):
    _temp = [-1]*(end-begin)
    i=begin
    j=mid
    k=0

    while i < mid and j < end:
        if array[i] > array[j]:
            _temp[k] = array[j]
            j += 1
            k += 1
        else:
            _temp[k] = array[i]
            i += 1
            k += 1
    
    while i < mid:
        _temp[k] = array[i]
        k += 1
        i += 1
    
    while j < end:
        _temp[k] = array[j]
        j += 1
        k += 1
    
    for i in range(begin, end):
        array[i] = _temp[i-begin]


def quick_sort(array, begin=0, end=None):
    if end is None:
        end = len(array)

    if end-begin <= 1:
        return
    
    pi = partition(array, begin, end)
    quick_sort(array, begin, pi)
    quick_sort(array, pi+1, end)


def partition(array, begin, end):
    
    # Using Median of Three Heuristic:
    pivot, pivot_idx = sorted([(array[i], i) for i in [begin, begin + int((end-begin)//2), end-1]], key=lambda x: x[0])[1]
    array[end-1], array[pivot_idx] = pivot, array[end-1]

    # Using end element as pivot
    # pivot = array[end-1]

    i = begin
    for j in range(begin, end-1):
        if array[j] < pivot:
            # print(f'swapping {array[i]} with {array[j]}')
            array[i], array[j] = array[j], array[i]
            i += 1

    array[i], array[end-1] = array[end-1], array[i]
    return i




if __name__ == '__main__':
    # complete_analysis(insertion_sort)(test_len=10000)
    complete_analysis(merge_sort)(test_len=10000)

    complete_analysis(quick_sort)(test_len=10000)


    # insertion_sort()
    # array = [2,51,9,23,46,1,234,8,19]
    # i = partition(0, len(array), array)
    # print(array, i)
    # print(array)
    # quick_sort(0, len(array), array)
    # print(array)
    # merge_sort_wrapper()
    # array = list(np.random.randint(0, 10**7, (10**4,)))
    # print('With random: ')
    # insertion_sort(array=array)

    # array = sorted(array, reverse=True)
    # print("With Reverse Sorted: ")
    # insertion_sort(array=array)
