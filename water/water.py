"""
Copyright 2022 Filip Poljak Skobla. All Rights Reserved.
Licensed to GPLv2 www.gnu.org/licenses/old-licenses/gpl-2.0.html

Synchronization problem which represents the formation of water from molecules:
    two hydrogens and one oxygen
"""

from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep


class SimpleBarrier:
    """ A class of barrier """
    def __init__(self, N):
        """
        Constructs all the necessary attributes for the barrier object.
        Parameters
        ----------
            N : int
                number of threads
            ccounter : int
                counter for barrier
            mutex : Mutex
                imported mutex from fei.ppds for use in thread parallelism
            sem : Semaphore
               imported Semaphore from fei.ppds, which is use for signalization
        """
        self.N = N
        self.mutex = Mutex()
        self.counter = 0
        self.sem = Semaphore(0)

    def wait(self):
        """
        Method of barrier with special usage of print that water was created
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.N:
            self.counter = 0
            # Printing if 2H and 1O can be created to water
            print("Voda vznikla")
            self.sem.signal(self.N)
        self.mutex.unlock()
        self.sem.wait()


class Shared:
    """A class of shared object with shared attributes
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the cook barrier object.
        Parameters
        ----------
            mutex : Mutex
                mutex for threads
            oxygen : int
                counter of oxygens
            hydrogen : int
                counter of hydrogens
            barrier: SimpleBarrier
                with value N - number of 3 needed molecules
            oxyQueue : Semaphore
                with value 0
            hydroQueue : Semaphore
                with value 0
        """
        self.mutex = Mutex()
        self.oxygen = 0
        self.hydrogen = 0
        self.barrier = SimpleBarrier(3)
        self.oxyQueue = Semaphore(0)
        self.hydroQueue = Semaphore(0)


def oxygen(shared):
    """ A function of oxygen in which is add one oxygen all time and
        if can be created water than bond molecules to water
    """
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
    """ A function of hydrogen in which is add one hydrogen all time and
        if can be created water than bond molecules to water
    """
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
    """ A function of bonding to water """
    # Representation of bonding time
    sleep(0.2 + randint(0, 3) / 10)


def init_and_run():
    """ Initialization of hydrogens and oxygen via threads and shared object"""
    threads = list()
    shared = Shared()
    # Counter of H and O for printing
    counterHydrogen = 0
    counterOxygen = 0
    while True:
        # Random number between <0,3> for randomization of creation O and H
        i = randint(0, 3)
        # Even number --> creation of Oxygens
        if i % 2 == 0:
            threads.append(Thread(oxygen, shared))
            print("O")
            counterOxygen += 1
            # Time that represent oxygen to print (for better visualisation)
            sleep(0.4 + randint(0, 3) / 10)
        else:
            threads.append(Thread(hydrogen, shared))
            print("H")
            counterHydrogen += 1
            # Time that represent hydrogen to print (for better visualisation)
            sleep(0.4 + randint(0, 3) / 10)
        print("Celkovy pocet H: %2d" % counterHydrogen)
        print("Celkovy pocet O: %2d" % counterOxygen)
    for t in threads:
        t.join()

if __name__ == "__main__":
    init_and_run()
