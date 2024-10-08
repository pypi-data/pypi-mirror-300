class Irasas:
    def __init__(self, suma, tipas) -> None:
        self.suma = suma
        self.tipas = tipas
    def __repr__(self):
        return f"{self.tipas}: {self.suma} pinigu"
    def __str__(self):
        return f"{self.tipas}: {self.suma} pinigu"