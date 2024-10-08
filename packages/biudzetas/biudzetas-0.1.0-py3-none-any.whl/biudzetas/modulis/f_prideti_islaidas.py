from .f_irasas import Irasas

class Prideti_Islaidas(Irasas):
    def __init__(self, suma: float, tipas: str) -> None:
        super().__init__(suma)
        self.tipas = tipas

    def __str__(self) -> str:
        return (f"{self.tipas}: {self.suma} $")