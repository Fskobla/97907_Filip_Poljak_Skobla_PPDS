# PPDS - Paralelné programovanie a distribuované systémy
![FEI](https://www.fei.stuba.sk/buxus/images/web/logoFEI.jpg)
## Cvičenie 9: CUDA pomocou Numba
#### Programovací jazyk: Python verzie 3.10.2
![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)
Program, ktorý demonštruje tvorbu molekuly vody z dvoch vodíkov a jedného kyslíka.
#### Ako spusiť programy
V prvom rade treba stiahnúť repozitár s príslušnými súbormi príkladov. Pričom je potrebné mať nainštalované vývojové prostredie pre programovací jazyk Python verzie 3.10.2. 

#### Dokumentácia
Repozitár sa skladá z dvoch úloh:
- Úloha: obsahuje jeden python program (CUDA) spolu s náhodným obrázkom pred demonštráciu (o veľkosti 32x32).

##### Úloha - CUDA
Pri tejto úlohe bola využitá 3D mriežka, ktorá reprezentuje dimenzie obrázka a obrázok o veľkosti 32x32x4(kde 4 = počet kanálov obrázka)- Následne bol upravený jas(sveteľnosť) o polovicu nižšiu.
```python
@cuda.jit
def my_kernel_3D(io_array):
    x, y, z = cuda.grid(3)
    io_array[x, y, z] = io_array[x, y, z] / 2
```
Na začiatku programu sa náhodne vybraný obrázok načíta, nastavia sa veľkosti blokov a vlákien. Potom prejde obrázok cez danú vyššie uvedenú funkciu a nakonci sa zapíše do súboru .png.

-------

#### Špeciálne poďakovanie
Mgr. Ing. Matúš Jókay, PhD. - za hlavnú štruktúru programu.

-------