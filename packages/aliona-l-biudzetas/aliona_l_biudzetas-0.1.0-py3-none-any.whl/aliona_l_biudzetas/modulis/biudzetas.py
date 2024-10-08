from aliona_l_biudzetas.modulis.pajamos import PajamuIrasas
from aliona_l_biudzetas.modulis.islaidos import IslaiduIrasas
class Biudzetas:
    def __init__(self) -> None:
        self.zurnalas = []
    
    def prideti_pajamas(self, suma, siuntejas, papildoma_informacija):
        pajamos = PajamuIrasas(suma, siuntejas, papildoma_informacija)
        self.zurnalas.append(pajamos)

    def prideti_islaidas(self, suma, atsiskaitymo_budas, isigyta_preke_paslauga):
        islaidos = IslaiduIrasas(suma, atsiskaitymo_budas, isigyta_preke_paslauga)
        self.zurnalas.append(islaidos)

    def gauti_balansa(self):
        viso_pajamos = sum(irasa.suma for irasa in self.zurnalas if irasa.tipas == 'pajamos')
        viso_islaidos = sum(irasa.suma for irasa in self.zurnalas if irasa.tipas == 'islaidos')
        return viso_pajamos - viso_islaidos
        
    def parodyti_ataskaita(self):
        for i in self.zurnalas:
            print(i)

