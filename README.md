# PPDS - Paralelné programovanie a distribuované systémy
![FEI](https://www.fei.stuba.sk/buxus/images/web/logoFEI.jpg)
## Cvičenie 3: Vypínač, P-K, Č-Z
#### Programovací jazyk: Python verzie 3.10.2
![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)
Programy, ktoré demonštrujú využitie vypínača, P-K, Č-Z.
#### Ako spusiť programy
V prvom rade treba stiahnúť repozitár s príslušnými súbormi príkladov(konkrétne sa jedná o 3 príklady využitia turniketov a bariéry). Pričom je potrebné mať nainštalované vývojové prostredie pre programovací jazyk Python verzie 3.10.2. 

#### Dokumentácia
Repozitár sa skladá z dvoch úloh:
- Úloha 1: obsahuje jeden python programy (vypínač s príkladom)

##### Úloha 1 
Pri danej úlohe je spravená trieda LightSwitch s vlastnými metódami a príklad použitia.
##### LightSwitch
```python
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
```
Funguje to na princípe, že prvý miestnosť rozsvieti - metóda lock a posledný zase zhasína - metóda unlock.
Ako príklad použitia som implementoval zapisovateľ a čitateľ schému, konkrétne schému vyhladovania s použitím aj turniketu podľa psedukódu z prednášky. 
#### Špeciálne poďakovanie
Mgr. Ing. Matúš Jókay, PhD. - za hlavnú štruktúru programu.

-------


