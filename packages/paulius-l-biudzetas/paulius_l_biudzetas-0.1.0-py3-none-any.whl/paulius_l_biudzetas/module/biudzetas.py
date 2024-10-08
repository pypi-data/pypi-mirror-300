from paulius_l_biudzetas.module.pajamu_irasas import PajamuIrasas
from paulius_l_biudzetas.module.islaidu_irasas import IslaiduIrasas

class Biudzetas():
    def __init__(self):
        self.zurnalas = []

    def ivesti_pajamas(self, suma, siuntejas, papildoma_informacija):
        pajamu_irasas = PajamuIrasas(suma, siuntejas, papildoma_informacija)
        self.zurnalas.append(pajamu_irasas)

    def ivesti_islaidas(self, suma, atsiskaitymo_budas, isigyta_preke_paslauga):
        islaidu_irasas = IslaiduIrasas(suma, atsiskaitymo_budas, isigyta_preke_paslauga)
        self.zurnalas.append(islaidu_irasas)

    def gauti_biudzeto_balansa(self):
        balansas = 0
        for irasas in self.zurnalas:
            if isinstance(irasas, PajamuIrasas):
                balansas += irasas.suma
            if isinstance(irasas, IslaiduIrasas):
                balansas -= irasas.suma
        return balansas

    def gauti_ataskaita(self):
        for irasas in self.zurnalas:
            if isinstance(irasas, PajamuIrasas):
                print(f"Pajamos: {irasas.suma} {irasas.siuntejas} {irasas.papildoma_info}")
            if isinstance(irasas, IslaiduIrasas):
                print(f"Išlaidos: {irasas.suma} {irasas.atsiskaitymo_budas} {irasas.isigyta_preke_paslauga}")
