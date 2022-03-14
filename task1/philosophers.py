from time import sleep
from random import randint
from fei.ppds import Semaphore, Thread, print

# Number of philosophers
PHIL_NUM = 5


def phil(forks, fork1, fork2, p_id):
    """
    A function for dining philosophers
    """
    sleep(randint(40, 100)/1000)

    while True:
        think(p_id)
        get_forks(forks, fork1, fork2, p_id)
        eat(p_id)
        put_forks(forks, fork1, fork2, p_id)


def think(p_id):
    """
    A function of thinking in example
    """
    print(f'{p_id:02d}: thinking')
    sleep(randint(40, 50)/1000)


def eat(p_id):
    """
    A function of eating in example
    """
    print(f'{p_id:02d}: eating')
    sleep(randint(40, 50)/1000)


def get_forks(forks, fork1, fork2, p_id):
    """
    A function for getting forks
    """
    print(f'{p_id:02d}: try to get forks')
    forks[fork1].wait()
    forks[fork2].wait()
    print(f'{p_id:02d}: taken forks')


def put_forks(forks, fork1, fork2, p_id):
    """
    A function for putting forks after eating
    """
    forks[fork1].signal()
    forks[fork2].signal()
    print(f'{p_id:02d}: put forks')


def main():
    """
    A main funcion
    """
    # Number of forks
    forks = [Semaphore(1) for _ in range(PHIL_NUM)]

    # Random generator which indicates group of left/right forks
    random = randint(1, PHIL_NUM-1)
    p_type = [0]*(PHIL_NUM-random) + [1] * random

    philosophers = []
    for p_id in range(PHIL_NUM):
        right = (p_id + 1) % PHIL_NUM
        left = p_id

        # Array consist of 1 and 0 and indicates right/left fork
        if p_type[p_id]:
            philosophers.append(Thread(phil, forks, right, left, p_id))
        else:
            philosophers.append(Thread(phil, forks, left, right, p_id))

    for p in philosophers:
        p.join()


if __name__ == '__main__':
    main()
