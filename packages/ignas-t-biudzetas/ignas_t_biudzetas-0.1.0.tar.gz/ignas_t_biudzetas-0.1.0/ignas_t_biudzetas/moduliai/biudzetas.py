from ignas_t_biudzetas.moduliai.pajamu_irasas import PajamuIrasas
from ignas_t_biudzetas.moduliai.islaidu_irasas import IslaiduIrasas

class Biudzetas:
    def __init__(self):
        self.zurnalas = []

    def prideti_pajamu_irasa(self,suma,siuntejas,papildoma_informacija):
        self.zurnalas.append(PajamuIrasas(suma,siuntejas,papildoma_informacija))

    def prideti_islaidu_irasa(self,suma,atsiskaitymo_budas,isigyta_preke_paslauga):
        self.zurnalas.append(IslaiduIrasas(suma,atsiskaitymo_budas,isigyta_preke_paslauga))

    def gauti_balansa(self):
        balansas = 0
        for irasas in self.zurnalas:
            if isinstance(irasas, PajamuIrasas):
                balansas += irasas.suma
            if isinstance(irasas, IslaiduIrasas):
                balansas -= irasas.suma
        return balansas
    
    def rodyti_balansa(self):
        print("\nBalansas: ")
        print(self.gauti_balansa())
    
    def rodyti_ataskaita(self):
         print("\nAtaskaita:")
         print("*"*90)
         for irasas in self.zurnalas:
            print(irasas)
         print("*"*90)