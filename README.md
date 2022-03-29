# PPDS - Paralelné programovanie a distribuované systémy
![FEI](https://www.fei.stuba.sk/buxus/images/web/logoFEI.jpg)
## Cvičenie 6: Menej klasické synchronizačné problémy
#### Programovací jazyk: Python verzie 3.10.2
![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)
Program, ktorý demonštruje tvorbu molekuly vody z dvoch vodíkov a jedného kyslíka.
#### Ako spusiť programy
V prvom rade treba stiahnúť repozitár s príslušnými súbormi príkladov. Pričom je potrebné mať nainštalované vývojové prostredie pre programovací jazyk Python verzie 3.10.2. 

#### Dokumentácia
Repozitár sa skladá z dvoch úloh:
- Úloha: obsahuje jeden python program (problém tvorby vody)

##### Úloha - tvorba vody
Pri danej úlohe bola použitá štandardná trieda bariéry, ktorá bola použitá aj v prechádzajúcich cvičeniach, okrem toho sa program skladá z dvoch hlavných funkcií, ktoré reprezentujú vodík a kyslík.

```python
def oxygen(shared):
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
```
Pri oboch funkciách reprezentujúce dané prvy sa na začiatku prídava jeden prvok daného typu, pričom v triede Shared() je počítadlo daných prvkov, ktoré pri možnosti tvorby molekuly odpočíta príslušné hodnoty(2x vodík H a 1x kyslík O) a uvoľnia sa semafóry pre dané prvky. Následne sa spoja vo funkcií bond(), ktorá reprezentuje čas spájania do molekuly vody. 

Následne vo funkcií init_and_run(), sa vytvárajú dané vlákna prvkov vodíka kyslíka v nekonečnom cykle while. Pričom vytváranie prvkov daných vlákien je vytvorené tak, že sa vygeneruje náhodné číslo i, ktoré ak je párne vytvorí chemický prvkov z periodickej tabuľky O-kyslík, inak sa vytvorí prvkov H-vodík. Okrem toho sú tam aj pomocné počítadla pre lepšiu prehľadnosť pri výpise na konzole.

###### Výstup
Následne výstup z konzole vyzerá nasledovne:
```python
O alebo H
Celkovy pocet H:  0 # v prípade ak na konzole sa objaví H = H + 1
Celkovy pocet O:  0  # v prípade ak na konzole sa objaví O = O + 1
# Ak vznike voda sa vypíše: Vznikla voda
```

-------

#### Špeciálne poďakovanie
Mgr. Ing. Matúš Jókay, PhD. - za hlavnú štruktúru programu.

-------