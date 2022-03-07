from time import sleep
from random import randint
from fei.ppds import Thread, Semaphore, Mutex, print


class LightSwitch(object):
    def __init__(self):
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


class Shared():
    def __init__(self):
        self.roomEmpty = Semaphore(1)
        self.readLS = LightSwitch()
        self.turniket = Semaphore(1)


def writer(shared):
    while True:
        # pred kazdym pokusom o zapis pocka v intervale <0.0; 1> sekundy
        sleep(randint(0, 10)/10)

        shared.turniket.wait()
        shared.roomEmpty.wait()
        # simulujeme dlzku zapisu v intervale <0.1; 0.3> sekundy
        sleep(0.1 + randint(0, 2)/10)
        print("W")
        shared.roomEmpty.signal()
        shared.turniket.signal()


def reader(shared):
    while True:
        # pred kazdym pokusom o citanie pocka sa v intervale <0.0; 1> sekundy
        sleep(randint(0, 10)/10)

        shared.turniket.wait()
        shared.turniket.signal()
        shared.readLS.lock(shared.roomEmpty)
        # simulujeme dlzku citania v intervale <0.3; 0.7> sekundy
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
