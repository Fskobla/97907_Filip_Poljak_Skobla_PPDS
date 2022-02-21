from collections import Counter
from time import sleep
from random import randint
from fei.ppds import Thread, Mutex


class Shared():
    """
    A class to represent a shared array of elements with size
    """
    def __init__(self, size):
        """
        Constructs all the necessary attributes for the shared object.
        Parameters
        ----------
            counter : int
                counter of elements
            end : int
                size of array
            elements : int
                array of int, on beginning size of array is end
                and filled with 0
            mutex : Mutex
                imported mutex from fei.ppds for use in thread parallelism
        """
        self.counter = 0
        self.end = size
        self.elements = [0] * size
        self.mutex = Mutex()


def do_count(shared):
    """
    Function which switches threads due to mutex
        Parameters:
                shared: class to use with parallelism
    """
    while True:
        if shared.counter >= shared.end:
            break
        # mutex inside the loop
        shared.mutex.lock()
        shared.elements[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()
        # simulation of switching to the next thread outside the
        # mutex critical location
        sleep(randint(1, 10)/1000)

shared = Shared(10000)
thread1 = Thread(do_count, shared)
thread2 = Thread(do_count, shared)
thread1.join()
thread2.join()

counter = Counter(shared.elements)
print(counter.most_common())

