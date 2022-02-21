from collections import Counter
from time import sleep
from random import randint
from fei.ppds import Thread, Mutex


class Shared():
    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elements = [0] * size
        self.mutex = Mutex()


def do_count(shared):
    shared.mutex.lock()
    while True:
        if shared.counter >= shared.end:
            break
        shared.elements[shared.counter] += 1
        sleep(randint(1, 10)/1000)
        shared.counter += 1
    shared.mutex.unlock()

shared = Shared(1_000)
thread1 = Thread(do_count, shared)
thread2 = Thread(do_count, shared)
thread1.join()
thread2.join()

counter = Counter(shared.elements)
print(counter.most_common())
