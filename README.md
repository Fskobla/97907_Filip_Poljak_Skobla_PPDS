# PPDS - Paralelné programovanie a distribuované systémy
![FEI](https://www.fei.stuba.sk/buxus/images/web/logoFEI.jpg)
## Cvičenie 8: Asynchrónne programovanie
#### Programovací jazyk: Python verzie 3.10.2
![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)
Program, ktorý demonštruje tvorbu molekuly vody z dvoch vodíkov a jedného kyslíka.
#### Ako spusiť programy
V prvom rade treba stiahnúť repozitár s príslušnými súbormi príkladov. Pričom je potrebné mať nainštalované vývojové prostredie pre programovací jazyk Python verzie 3.10.2. 

#### Dokumentácia
Repozitár sa skladá z dvoch úloh:
- Úloha: obsahuje dva python program (synchrónna a asynchrónna verzia)

##### Úloha - synchrónna verzia
Zadanie: Študenti Matúš a Milan dostali na domácu úlohu 12 čísiel a mali zistiť, ktoré z nich sú prvočísla. Preto ako správni kamaráti sa rozhodli, že úlohu vypracujú spoločne, pričom sa striedali (najprv vypočítal jeden a potom druhý). Koľko bude trvať týmto dvom študentom vypracovanie úlohy, ak Matúš je lepší študent z matematiky (čas určenia jedného čísla mu trvá 1s) a Milanovi, ktorý potrebuje až 2s na určenie jedného čísla ?
```python
def result(student, numbers):
    while not numbers.empty():
        number = numbers.get()
        if(student == "Matúš"):
            count_time = 1
        else:
            count_time = 2
        start = time.perf_counter()
        time.sleep(count_time)
        end = time.perf_counter() - start

        for i in range(2, number):
            if(number % i == 0):
                print(f"Študent {student}: určil číslo {number},"
                      f"že nie je prvočíslo, trvalo mu to: {end}")
                break
            else:
                print(f"Študent {student}: určil číslo {number},"
                      f"je prvočíslo, trvalo mu to: {end}")
                break
        yield
```
Pri tejto úlohe bola využitá queue, v ktorej boli zadané dané čísla a postupne sa z nej vyberali. Pričom ak došiel na rad Matúš, tak čas trvania bol 1s a v prípade Milana 2s. Následne sa určilo, či číslo je prvočíslo alebo nie. A nakoniec sa v úlohe vypísal čas. 
###### Výsledok tohto príkladu by mal byť, vzhľadom na 12 čísiel a striedanie výpočtu študentov: 
6 čísiel x 1s (Matúš) + 6 čísiel x 2s (Milan) = 18s

##### Úloha - Asynchrónna verzia
Zadanie: Modifikujte úlohu synchrónnej verzie tak, že študenti Milan a Matúš budú naraz určovať dané čísla, či sú prvočísla. A určite, či by ušetrili čas, ktorý by mohli vynaložiť na iné aktivity.
```python
async def result(student, numbers, counter):
    while not numbers.empty():
        number = await numbers.get()
        if(student == "Matúš"):
            count_time = 1
            counter += 1
        else:
            count_time = 2
            counter += 1
        start = time.perf_counter()
        await asyncio.sleep(count_time)
        end = time.perf_counter() - start

        for i in range(2, number):
            if(number % i == 0):
                print(f"Študent {student}: určil číslo {number},"
                      f"že nie je prvočíslo, trvalo mu to: {end}")
                break
            else:
                print(f"Študent {student}: určil číslo {number},"
                      f"je prvočíslo, trvalo mu to: {end}")
                break
    print(f"Študent {student} určil celkovo {counter} čísiel")
```
Pri tejto úlohe sa využil asynchrónny prístup, ktorý umožnil, že študenti naraz určovali čísla, či sú alebo nie sú prvočísla.
Výsledok tohto príkladu by mal byť, vzhľadom na 12 čísiel a čas trvania:

8 čísiel x 1s (Matúš) = 8s
4 čísiel x 2s (Milan) = 8s
Vzhľadom k tomu, že aj jednému to trvá 8s aj druhému, tak výsledný čas bude 8s.
##### Synchrónna verzia vs Asynchrónna verzia
Na daných príkladov môžeme vidieť, že asynchrónna verzia je rýchlejšia, čo sa týka času, pretože sa súčasne vykonáva určovanie čísiel. 

-------

#### Špeciálne poďakovanie
Mgr. Ing. Matúš Jókay, PhD. - za hlavnú štruktúru programu.

-------