from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print


class Shared(object):
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)

        self.agentSemaphore = Semaphore(1)

        self.tobaccoCounter = 0
        self.paperCounter = 0
        self.matchCounter = 0
        self.mutex = Mutex()

        self.dealerTobacco = Semaphore(0)
        self.dealerPaper = Semaphore(0)
        self.dealerMatch = Semaphore(0)


def make_cigarette(name):
    print(f"smoker '{name}' makes cigarette")
    sleep(randint(0, 10)/100)


def smoke(name):
    print(f"smoker '{name}' smokes")
    sleep(randint(0, 10)/100)


def smoker_tobacco(shared):
    while True:
        sleep(randint(0, 10)/100)
        shared.dealerTobacco.wait()
        make_cigarette("smoker_tobacco")
        smoke("smoker_tobacco")


def smoker_paper(shared):
    while True:
        sleep(randint(0, 10)/100)
        shared.dealerPaper.wait()
        make_cigarette("smoker_paper")
        smoke("smoker_paper")


def smoker_match(shared):
    while True:
        sleep(randint(0, 10)/100)
        shared.dealerMatch.wait()
        make_cigarette("smoker_match")
        smoke("smoker_match")


def agent_1(shared):
    while True:
        sleep(randint(0, 10)/100)
        print("agent: tobacco, paper --> smoker_match")
        shared.tobacco.signal()
        shared.paper.signal()


def agent_2(shared):
    while True:
        sleep(randint(0, 10)/100)
        print("agent: paper, match --> smoker_tobacco")
        shared.paper.signal()
        shared.match.signal()


def agent_3(shared):
    while True:
        sleep(randint(0, 10)/100)
        print("agent: tobacco, match --> smoker_paper")
        shared.tobacco.signal()
        shared.match.signal()


def dealer_tobacco(shared):
    while True:
        shared.tobacco.wait()
        shared.mutex.lock()

        counterT = shared.tobaccoCounter
        counterP = shared.paperCounter
        counterM = shared.matchCounter
        if shared.paperCounter:
            shared.paperCounter -= 1
            shared.dealerMatch.signal()
        elif shared.matchCounter:
            shared.matchCounter -= 1
            shared.dealerPaper.signal()
        else:
            shared.tobaccoCounter += 1

        print(f"tobacco: {counterT}->{shared.tobaccoCounter},"
              f"paper:{counterP}->{shared.paperCounter},"
              f"match: {counterM}->{shared.matchCounter}")
        shared.mutex.unlock()


def dealer_paper(shared):
    while True:
        shared.paper.wait()
        shared.mutex.lock()

        counterT = shared.tobaccoCounter
        counterP = shared.paperCounter
        counterM = shared.matchCounter
        if shared.matchCounter:
            shared.matchCounter -= 1
            shared.dealerTobacco.signal()
        elif shared.tobaccoCounter:
            shared.tobaccoCounter -= 1
            shared.dealerMatch.signal()
        else:
            shared.paperCounter += 1

        print(f"tobacco: {counterT}->{shared.tobaccoCounter},"
              f"paper:{counterP}->{shared.paperCounter},"
              f"match: {counterM}->{shared.matchCounter}")
        shared.mutex.unlock()


def dealer_match(shared):
    while True:
        shared.match.wait()
        shared.mutex.lock()

        counterT = shared.tobaccoCounter
        counterP = shared.paperCounter
        counterM = shared.matchCounter
        if shared.tobaccoCounter:
            shared.tobaccoCounter -= 1
            shared.dealerPaper.signal()
        elif shared.paperCounter:
            shared.paperCounter -= 1
            shared.dealerTobacco.signal()
        else:
            shared.matchCounter += 1

        print(f"tobacco: {counterT}->{shared.tobaccoCounter},"
              f"paper:{counterP}->{shared.paperCounter},"
              f"match: {counterM}->{shared.matchCounter}")
        shared.mutex.unlock()


def run_model():
    shared = Shared()

    dealers = []
    dealers.append(Thread(dealer_match, shared))
    dealers.append(Thread(dealer_tobacco, shared))
    dealers.append(Thread(dealer_paper, shared))
    smokers = []
    smokers.append(Thread(smoker_match, shared))
    smokers.append(Thread(smoker_tobacco, shared))
    smokers.append(Thread(smoker_paper, shared))
    agents = []
    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))

    for t in agents + smokers + dealers:
        t.join()

if __name__ == "__main__":
    run_model()
