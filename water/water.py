from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.counter = 0
        self.sem = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.N:
            self.counter = 0
            print("Voda vznikla")
            self.sem.signal(self.N)
        self.mutex.unlock()
        self.sem.wait()


class Shared:
    def __init__(self):
        self.mutex = Mutex()
        self.oxygen = 0
        self.hydrogen = 0
        self.barrier = SimpleBarrier(3)
        self.oxyQueue = Semaphore(0)
        self.hydroQueue = Semaphore(0)


def oxygen(shared):
    shared.mutex.lock()
    shared.oxygen += 1
    if shared.hydrogen < 2:
        shared.mutex.unlock()
    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxyQueue.signal()
        shared.hydroQueue.signal(2)
    shared.oxyQueue.wait()
    bond(shared)
    shared.barrier.wait()
    shared.mutex.unlock()


def hydrogen(shared):
    shared.mutex.lock()
    shared.hydrogen += 1
    if shared.hydrogen < 2 or shared.oxygen < 1:
        shared.mutex.unlock()
    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxyQueue.signal()
        shared.hydroQueue.signal(2)
    shared.hydroQueue.wait()
    bond(shared)
    shared.barrier.wait()


def bond(shared):
    sleep(0.2 + randint(0, 3) / 10)


def init_and_run():
    threads = list()
    shared = Shared()
    counterHydrogen = 0
    counterOxygen = 0
    while True:
        i = randint(0, 3)
        if i % 2 == 0:
            threads.append(Thread(oxygen, shared))
            print("O")
            counterOxygen += 1
            sleep(0.4 + randint(0, 3) / 10)
        else:
            threads.append(Thread(hydrogen, shared))
            print("H")
            counterHydrogen += 1
            sleep(0.4 + randint(0, 3) / 10)
        print("Celkovy pocet H: %2d" % counterHydrogen)
        print("Celkovy pocet O: %2d" % counterOxygen)
    for t in threads:
        t.join()

if __name__ == "__main__":
    init_and_run()
