# Testing our multiprocessing on new VM
# https://www.kth.se/blogs/pdc/2019/02/parallel-programming-in-python-multiprocessing-part-1/

import multiprocessing as mp

def square(x):
    return x * x

nprocs = mp.cpu_count()
print(f"You have {nprocs}")

pool = mp.Pool(processes=nprocs)

# This throws a freeze error on Windows. Run on Ubuntu instead
result = pool.map(square, range(5))
print(result)
