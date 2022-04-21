"""
Copyright 2022 Filip Poljak Skobla. All Rights Reserved.
Licensed to GPLv2 www.gnu.org/licenses/old-licenses/gpl-2.0.html
Synchronise version of primes
"""

import time
import queue


def result(student, numbers):
    """
        Function that choosing the numbers if it is prime or not
    """
    while not numbers.empty():
        number = numbers.get()
        # If student is Matus - 1s time for define number
        if(student == "Matúš"):
            count_time = 1
        # If student is Milan - 2s count
        else:
            count_time = 2
        start = time.perf_counter()
        time.sleep(count_time)
        end = time.perf_counter() - start

        # Define if number is prime
        for i in range(2, number):
            if(number % i == 0):
                print(f"Študent {student}: určil číslo {number},"
                      f"že nie je prvočíslo, trvalo mu to: {end}")
                break
            else:
                print(f"Študent {student}: určil číslo {number},"
                      f"je prvočíslo, trvalo mu to: {end}")
                break
        yield


def main():
    """
        The main function which initialize variables
    """
    # Empty queue for numbers
    numbers = queue.Queue()
    # Add numbers into the queue
    for number in [3, 4, 6, 7, 10, 13, 14, 18, 22, 24, 29, 30]:
        numbers.put(number)

    # Two students
    results = [result("Matúš", numbers), result("Milan", numbers)]

    start = time.perf_counter()

    # Loop which will repeat until the queue is not empty
    loop = True
    while loop:
        for r in results:
            try:
                next(r)
            except StopIteration:
                results.remove(r)
                if len(results) == 0:
                    loop = False
    end = time.perf_counter() - start
    print(f"Čas trvania výpočtu prvočísiel: {end}")


if __name__ == "__main__":
    main()
