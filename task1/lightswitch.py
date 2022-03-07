from time import sleep
from random import randint
from fei.ppds import Thread, Semaphore, Mutex, print


class LightSwitch(object):
    """
    A class to represent a lightswitch object
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the lightswitch object.
        Parameters
        ----------
            counter : int
                counter for ls
            mutex : Mutex
                imported mutex from fei.ppds for use in thread parallelism
        """
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore):
        """
        Method of lightswitch (first thread wants to enter the room)
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()

    def unlock(self, semaphore):
        """
        Method of lightswitch (last thread wants to leave the room)
        """
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()

"""
Example for usage of LightSwitch in Writer-Reader scheme
"""


class Shared():
    """
    A class to represent a lightswitch object
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the lightswitch object.
        Parameters
        ----------
            roomEmpty : Semaphore
                value 1, tells if room is empty
            readLS : LightSwitch
                LightSwitch object
            turniket : Semaphore
                value 1, enable thread/s
        """
        self.roomEmpty = Semaphore(1)
        self.readLS = LightSwitch()
        self.turniket = Semaphore(1)


def writer(shared):
    """
    A function for WRITER in W-R example
    """
    while True:
        # wait for writing in interval <0.0; 1> seconds
        sleep(randint(0, 10)/10)

        shared.turniket.wait()
        shared.roomEmpty.wait()
        # simulation of write in interval <0.1; 0.3> seconds
        sleep(0.1 + randint(0, 2)/10)
        print("W")
        shared.roomEmpty.signal()
        shared.turniket.signal()


def reader(shared):
    """
    A function for READER in W-R example
    """
    while True:
        # wait for reading in interval <0.0; 1> seconds
        sleep(randint(0, 10)/10)

        shared.turniket.wait()
        shared.turniket.signal()
        shared.readLS.lock(shared.roomEmpty)
        # simulate reading in interval <0.3; 0.7> seconds
        sleep(0.3 + randint(0, 4)/10)
        print("R")
        shared.readLS.unlock(shared.roomEmpty)

shared = Shared()
threads = []

for i in range(10):
    t = Thread(writer, shared)
    t = Thread(reader, shared)
    threads.append(t)

for t in threads:
    t.join()
