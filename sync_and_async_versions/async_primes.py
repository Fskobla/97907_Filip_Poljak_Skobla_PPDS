import time
import queue
import asyncio


async def result(student, numbers, counter):
    while not numbers.empty():
        number = await numbers.get()
        if(student == "Matúš"):
            count_time = 1
            counter += 1
        else:
            count_time = 2
            counter += 1
        start = time.perf_counter()
        await asyncio.sleep(count_time)
        end = time.perf_counter() - start

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
    numbers = asyncio.Queue()
    counter = 0

    for number in [3, 4, 6, 7, 10, 13, 14, 18, 22, 24, 29, 30]:
        await numbers.put(number)

    results = [result("Matúš", numbers, counter),
               result("Milan", numbers, counter)]

    start = time.perf_counter()

    await asyncio.gather(*results)

    end = time.perf_counter() - start

    print(f"Čas trvania výpočtu prvočísiel: {end}")


if __name__ == "__main__":
    asyncio.run(main())
