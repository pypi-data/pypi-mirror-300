from pirmas_projektas.Biudzetas import Biudzetas
from pirmas_projektas.failo_sukurimas import parodyti_biudzeta, saugoti_biudzeta

def main():
    biudzetas = parodyti_biudzeta()
    if biudzetas is None:
        biudzetas = Biudzetas()
    while True:
        print("\nBiudžeto programa")
        print("[1] Įvesti pajamas")
        print("[2] Įvesti išlaidas")
        print("[3] Parodyti biudžetą")
        print("[4] Parodyti balansą")
        print("[5] Išeiti")
        pasirinkimas = input("Įveskite pasirinkimą: ")
        if pasirinkimas == "1":
            pajamu_suma = float(input("Įveskite pajamų sumą: "))
            biudzetas.ivesti_pajamas(pajamu_suma)
            saugoti_biudzeta(biudzetas)
        elif pasirinkimas == "2":
            islaidu_suma = float(input("Įveskite išlaidų sumą: "))
            biudzetas.ivesti_islaidas(islaidu_suma)
            saugoti_biudzeta(biudzetas)
        elif pasirinkimas == "3":
            biudzetas.parodyti_biudzeta()
        elif pasirinkimas == "4":
            biudzetas.parodyti_balansa()
        elif pasirinkimas == "5":
            saugoti_biudzeta(biudzetas)
            break
        else:
            print("Neteisingas pasirinkimas. Prašome bandyti dar kartą.")

if __name__ == "__main__":
    main()