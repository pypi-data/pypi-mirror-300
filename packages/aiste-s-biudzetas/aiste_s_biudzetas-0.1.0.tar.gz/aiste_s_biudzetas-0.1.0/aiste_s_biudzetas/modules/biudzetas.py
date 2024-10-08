from aiste_s_biudzetas.modules.pajamu_irasas import PajamuIrasas
from aiste_s_biudzetas.modules.islaidu_irasas import IslaiduIrasas

class Biudzetas:
    def __init__(self):
        self.zurnalas = []

    def prideti_pajamu_irasa(self, suma, siuntejas, papildoma_informacija):
        pajamos = PajamuIrasas(suma, siuntejas, papildoma_informacija)
        self.zurnalas.append(pajamos)

    def prideti_islaidu_irasa(self, suma, atsiskaitymo_budas, isigyta_preke_paslauga):
        islaidos = IslaiduIrasas(suma, atsiskaitymo_budas, isigyta_preke_paslauga)
        self.zurnalas.append(islaidos)

    def gauti_balansa(self):
        balansas = 0
        for irasas in self.zurnalas:
            if irasas.gauti_tipas() == "Pajamos":
                balansas += irasas.suma
            elif irasas.gauti_tipas() == "Išlaidos":
                balansas -= irasas.suma
        print(f"Balansas: {balansas}")

    def parodyti_ataskaita(self):
        for irasas in self.zurnalas:
            print(irasas)
