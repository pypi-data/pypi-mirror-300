from aiste_s_biudzetas.modules.biudzetas import Biudzetas

biudzetas = Biudzetas()

while True:
    pasirinkimas = int(input("1 - įvesti pajamas, \n2 - įvesti išlaidas, \n3 - gauti balansą, \n4 - parodyti ataskaitą, \n5 - išeiti iš programos\n"))

    if pasirinkimas == 1:
        suma = float(input("Įveskite pajamų sumą: "))
        siuntejas = input("Įveskite pajamų siuntėją: ")
        papildoma_informacija = input("Įveskite papildomą informaciją apie pajamas: ")
        biudzetas.prideti_pajamu_irasa(suma, siuntejas, papildoma_informacija)

    elif pasirinkimas == 2:
        suma = float(input("Įveskite išlaidų sumą: "))
        atsiskaitymo_budas = input("Įveskite atsiskaitymo būdą: ")
        isigyta_preke_paslauga = input("Įveskite įsigytą prekę/paslaugą: ")
        biudzetas.prideti_islaidu_irasa(suma, atsiskaitymo_budas, isigyta_preke_paslauga)

    elif pasirinkimas == 3:
        biudzetas.gauti_balansa()

    elif pasirinkimas == 4:
        biudzetas.parodyti_ataskaita()

    elif pasirinkimas == 5:
        print("Viso gero")
        break
