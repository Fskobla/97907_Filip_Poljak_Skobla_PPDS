# PPDS - Paralelné programovanie a distribuované systémy
![FEI](https://www.fei.stuba.sk/buxus/images/web/logoFEI.jpg)
## Cvičenie 7: Asynchrónne programovanie v Pythone pomocou koprogramov (cez rozšírené generátory)
#### Programovací jazyk: Python verzie 3.10.2
![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)
Program, ktorý demonštruje tvorbu molekuly vody z dvoch vodíkov a jedného kyslíka.
#### Ako spusiť programy
V prvom rade treba stiahnúť repozitár s príslušnými súbormi príkladov. Pričom je potrebné mať nainštalované vývojové prostredie pre programovací jazyk Python verzie 3.10.2. 

#### Dokumentácia
Repozitár sa skladá z dvoch úloh:
- Úloha: obsahuje jeden python program (plánovač)

##### Úloha - plánovač
Pri danej úlohe bol vytvorený jednoduchý príklad plánovača koprogramov.
```python
class Planner(object):
    def __init__(self):
        self.task_array = []
        self.running = None

    def plan(self, task):
        self.task_array.append(task)

    def run(self):
        while self.task_array:
            actual_task = self.task_array[0]
            self.task_array.remove(self.task_array[0])
            actual_task.send(self.running)
            self.task_array.append(actual_task)
```
Pri tejto úlohe do task_array sa pridajú dané úlohy(tasky) toto prebieha v metóde plan(). Následne v metóde run() sa prehľadávajú v poli a vyberie sa prvý, ktorý sa následne odstráni a prída (dôvodom je posunutie pozície v poli).

###### Výstup
Následne výstup z konzole vyzerá nasledovne:
```python
FIRST TASK
SECOND TASK
THIRD TASK
```
Tento výstup sa opakuje v cykle, čiže sa to bude vypisovať pokiaľ sa činnosť programu nezastaví.

-------

#### Špeciálne poďakovanie
Mgr. Ing. Matúš Jókay, PhD. - za hlavnú štruktúru programu.

-------