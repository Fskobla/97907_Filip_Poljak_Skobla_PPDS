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

##### Úloha 2
Pri danej úlohe bolo potrebné správne nakonfigurovať chod troch čidiel za pomoci ôsmich operátorov(monitorov).
```python
def init():
    ....
     for monitor_id in range(8):
        Thread(monitor, monitor_id, valid_data, turniket,
               ls_monitor, access_data)
    for cidlo_id in range(3):
        Thread(cidlo, cidlo_id, turniket, ls_cidlo, valid_data, access_data)
```
V úvode inicializácie som si vytvoril 8 monitorov a 3 čidlá, ktoré mali id od 0 po 2. Následne som do funkcie monitor pridal požadované rozsahy aktualizácií údajov od 40 po 50ms.
```python
def cidlo(cidlo_id, turniket, ls_cidlo, valid_data, access_data):
        ....
        if cidlo_id == 0 or cidlo_id == 1:
            trvanie_zapisu = randint(10, 20)/1000
        else:
            trvanie_zapisu = randint(20, 25)/1000
```
Potom jednou z dôležitých úloh bolo rozlíšiť čidlá na základe časovania aktualizácie údajov. 
Čidlo s ID 0 je v mojom prípade čidlo P a Čidlo s ID 1 je čidlo T - obe čidlá majú rozsah aktualizácie od 10 po 20ms (pričom na poradí ID nezáleží, t.j čidlo 0 môže byť čidlo P a opačne).
Nakoniec čidlo s ID 2 je čidlo H, pretože ako jediné malo rozsah aktualizácie údajov od 20 po 25ms.
Následne som v tejto úlohe upravil niektoré potrebné veci podľa požiadaviek, pričom som danú úlohu aj odskúšal na základe výpisov z konzoly.

###### Výpis z konzole
```python
cidlo" 02": pocet_zapisujucich_cidiel=00, trvanie_zapisu=0.024
cidlo" 00": pocet_zapisujucich_cidiel=01, trvanie_zapisu=0.012
cidlo" 01": pocet_zapisujucich_cidiel=02, trvanie_zapisu=0.017
monit "03": pocet_citajucich_monitorov=00
monit "06": pocet_citajucich_monitorov=01
monit "07": pocet_citajucich_monitorov=02
monit "05": pocet_citajucich_monitorov=03
monit "04": pocet_citajucich_monitorov=04
monit "01": pocet_citajucich_monitorov=05
monit "02": pocet_citajucich_monitorov=06
monit "00": pocet_citajucich_monitorov=07
cidlo" 00": pocet_zapisujucich_cidiel=00, trvanie_zapisu=0.020
cidlo" 01": pocet_zapisujucich_cidiel=01, trvanie_zapisu=0.010
cidlo" 02": pocet_zapisujucich_cidiel=02, trvanie_zapisu=0.025
```
Výpis z konzole vyzerá nasledovne. Pričom ID čidiel a monitorov nemusí byť postupne od 00 po 0x.

-------
##### Pseudokód
```python
DEFINE CLASS Lightswitch():
    DEFINE FUNCTION __init__(self):
        SET self.mutex TO Mutex()
        SET self.counter TO 0
        
    DEFINE FUNCTION lock(self, semaphore):
        self.mutex.lock()
        SET counter TO self.counter
        self.counter += 1
        IF self.counter EQUALS 1:
            semaphore.wait()
        self.mutex.unlock()
        RETURN counter

    DEFINE FUNCTION unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        IF self.counter EQUALS 0:
            semaphore.signal()
        self.mutex.unlock()

DEFINE FUNCTION init():
    SET access_data TO Semaphore(1)
    SET turniket TO Semaphore(1)
    SET ls_monitor TO Lightswitch()
    SET ls_cidlo TO Lightswitch()
    SET valid_data TO Event()
    
    FOR monitor_id IN range(8):
        Thread(monitor, monitor_id, valid_data, turniket,
               ls_monitor, access_data)
    FOR cidlo_id IN range(3):
        Thread(cidlo, cidlo_id, turniket, ls_cidlo, valid_data, access_data)

DEFINE FUNCTION monitor(monitor_id, valid_data, turniket, ls_monitor, access_data):
    valid_data.wait()
    WHILE True:
        sleep(randint(40, 50)/1000)
        turniket.wait()
        SET pocet_citajucich_monitorov TO ls_monitor.lock(access_data)
        turniket.signal()
        OUTPUT(f'monit "{monitor_id:02d}": '
              f'pocet_citajucich_monitorov={pocet_citajucich_monitorov:02d}')
        ls_monitor.unlock(access_data)
        
DEFINE FUNCTION cidlo(cidlo_id, turniket, ls_cidlo, valid_data, access_data):
    WHILE True:
        sleep(randint(50, 60)/1000)
        turniket.wait()
        turniket.signal()
        
        SET pocet_zapisujucich_cidiel TO ls_cidlo.lock(access_data)
        IF cidlo_id EQUALS 0 or cidlo_id EQUALS 1:
            SET trvanie_zapisu TO randint(10, 20)/1000
        ELSE:
            SET trvanie_zapisu TO randint(20, 25)/1000
        OUTPUT(f'cidlo" {cidlo_id:02d}": '
              f'pocet_zapisujucich_cidiel={pocet_zapisujucich_cidiel:02d}, '
              f'trvanie_zapisu={trvanie_zapisu:5.3f}')
        sleep(trvanie_zapisu)
        valid_data.signal()
        ls_cidlo.unlock(access_data)
        
IF __name__ EQUALS '__main__':
    init()
```


#### Špeciálne poďakovanie

https://gist.github.com/BlueNexus/599962d03a1b52a8d5f595dabd51dc34 - tvorba pseudokódu.

Mgr. Ing. Matúš Jókay, PhD. - za hlavnú štruktúru programu.

-------
