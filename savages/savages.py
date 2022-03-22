from fei.ppds import Semaphore, Mutex, Thread, Event, print
from random import randint
from time import sleep

""" Global variables:
    M - maximum number of servings in pot
    N - number of savages
    COOKS - number of cooks(chefs)
"""
M = 5
N = 3
COOKS = 3


class SimpleBarrier:
    """A class of barrier with special implementation in wait()
    """
    def __init__(self, N):
        """
        Constructs all the necessary attributes for the barrier object.
        Parameters
        ----------
            N : int
                number of threads
            cnt : int
                counter for barrier
            mutex : Mutex
                imported mutex from fei.ppds for use in thread parallelism
            sem : Semaphore
               imported Semaphore from fei.ppds, which is use for signalization
        """
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self,
             print_str,
             savage_id,
             print_last_thread=False,
             print_each_thread=False):
        """
        Method of barrier with special usage of print
        """
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
    """A class of barrier for cooks with multiple cooking
    """
    def __init__(self, COOKS):
        """
        Constructs all the necessary attributes for the cook barrier object.
        Parameters
        ----------
            COOKS : int
                number of cooks
            counter : int
                counter for barrier
            mutex : Mutex
                imported mutex from fei.ppds for use in thread parallelism
            T : Semaphore
              imported Semaphore from fei.ppds, which is use for signalization
        """
        self.COOKS = COOKS
        self.counter = 0
        self.mutex = Mutex()
        self.T = Semaphore(0)

    def wait(self, cook_id, shared):
        """A method which is used for fullfiling pot by last cooks and
           signalise the savages that can eat
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.COOKS:
            self.counter = 0
            # Fullfiling of pot by last cooks
            shared.servings = M
            # Signalisation by printing
            print("kuchar %2d: dovarene -----> pocet porcii: %2d"
                  % (cook_id, shared.servings))
            shared.empty_pot.clear()
            shared.full_pot.signal()
            self.T.signal(self.COOKS)
        self.mutex.unlock()
        self.T.wait()


class Shared:
    """A class of shared object
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the cook barrier object.
        Parameters
        ----------
            mutex : Mutex
                mutex for threads
            servings : int
                counter of servings
            full_pot : Semaphore
                value 0, signalise if pot is full
            empty_pot : Event
                signalise if pot is empty
            barrier1, barrier2 : SimpleBarrier
                with value N - number of savages
            barrier3 : CookBarrier
                with value COOKS - number of cooks
                which represent the waitting for last cook to fullfil pot
        """
        self.mutex = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Event()
        self.barrier1 = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)
        self.barrier3 = CookBarrier(COOKS)


def get_serving_from_pot(savage_id, shared):
    """ A function of savages which represent that savages take portion """
    print("divoch %2d: beriem si porciu" % savage_id)
    shared.servings -= 1


def eat(savage_id):
    """ A function which represent that savages eat """
    print("divoch %2d: hodujem" % savage_id)
    # Time which represents eating
    sleep(0.2 + randint(0, 3) / 10)


def savage(savage_id, shared):
    """ A function of savage which informs about situation of savages, if
        they can eat (pot is not empty) or they can't eat (pot is empty)
    """
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
    """ A function in which cooks cook """
    print("kuchar %2d: varim" % cook_id)
    # Time which represents cooking
    sleep(0.4 + randint(0, 2) / 10)


def cook(cook_id, shared):
    """ A function which represent all cooking """
    while True:
        shared.empty_pot.wait()
        put_servings_in_pot(cook_id)
        shared.barrier3.wait(cook_id, shared)


def init_and_run(COOKS, N, M):
    """ Initialization of savages and cooks """
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
