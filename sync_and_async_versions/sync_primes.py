import time
import queue


def result(student, numbers):
    while not numbers.empty():
        number = numbers.get()
        if(student == "Matúš"):
            count_time = 1
        else:
            count_time = 2
        start = time.perf_counter()
        time.sleep(count_time)
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
        yield


def main():
    numbers = queue.Queue()
    for number in [3, 4, 6, 7, 10, 13, 14, 18, 22, 24, 29, 30]:
        numbers.put(number)

    results = [result("Matúš", numbers), result("Milan", numbers)]

    start = time.perf_counter()

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
