# PPDS - Paralelné programovanie a distribuované systémy
![FEI](https://www.fei.stuba.sk/buxus/images/web/logoFEI.jpg)
## Cvičenie 5: Problém fajčiarov, problém divochov
#### Programovací jazyk: Python verzie 3.10.2
![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)
Programy, ktoré demonštrujú príklad fajčiarov a divochov
#### Ako spusiť programy
V prvom rade treba stiahnúť repozitár s príslušnými súbormi príkladov. Pričom je potrebné mať nainštalované vývojové prostredie pre programovací jazyk Python verzie 3.10.2. 

#### Dokumentácia
Repozitár sa skladá z dvoch úloh:
- Úloha 1: obsahuje jeden python program (problém fajčiarov)
- Úloha 2: obsahuje jeden python program (problém divochov)

##### Úloha 1 - Problém fajčiarov
##### Analýza
Pri danej úlohe bol odskúšaný príklad podľa seminára, pri ktorom by na základe podmienky pri dealeroch mala byť jedna surovina uprednosťovaná. Avšak pri pôvodnom príklade môžem po niekoľkých spusteniach poznamenať, že to tak nebolo, pretože základom pre fajčenie cigarety je dodávka surovín od agenta. Nakoniec som tento príklad trocha upravil v podmienke, kde pri if nie je rovnaká surovina dvakrát a taktiež podľa výsledku je hlavnou príčinou, kto skôr bude fajčiť dodávka surovín od agenta.
V prvom rade si vytvoríme počet vidličiek, ktorí zodpovedá počtu filozofov(globálna premenná). Následne si vytvoríme random číslo v rozsahu a na základe toho vytvoríme pole, ktoré má hodnoty 0 a 1. Tento princíp je taký, že na začiatku poľa sú 0 a následne podľa vygenerovanej hodnoty random sú 1, čo nám bude značiť ľavákov a pravákov, pričom je aspoň jeden z danej skupiny. Potom v cykle prechádzame a určíme si hodnoty ľavákov a pravákov a následne podľa núl a jednotiek z daného poľa ich vytvoríme.

##### Úloha 2 - Problém divochov
Pri danej úlohe bolo vyriešiť problém divochov a viacerých kuchárov, ktorí môžu variť naraz.
##### Analýza
Táto úloha sa dosť podobá na problém producent-konzument, pretože pri tejto úlohe je v podstate producent-
kuchár, ktorý napĺňa hrniec. A ako konzument tu vystupuje divoch, ktorý konzumuje z hrnca nejaké jedlo.

----
V úvode tejto úlohy som si vytvoril určitý počet jediel, kuchárov a divochov - tieto 3 počty sú v programe reprezentované globálnymi premennými. A okrem toho som si vytvoril novú triedu bariéry pre reprezentáciu kuchára a upravil funkciu spojenú s ním - funkcia cook() a taktiež hlavnú funkciu, v ktorej sa inicializujú divosi a kuchári.
```python
class CookBarrier:
        self.COOKS = COOKS
        self.counter = 0
        self.mutex = Mutex()
        self.T = Semaphore(0)

    def wait(self, cook_id, shared):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.COOKS:
            self.counter = 0
            shared.servings = M
            print("kuchar %2d: dovarene -----> pocet porcii: %2d"
                  % (cook_id, shared.servings))
            shared.empty_pot.clear()
            shared.full_pot.signal()
            self.T.signal(self.COOKS)
        self.mutex.unlock()
        self.T.wait()
```
Hlavnou úlohou bolo asi vytvoriť danú bariéru pre kuchára. A táto bariéra spočíva v tom, že sa kuchári čakajú a ak príde posledný, tak ten naplní hrniec, informuje o naplnenosti a dá signál divochom, že hrniec je naplnený.
```python
def cook(cook_id, shared):
    while True:
        shared.empty_pot.wait()
        put_servings_in_pot(cook_id)
        shared.barrier3.wait(cook_id, shared)
```
A ďalšia funkcia bola cook, v ktorej v cykle sa čaká na divochov, ktorí dajú informáciu o prázdnosti hrnca a kuchári začnú variť a nasleduje bariéra.
##### Pseudokód
```python
M ← 5
N ← 3
COOKS ← 3

Class CookBarrier:
    Function __init__(self, COOKS):
        self.COOKS ← COOKS
        self.counter ← 0 
        self.mutex ← Mutex()
        self.T ← Semaphore(0)
    end 
        
    Function wait(self, cook_id, shared):
        self.mutex.lock()
        self.counter ← self.counter + 1 
        if self.counter equals self.COOKS:
            self.counter ← 0
            shared.servings ← M
            output("kuchar %2d: dovarene -----> pocet porcii: %2d"
                  % (cook_id, shared.servings))
            shared.empty_pot.clear()
            shared.full_pot.signal()
            self.T.signal(self.COOKS)
        self.mutex.unlock()
        self.T.wait()
    end
```     
```python
Function put_servings_in_pot(cook_id):
    output("kuchar %2d: varim" % cook_id)
    sleep(0.4 + randint(0, 2) / 10)
end
``` 
```python
Function cook(cook_id, shared):
    while True:
        shared.empty_pot.wait()
        put_servings_in_pot(cook_id)
        shared.barrier3.wait(cook_id, shared)
    end while
end 
``` 

-------

#### Špeciálne poďakovanie
Mgr. Ing. Matúš Jókay, PhD. - za hlavnú štruktúru programu.

-------


