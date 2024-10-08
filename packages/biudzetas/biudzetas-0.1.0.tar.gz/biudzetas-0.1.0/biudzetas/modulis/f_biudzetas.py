from biudzetas.modulis.f_prideti_pajamas import Prideti_Pajamas
from biudzetas.modulis.f_prideti_islaidas import Prideti_Islaidas


class Biudzetas():
    def __init__(self) -> None:
        self.zurnalas = []

    def prideti_pajamu_irasa(self, suma: float, tipas: str) -> None:
        pajamu_irasas = Prideti_Pajamas(suma, tipas)
        self.zurnalas.append(pajamu_irasas)

    def prideti_islaidu_irasa(self, suma: float, tipas: str) -> None:
        islaidu_irasas = Prideti_Islaidas(suma, tipas)
        self.zurnalas.append(islaidu_irasas)

    def parodyk_balanca(self) -> float:
        balancas = 0
        for irasas in self.zurnalas:
            balancas += irasas.suma
        return balancas
    
    def parodyk_ataiskaita(self):
        for irasas in self.zurnalas:
            print(f"{irasas.tipas}: {irasas.suma}")

print("as veikiu, bet nesuprantu")