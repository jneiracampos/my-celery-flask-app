import numpy as np

def memory_and_cpu_intensive():

    # Memory Intensive
    large_array = np.random.rand(10**7)
    np.sum(large_array)

    # CPU Intensive
    def fibonacci(n):
        if n <= 1:
            return n
        else:
            return fibonacci(n-1) + fibonacci(n-2)

    fibonacci(35)

    print("Memory and CPU intensive operations completed.")

if __name__ == "__main__":
    memory_and_cpu_intensive()
