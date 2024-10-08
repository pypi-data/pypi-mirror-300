from paulius_l_biudzetas.module.biudzetas import Biudzetas

mano_biudzetas = Biudzetas()

while True:
    print("Pasirinkite veiksmą: ")
    print("1 - Įvesti pajamas")
    print("2 - Įvesti išlaidas")
    print("3 - Gauti balansą")
    print("4 - Gauti ataskaitą")
    print("0 - Išeiti iš programos")
    pasirinkimas = input()
    if pasirinkimas == "1":
        print("Įveskite pajamas: ")
        suma = int(input("Suma: "))
        siuntejas = input("Siuntėjas: ")
        papildoma_informacija = input("Papildoma informacija: ")
        mano_biudzetas.ivesti_pajamas(suma, siuntejas, papildoma_informacija)
        print("Pajamos įvestos sėkmingai!")
    if pasirinkimas == "2":
        print("Įveskite išlaidas: ")
        suma = int(input("Suma: "))
        atsiskaitymo_budas = input("Atsiskaitymo būdas: ")
        isigyta_preke_paslauga = input("Įsigyta prekė/paslauga: ")
        mano_biudzetas.ivesti_islaidas(suma, atsiskaitymo_budas, isigyta_preke_paslauga)
        print("Išlaidos įvestos sėkmingai!")
    if pasirinkimas == "3":
        print(f"Sąskaitos balansas: {mano_biudzetas.gauti_biudzeto_balansa()}")
    if pasirinkimas == "4":
        mano_biudzetas.gauti_ataskaita()
    if pasirinkimas == "0":
        break