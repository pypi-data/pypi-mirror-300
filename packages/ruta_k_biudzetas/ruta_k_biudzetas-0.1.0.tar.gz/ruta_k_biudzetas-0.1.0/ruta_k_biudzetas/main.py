from module import c_biudzetas

biudzetas = c_biudzetas.Biudzetas()
while True:
    veiksmas = int(input("Pasirinkite, kokį veiksmą norite atlikti:\n1 - įvesti pajamas\n2 - įvesti išlaidas\n3 - parodyti pajamų/išlaidų balansą\n4 - parodyti biudžeto ataskaitą\n0 - išeiti iš programos\n"))
    if veiksmas == 0:
        break
    elif veiksmas == 1:
        suma = float(input("Įveskite pajamų sumą:\n"))
        siuntejas = input("Įveskite siuntėją:\n")
        papildoma_informacija = input("Įveskite papildomą informaciją:\n")
        biudzetas.prideti_pajamu_irasa(suma,siuntejas,papildoma_informacija)
    elif veiksmas == 2:
        suma = float(input("Įveskite išlaidų sumą:\n"))
        atsiskaitymo_budas = input("Įveskite atsiskaitymo būdą:\n")
        isigyta_preke_paslauga = input("Nurodykite, kokia prekė ar paslauga įsigyta:\n")
        biudzetas.prideti_islaidu_irasa(suma,atsiskaitymo_budas,isigyta_preke_paslauga)
    elif veiksmas == 3:
        biudzetas.gauti_balansa()
    elif veiksmas == 4:
        biudzetas.parodyti_ataskaita()