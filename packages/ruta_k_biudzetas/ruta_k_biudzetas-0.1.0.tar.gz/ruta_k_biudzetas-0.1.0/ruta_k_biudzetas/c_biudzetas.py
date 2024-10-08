from module import c_islaidu_irasas as isl
from module import c_pajamu_irasas as paj

class Biudzetas:
    def __init__(self):
        self.zurnalas = []
    def prideti_pajamu_irasa(self, suma: float, siuntejas, papildoma_informacija):
        pajamos = paj.PajamuIrasas(suma,siuntejas,papildoma_informacija)
        self.zurnalas.append(pajamos)
    def prideti_islaidu_irasa(self, suma: float, atsiskaitymo_budas,isigyta_preke_paslauga):
        islaidos = isl.IslaiduIrasas(suma, atsiskaitymo_budas, isigyta_preke_paslauga)
        self.zurnalas.append(islaidos)
    def gauti_balansa(self):
        balansas = 0
        for irasas in self.zurnalas:
            if isinstance(irasas,paj.PajamuIrasas):
                balansas+=irasas.suma
            if isinstance(irasas,isl.IslaiduIrasas):
                balansas-=irasas.suma
        print(f"Balansas: {balansas}")
    def parodyti_ataskaita(self):
        for irasas in self.zurnalas:
            print(f"{irasas.tipas}: {irasas.suma}")