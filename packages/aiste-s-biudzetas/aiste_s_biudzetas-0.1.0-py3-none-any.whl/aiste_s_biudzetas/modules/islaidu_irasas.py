from aiste_s_biudzetas.modules.irasas import Irasas

class IslaiduIrasas(Irasas):
    def __init__(self, suma, atsiskaitymo_budas, isigyta_preke_paslauga):
        super().__init__(suma)
        self.atsiskaitymo_budas = atsiskaitymo_budas
        self.isigyta_preke_paslauga = isigyta_preke_paslauga

    def gauti_tipas(self):
        return "Išlaidos"

    def __str__(self):
        return f"Išlaidos - Suma: {self.suma}, Atsiskaitymo būdas: {self.atsiskaitymo_budas}, Įsigyta prekė/paslauga: {self.isigyta_preke_paslauga}"
