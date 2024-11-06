import numpy as np

def memory_cpu_intensive():
    array = np.random.rand(10**7)
    array_sum = np.sum(array)

    def fibonacci(n):
        if n <= 1:
            return n
        else:
            return fibonacci(n-1) + fibonacci(n-2)

    fib_35 = fibonacci(35)

    return f"Sum of array: {array_sum}, Fibonacci(35): {fib_35}"
