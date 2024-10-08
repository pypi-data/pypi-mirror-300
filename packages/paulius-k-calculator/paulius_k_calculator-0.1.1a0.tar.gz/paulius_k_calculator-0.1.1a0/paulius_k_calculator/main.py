from  klase import Biudzetas

# Sukuriamas Biudzetas objektas
mano_biudzetas = Biudzetas()

# Programos valdymas
while True:
    
    print("\nPasirinkite veiksmą:")
    print("1. Pridėti pajamas")
    print("2. Pridėti išlaidas")
    print("3. Peržiūrėti biudžetą")
    print("4. Baigti programą")

    pasirinkimas = input("Įveskite pasirinkimą (1/2/3/4): ")

    if pasirinkimas == '1':
        suma = float(input("Įveskite pajamų sumą: "))
        mano_biudzetas.prideti_pajamas(suma)
    elif pasirinkimas == '2':
        suma = float(input("Įveskite išlaidų sumą: "))
        mano_biudzetas.prideti_islaidas(suma)
    elif pasirinkimas == '3':
        mano_biudzetas.parodyti_biudzeta()
    elif pasirinkimas == '4':
        print("Programa baigiama. Ačiū!")
        break
    else:
        print("Neteisingas pasirinkimas.")