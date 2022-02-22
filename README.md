# PPDS - Paralelné programovanie a distribuované systémy
![FEI](https://www.fei.stuba.sk/buxus/images/web/logoFEI.jpg)
## Cvičenie 1: Úvod do PPDS, oboznámenie sa s prostredím
#### Programovací jazyk: Python verzie 3.10.2
![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)
 Jednoduchý program na demonštráciu využitia zámku v spolupráci s vláknami
#### Vlastnosti
- Obsahuje 3 rozdielne súbory na demonštráciu využitia zámku

#### Ako spusiť programy
V prvom rade treba stiahnúť repozitár s príslušnými súbormi príkladov(konkrétne sa jedná o 3 príklady využitia zámku). Pričom je potrebné mať nainštalované vývojové prostredie pre programovací jazyk Python verzie 3.10.2. 

#### Dokumentácia
Všetky 3 príklady súborov majú podobnú štruktúru okrem funkcie do_count.
##### Príklad 1
```python
def do_count(shared):
    shared.mutex.lock()
    while True:
        if shared.counter >= shared.end:
            break
        shared.elements[shared.counter] += 1
        sleep(randint(1, 10)/1000)
        shared.counter += 1
    shared.mutex.unlock()
```
V tomto príklade nie je zámok vo vnútri cyklu. Čo znamená, že program je vykonávaný len na jednom vlákne počas celého behu. Tento príklad nie je veľmi dobrou voľbou na demonštráciu paralelizmu na vláknach, ale výsledok je vzhľadom na zadanie uspokojový, pretože všetky prvky poľa majú hodnotu 1.
##### Príklad 2
```python
def do_count(shared):
    while shared.counter < shared.end-1:
        shared.mutex.lock()
        shared.elements[shared.counter] += 1
        sleep(randint(1, 10)/1000)
        shared.counter += 1
        shared.mutex.unlock()
```
V tomto príklade je zámok vo vnútri cyklu. Tento program prebieha paralelne počas celého behu. Ale nastáva tu jeden problém, že ak je veľkosť poľa 1, tak hodnota prvku bude 0. Tento problém je spôsobený rozsahom v cykle (hodnota shared.end-1). Inak pre ostatné veľkosti poľa by mal fungovať tento príklad správne.
##### Príklad 3
```python
def do_count(shared):
    while True:
        if shared.counter >= shared.end:
            break
        shared.mutex.lock()
        shared.elements[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()
        sleep(randint(1, 10)/1000)
```
V tomto príklade sa zámok nachádza vo vnútri cyklu a asi je to najlepší príklad zo všetkých troch na demonštráciu paralelizmu. V tomto príklade sa využívajú vlákna paralelne. Pričom funkcia sleep je daná na koniec z dôvodu, že ak by sa nachádzala v vnútri zámku, tak by prvý prvok poľa bol problém a mal by hodnotu 2. Jedným z riešení by mohlo byť, že by sa permanentne nastavila hodnota prvého prvku na 1 alebo by sa v podmienke if nastavila hodnota shared.counter+1, čo by mohlo spôsobovať problém v inej časti implementácie. 
#### Experimenty
Na experimentovanie bol použitý Counter, ktorý slúžil na vypísanie hodnôt prkov.
```python
from collections import Counter

counter = Counter(shared.elements)
print(counter.most_common())
```
Vo všetkých troch príklad bolo použité pole o veľkosti: 100, 1000, 10 000, 100 000 s nasledujúcimi výsledkami:
```python
[(1, 100)]
[(1, 1000)]
[(1, 10000)]
[(1, 100000)]
```
#### Špeciálne poďakovanie
Mgr. Ing. Matúš Jókay, PhD. - za hlavnú štruktúru programu.

-------

# PPDS - Parallel programming and distributed systems
![FEI](https://www.fei.stuba.sk/buxus/images/web/logoFEI.jpg)
## Exercise 1: Introduction to PPDS, familiarity with the environment
#### Programming language: Python version 3.10.2
![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)
A simple program to demonstrate the use of mutex in collaboration with threads
#### Features
- Contains 3 different files to demonstrate usage of mutex

#### Getting started
First of all, you need to download the repository with the appropriate sets of examples (specifically, there are 3 examples of using the lock). It is necessary to have a development environment for the Python programming language version 3.10.2 installed.

#### Documentation
All 3 files has similiar structure except function do_count.
##### Example 1
```python
def do_count(shared):
    shared.mutex.lock()
    while True:
        if shared.counter >= shared.end:
            break
        shared.elements[shared.counter] += 1
        sleep(randint(1, 10)/1000)
        shared.counter += 1
    shared.mutex.unlock()
```
In this example the mutex is outside the loop. This means that the program works only on one thread for all of the execution. This example is not properly very good option to demonstrate parallelism on threads, but the result of this is that the all elements of array have value 1.
##### Example 2
```python
def do_count(shared):
    while shared.counter < shared.end-1:
        shared.mutex.lock()
        shared.elements[shared.counter] += 1
        sleep(randint(1, 10)/1000)
        shared.counter += 1
        shared.mutex.unlock()
```
In this example is mutex inside the loop. In program we have parallelism on threads during the execution of program. But one problem in this example is that if the size of array is 1. The value of element is 0, the problem is due to range in loop.
##### Example 3
```python
def do_count(shared):
    while True:
        if shared.counter >= shared.end:
            break
        shared.mutex.lock()
        shared.elements[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()
        sleep(randint(1, 10)/1000)
```
In this example is mutex inside loop and this example works properly in parallelism. But if the sleep is inside the mutex it will be a problem with first element in array which will have value of 2. It could be solve if permanent the value of first element will be 1 or if the condition will be shared.counter+1, but this could make some other problems with implementation of this solution.

#### Experiments
For experimentation is used Counter for print the values of elements.
```python
from collections import Counter

counter = Counter(shared.elements)
print(counter.most_common())
```
In all examples was used array with size of: 100, 1000, 10 000, 100 000 with results:
```python
[(1, 100)]
[(1, 1000)]
[(1, 10000)]
[(1, 100000)]
```

#### Special thanks
Mgr. Ing. Matúš Jókay, PhD. - for main structure of the program.