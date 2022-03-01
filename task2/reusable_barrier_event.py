from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, Event
from fei.ppds import print


class SimpleBarrier:
    """
    A class to represent a barrier object
    """
    def __init__(self, N):
        """
        Constructs all the necessary attributes for the barrier object.
        Parameters
        ----------
            N : int
                number of threads
            counter : int
                counter for barrier
            mutex : Mutex
                imported mutex from fei.ppds for use in thread parallelism
            event : Event
                imported Event from fei.ppds, which is use for signalization
        """
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        """
        Method of barrier with using of event
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.N:
            self.counter = 0
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()
        self.event.clear()


def rendezvous(thread_name):
    """
    Function for printing before the barrier
        Parameters:
                thread_name: name of the thread
    """
    sleep(randint(1, 10)/10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    """
    Function for printing after the barrier
        Parameters:
                thread_name: name of the thread
    """
    print('ko: %s' % thread_name)
    sleep(randint(1, 10)/10)


def barrier_example(barrier, thread_name):
    """
    Function which uses reusable barrier and print function rendezvous and ko
        Parameters:
                barrier: barrier class
                thread_name: name of the thread
    """
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
