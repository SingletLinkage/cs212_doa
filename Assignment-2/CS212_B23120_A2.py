import time
import numpy as np
from copy import deepcopy
import sys
import matplotlib.pyplot as plt
import json

def get_test_set(length: int):
    np.random.RandomState(1)
    # [random, sorted, reverse-sorted, many_duplicates]
    _random: list[int] = list(np.random.randint(low=0, high=1e4, size=(length, )))  # randomly selecting `length` number of integers between 0 and 10**7
    _sorted: list[int] = sorted(_random)  # sort the values
    _reverse: list[int] = _sorted[::-1]  # reverse the sorted array
    # selecting a specific (length/3) number of elements and tiling the list 5 times then shuffling and extracting the first `length` number of elements
    _duplicates: list[int] = _random[:int(length//3)]*5
    np.random.shuffle(_duplicates)
    _duplicates = _duplicates[:length]
    return _random, _sorted, _reverse, _duplicates

def write_to_file(length: int):
    _test_sets = get_test_set(length)
    with open(f'inputfile_{length}.json', 'w') as file:
        json.dump(dict(zip(['random', 'sorted', 'reverse', 'duplicates'], [','.join(map(str, _set)) for _set in _test_sets])), file)

def get_from_file(length: int):
    stuff = dict()
    with open(f'inputfile_{length}.json', 'r') as file:
        stuff = json.load(file)
    return {k: list(map(int, v.split(','))) for (k,v) in stuff.items()}

def complete_analysis(func, test_len: int = 1000):
    _test_case_set: dict[str: list[int]] = get_from_file(test_len) # dict to store arrays
    _time_taken: dict[str: float] = dict(zip(_test_case_set.keys(), [0.]*4)) # dict to store benchmark times

    for _type, _case in _test_case_set.items():
        _copied_case = deepcopy(_case)
        if func.__name__ == 'bucket_sort':
            _copied_case = list(map(lambda x: (x - min(_copied_case))/(max(_copied_case) - min(_copied_case)), _copied_case))
        _t1 = _t2 = 0
        _t1: float = time.perf_counter()  # begin time count
        func(_copied_case)
        _t2: float = time.perf_counter()  # end time count
        _time_taken[_type] = round(_t2-_t1, 6)
        
    print(f'''
Sorting Technique: {func.__name__}
Number of Elements: {test_len}
Cases:
    1. Random Order: \t\t{_time_taken['random']} s
    2. Sorted Order: \t\t{_time_taken['sorted']} s
    3. Reverse Sorted Order: \t{_time_taken['reverse']} s
    4. With many duplicates: \t{_time_taken['duplicates']} s
        ''')
    return _time_taken            

def insertion_sort(array: list[float]):
    n: int = len(array)  # number of elements in the array
    for i  in range(1, n):   # since 1st element is already sorted
        key: int = array[i]
        j: int = i-1

        while(array[j] > key and j >= 0):
            array[j+1] = array[j]
            j = j-1

        array[j+1] = key
    
def bucket_sort(array: list[float]):
    buckets = [[] for _ in range(len(array))]

    for item in array:
        buckets[min(int(item*len(array)),len(array)-1)].append(item)
    
    for bucket in buckets:
        insertion_sort(bucket)
    
    array = sum(buckets, [])
    return array

def radix_sort(array: list[int]):
    max_digits = np.log10(max(array)) + 1
    for i in range(int(max_digits)):
        buckets = [[] for _ in range(10)]
        for item in array:
            buckets[int(item/(10**i))%10].append(item)
        array = sum(buckets, [])
    return array

if __name__ == '__main__':
    dataset = dict()
    for func in [radix_sort, bucket_sort]:
        dataset[func.__name__] = dict()
        for i in [100, 1000, 10000]:
            dataset[func.__name__][i] = complete_analysis(func, test_len=i)

    # some cool plots
    fig, ax = plt.subplots(2, 3, figsize=(15, 15))
    for i, (func, data) in enumerate(dataset.items()):
        for j, (n, times) in enumerate(data.items()):
            ax[i, j].bar(times.keys(), times.values(), color=['red', 'green', 'blue', 'orange'])
            ax[i, j].set_title(f'{func} with n={n}')
            ax[i, j].set_ylabel('Time Taken in seconds')
    plt.tight_layout()
    plt.show()
    
    # compare performance of all algo for elements
    fig, ax = plt.subplots(1, 3, figsize=(10, 5))
    for func, data in dataset.items():
        for i in [2,3,4]:
            ax[i-2].bar(data[10**i].keys(), data[10**i].values(), label=func, alpha=0.5)
            ax[i-2].set_title(f'Performance of Sorting Algorithms for {10**i} elements')
            ax[i-2].set_xlabel('Cases')
            ax[i-2].set_ylabel('Time Taken in seconds')
            ax[i-2].legend()
    plt.tight_layout()
    plt.show()