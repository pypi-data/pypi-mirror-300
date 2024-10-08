from aliona_l_biudzetas.modulis.biudzetas import Biudzetas
ats = Biudzetas()
while True:
    pasirinkimas = int(input("Ivesti pajamas - 1\nIvesti islaidas - 2\nRodyti balansa - 3\nRodyti ataskaita - 4\nBaigti programa - 5\n "))
    if pasirinkimas == 1:
        suma = float(input("Iveskite pajamu suma: "))
        siuntejas = input("Iveskite siuntejo varda: ")
        papildoma_informacija = input("Iveskite info uz ka: ")
        ats.prideti_pajamas(suma, siuntejas, papildoma_informacija)
        print(f"Pridejote i pajamas: {suma} pinigu gauta is {siuntejas} uz {papildoma_informacija}")

    elif pasirinkimas == 2:
        suma = float(input("Iveskite islaidu suma: "))
        atsiskaitymo_budas = input("Iveskite atsiskaitymo buda: ")
        isigyta_preke_paslauga = input("Iveskite uz ka sumokejote: ")
        ats.prideti_islaidas(suma, atsiskaitymo_budas, isigyta_preke_paslauga)
        print(f"Pridejote i islaidas: {suma} pinigu, sumoketus {atsiskaitymo_budas} uz {isigyta_preke_paslauga}")

    elif pasirinkimas == 3:
        print(f"Pajamų/išlaidų balansas:{ats.gauti_balansa()} pinigu")
    elif pasirinkimas == 4:
        print(f"Ataskaita:")
        ats.parodyti_ataskaita()
    elif pasirinkimas == 5:
        print("Ivedimas baigtas")
        break
    else:
        print("Nedaryk man nervu ir ivesk tinkama skaiciu!")
