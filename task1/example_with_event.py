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
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.N:
            self.counter = 0
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()


def barrier_example(barrier, thread_id):
    """
    Function which uses barrier and print id of the current running thread
    before and after barrier
        Parameters:
                barrier: barrier class
                thread_id: id of the thread
    """
    sleep(randint(1, 10)/10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)


sb = SimpleBarrier(5)

threads = [Thread(barrier_example, sb, i) for i in range(5)]
[t.join() for t in threads]
