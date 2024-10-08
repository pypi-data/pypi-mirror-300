from aiste_s_biudzetas.modules.irasas import Irasas

class PajamuIrasas(Irasas):
    def __init__(self, suma, siuntejas, papildoma_informacija):
        super().__init__(suma)
        self.siuntejas = siuntejas
        self.papildoma_informacija = papildoma_informacija

    def gauti_tipas(self):
        return "Pajamos"

    def __str__(self):
        return f"Pajamos - Suma: {self.suma}, Siuntėjas: {self.siuntejas}, Papildoma informacija: {self.papildoma_informacija}"
