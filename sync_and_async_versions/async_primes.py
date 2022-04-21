"""
Copyright 2022 Filip Poljak Skobla. All Rights Reserved.
Licensed to GPLv2 www.gnu.org/licenses/old-licenses/gpl-2.0.html
Asynchronise version of primes
"""

import time
import queue
import asyncio


async def result(student, numbers, counter):
    """
        Function that choosing the numbers if it is prime or not
    """
    while not numbers.empty():
        number = await numbers.get()
        # If student is Matus - 1s time for define number
        if(student == "Matúš"):
            count_time = 1
            counter += 1
        # If student is Milan - 2s count
        else:
            count_time = 2
            counter += 1
        start = time.perf_counter()
        await asyncio.sleep(count_time)
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
    print(f"Študent {student} určil celkovo {counter} čísiel")

async def main():
    """
        The main function which initialize variables
    """
    # Empty queue for numbers
    numbers = asyncio.Queue()
    # Counter how much choose the numbers
    counter = 0

    # Add numbers into the queue
    for number in [3, 4, 6, 7, 10, 13, 14, 18, 22, 24, 29, 30]:
        await numbers.put(number)

    # Two students
    results = [result("Matúš", numbers, counter),
               result("Milan", numbers, counter)]

    start = time.perf_counter()

    # Asynchronise gathering the results
    await asyncio.gather(*results)

    end = time.perf_counter() - start

    print(f"Čas trvania výpočtu prvočísiel: {end}")


if __name__ == "__main__":
    asyncio.run(main())
