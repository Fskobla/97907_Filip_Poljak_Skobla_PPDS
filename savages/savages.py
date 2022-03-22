from fei.ppds import Semaphore, Mutex, Thread, Event, print
from random import randint
from time import sleep


M = 5
N = 3
COOKS = 3


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self,
             print_str,
             savage_id,
             print_last_thread=False,
             print_each_thread=False):
        self.mutex.lock()
        self.cnt += 1
        if print_each_thread:
            print(print_str % (savage_id, self.cnt))
        if self.cnt == self.N:
            self.cnt = 0
            if print_last_thread:
                print(print_str % (savage_id))
            self.sem.signal(self.N)
        self.mutex.unlock()
        self.sem.wait()


class CookBarrier:
    def __init__(self, COOKS):
        self.COOKS = COOKS
        self.counter = 0
        self.mutex = Mutex()
        self.T = Semaphore(0)

    def wait(self, cook_id, shared):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.COOKS:
            self.counter = 0
            shared.servings = M
            print("kuchar %2d: dovarene -----> pocet porcii: %2d"
                  % (cook_id, shared.servings))
            shared.empty_pot.clear()
            shared.full_pot.signal()
            self.T.signal(self.COOKS)
        self.mutex.unlock()
        self.T.wait()


class Shared:
    def __init__(self):
        self.mutex = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Event()
        self.barrier1 = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)
        self.barrier3 = CookBarrier(COOKS)


def get_serving_from_pot(savage_id, shared):
    print("divoch %2d: beriem si porciu" % savage_id)
    shared.servings -= 1


def eat(savage_id):
    print("divoch %2d: hodujem" % savage_id)
    sleep(0.2 + randint(0, 3) / 10)


def savage(savage_id, shared):
    while True:
        shared.barrier1.wait(
            "divoch %2d: prisiel som na veceru, uz nas je %2d",
            savage_id,
            print_each_thread=True)
        shared.barrier2.wait("divoch %2d: uz sme vsetci, zaciname vecerat",
                             savage_id,
                             print_last_thread=True)

        shared.mutex.lock()
        print("divoch %2d: pocet zostavajucich porcii v hrnci je %2d" %
              (savage_id, shared.servings))
        if shared.servings == 0:
            print("divoch %2d: budim kuchara" % savage_id)
            shared.empty_pot.signal()
            shared.full_pot.wait()
        get_serving_from_pot(savage_id, shared)
        shared.mutex.unlock()
        eat(savage_id)


def put_servings_in_pot(cook_id):
    print("kuchar %2d: varim" % cook_id)
    sleep(0.4 + randint(0, 2) / 10)


def cook(cook_id, shared):
    while True:
        shared.empty_pot.wait()
        put_servings_in_pot(cook_id)
        shared.barrier3.wait(cook_id, shared)


def init_and_run(COOKS, N, M):
    threads = list()
    shared = Shared()
    for savage_id in range(0, N):
        threads.append(Thread(savage, savage_id, shared))
    for cook_id in range(0, COOKS):
        threads.append(Thread(cook, cook_id, shared))

    for t in threads:
        t.join()


if __name__ == "__main__":
    init_and_run(COOKS, N, M)
