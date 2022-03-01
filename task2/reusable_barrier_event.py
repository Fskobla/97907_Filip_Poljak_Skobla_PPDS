from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, Event
from fei.ppds import print


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.N:
            self.counter = 0
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()
        self.event.clear()


def rendezvous(thread_name):
    sleep(randint(1, 10)/10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1, 10)/10)


def barrier_example(barrier, thread_name):
    while True:
        rendezvous(thread_name)
        barrier.wait()
        ko(thread_name)
        barrier.wait()

threads = list()
sb = SimpleBarrier(5)
for i in range(5):
    t = Thread(barrier_example, sb, 'Thread %d' % i)
    threads.append(t)

for t in threads:
    t.join()
