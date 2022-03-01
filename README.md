# PPDS - Paralelné programovanie a distribuované systémy
![FEI](https://www.fei.stuba.sk/buxus/images/web/logoFEI.jpg)
## Cvičenie 2: Turniket, bariéra
#### Programovací jazyk: Python verzie 3.10.2
![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)
Programy, ktoré demonštrujú využitie turniketov, bariéry a znovupoužiteľnej bariéry.
#### Ako spusiť programy
V prvom rade treba stiahnúť repozitár s príslušnými súbormi príkladov(konkrétne sa jedná o 3 príklady využitia turniketov a bariéry). Pričom je potrebné mať nainštalované vývojové prostredie pre programovací jazyk Python verzie 3.10.2. 

#### Dokumentácia
Repozitár sa skladá z dvoch úloh:
- Úloha 1: obsahuje dva python programy (jednoduchá bariéra s využitím semaforu a jednoduchá bariéra s využitím eventu)
- Úloha 2: obsahuje jeden python program (znovupoužiteľná bariéra)

##### Úloha 1 
Pri danej úlohe boli je vytvorený príklad s využitím semaforu a eventu, pričom štruktúra kódu sa líši len v triede bariéry.
##### Využitie semaforu 
```python
class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.T = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.N:
            self.counter = 0
            self.T.signal(self.N)
        self.mutex.unlock()
        self.T.wait()
```
V tomto príklade sa na začiatku triedy inicializujú hodnoty N(počet vlákien), counter(počítadlo), mutex(zámok) a semafor.
Následne vo funkcií triedy je vytvorená funkcionalita bariéry, ktorá funguje na princípe:
- je využitý zámok, kvôli ochrany integrity (medzi vláknami) 
- vo vnútri zámku sa navyšuje počítadlo, pričom T(semafor) čaká na signál
- signál je vydaný až vtedy ak príde posledné vlákno, ktoré uvolní bariéru

##### Využitie eventu 
```python
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
```
Tento príklad je veľmi podobný s príkladom využitie semaforu. Ale namiesto semaforu sa tu využíva Event(signalizácia).
Na začiatku sa namiesto semaforu inicializuje event a princíp fungovania je v podstate rovnaký.

###### Výsledkom je výpis:
```python
vlakno i pred barierou
...
...
vlakno i po bariere
...
...
```
i = číslo od 0 po N (môže byť náhodne usporiadané a vypísané len raz)

##### Úloha 2 - Znovupoužiteľná bariéra
V danom príklade sa kód skladá z triedy bariéry, funkcie, v ktorej sa používa bariéra a pomocné funkcie na výpis.
```python
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
```
Ako je možné vidno na danom kóde, tak oproti príkladu event z úlohy 1 sa zmenil len jeden riadok kódu. Vďaka metóde clear() je možné barierú znovu použiť, pretože po zavolaní začne byť wait() blokujúci a znova sa bude čakať na signal(), ktorý sa aktivuje vzhľadom na podmienku(počet vlákien N).
```python
def barrier_example(barrier, thread_name):
    while True:
        rendezvous(thread_name)
        barrier.wait()
        ko(thread_name)
        barrier.wait()
```
Následne je vo funkcií daná bariéra dvakrát použitá(t.j. znovupoužiteľná bariéra) spolu s funkciou rendezvous a ko, ktoré slúžia na výpis informácií o názve vlákna. Pri tejto funkcíí to funguje teda tak, že sa vypíše N-krát rendezvous, kvôli využitiu bariéry prvýkrát a následne sa vypíše N-krát ko, kvôli využitiu bariéry, pretože sa čaká na všetky vlákna.
###### Výsledkom je výpis:
```python
rendezvous: Thread i
...
...
ko: Thread i
...
...
```
i = číslo od 0 po N (môže byť náhodne usporiadané a vypísané len raz)
#### Špeciálne poďakovanie
Mgr. Ing. Matúš Jókay, PhD. - za hlavnú štruktúru programu.

-------