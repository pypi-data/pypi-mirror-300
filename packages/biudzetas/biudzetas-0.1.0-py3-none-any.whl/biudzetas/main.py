from modulis.f_biudzetas import Biudzetas

import pickle

biudzetas = Biudzetas()

while True:
    pasirinkimas = int(input("\n[1] - Prideti"
          "\n[2] - Balancas"
          "\n[3] - Transactions"
          "\n[4] - Isaugoti ir iseiti"
          "\nPasirikimas: "))
    match pasirinkimas:
        case 1:
            suma = float(input("Pajamos/Islaidos: "))
            if suma > 0:
                tipas = "Pajamos"
                biudzetas.prideti_pajamu_irasa(suma, tipas)
            elif suma < 0:
                tipas = "Islaidos"
                biudzetas.prideti_pajamu_irasa(suma, tipas)
            else:
                print(f"Jus ivedete {suma}")
                continue
        case 2:
            print(f"Balancas: {biudzetas.parodyk_balanca()}")
        case 3:
            biudzetas.parodyk_ataiskaita()
        case 4:
            print("Irasimas baigtas!")
            with open("Ataskaita.pkl", "wb") as failas:
                pickle.dump(biudzetas, failas)
            
            with open("Ataskaita.pkl", "rb") as failas:
                nuskaitomas_pickle = pickle.load(failas)
                for el in nuskaitomas_pickle.zurnalas:
                    print("Suma:", el.suma)
                    print("Tipas:", el.tipas)
                    print("Balancas:", nuskaitomas_pickle.parodyk_balanca())
            break 