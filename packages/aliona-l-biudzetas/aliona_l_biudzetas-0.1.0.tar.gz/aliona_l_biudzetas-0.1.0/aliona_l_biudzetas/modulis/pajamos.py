from aliona_l_biudzetas.modulis.israsas import Irasas

class PajamuIrasas(Irasas):
    def __init__(self, suma, siuntejas, papildoma_informacija) -> None:
        super().__init__(suma, 'pajamos')
        self.siuntejas = siuntejas
        self.papildoma_informacija = papildoma_informacija
    def __str__(self):
        return f"Pajamu Irasas - Suma: {self.suma}, Siuntejas: {self.siuntejas}, Info: {self.papildoma_informacija}"