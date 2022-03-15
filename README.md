# PPDS - Paralelné programovanie a distribuované systémy
![FEI](https://www.fei.stuba.sk/buxus/images/web/logoFEI.jpg)
## Cvičenie 4: Večerajúci filozofi, Atómová elektráreň
#### Programovací jazyk: Python verzie 3.10.2
![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)
Programy, ktoré demonštrujú príklad večerajúcich filozofov a atómovej elektrárne.
#### Ako spusiť programy
V prvom rade treba stiahnúť repozitár s príslušnými súbormi príkladov. Pričom je potrebné mať nainštalované vývojové prostredie pre programovací jazyk Python verzie 3.10.2. 

#### Dokumentácia
Repozitár sa skladá z dvoch úloh:
- Úloha 1: obsahuje jeden python program (večerajúci filozofi)
- Úloha 2: obsahuje jeden python program (atómová elektráreň)

##### Úloha 1 
Pri danej úlohe sa riešil problém večerajúcich filozofov. A to tak, že bolo potrebné ich rozdeliť na ľavákov a pravákov(namiesto za pomoci čašníka). V danej úlohe sú základné funkcie ako: myslenie, jedenie, zobratie vidličiek a položenie vidličiek, tieto funkcie boli trochu len upravené, ale hlavný posun nastal v hlavnej funkcií main.
##### Večerajúci filozofi
```python
def main():
    forks = [Semaphore(1) for _ in range(PHIL_NUM)]
    
    random = randint(1, PHIL_NUM-1)
    p_type = [0]*(PHIL_NUM-random) + [1] * random

    philosophers = []
    for p_id in range(PHIL_NUM):
        right = (p_id + 1) % PHIL_NUM
        left = p_id

        if p_type[p_id]:
            philosophers.append(Thread(phil, forks, right, left, p_id))
        else:
            philosophers.append(Thread(phil, forks, left, right, p_id))

    for p in philosophers:
        p.join()
```
V prvom rade si vytvoríme počet vidličiek, ktorí zodpovedá počtu filozofov(globálna premenná). Následne si vytvoríme random číslo v rozsahu a na základe toho vytvoríme pole, ktoré má hodnoty 0 a 1. Tento princíp je taký, že na začiatku poľa sú 0 a následne podľa vygenerovanej hodnoty random sú 1, čo nám bude značiť ľavákov a pravákov, pričom je aspoň jeden z danej skupiny. Potom v cykle prechádzame a určíme si hodnoty ľavákov a pravákov a následne podľa núl a jednotiek z daného poľa ich vytvoríme.

#### Špeciálne poďakovanie
Mgr. Ing. Matúš Jókay, PhD. - za hlavnú štruktúru programu.

-------