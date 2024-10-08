from aliona_l_biudzetas.modulis.israsas import Irasas
class IslaiduIrasas(Irasas):
    def __init__(self, suma, atsiskaitymo_budas, isigyta_preke_paslauga) -> None:
        super().__init__(suma, 'islaidos')
        self.atsiskaitymo_budas = atsiskaitymo_budas
        self.isigyta_preke_paslauga = isigyta_preke_paslauga
    def __str__(self):
        return f"Islaidu Irasas - Suma: {self.suma}, Atsiskaitymo budas: {self.atsiskaitymo_budas}, Uz ka sumoketa: {self.isigyta_preke_paslauga}"