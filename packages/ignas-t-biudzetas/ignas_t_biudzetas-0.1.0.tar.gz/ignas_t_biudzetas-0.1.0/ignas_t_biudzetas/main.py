"""
Sukurti minibiudžeto programą, kuri:
• Leistų vartotojui įvesti pajamas arba išlaidas (su "-" ženklu)
• Pajamas ir išlaidas saugotų sąraše, o sąrašą pickle faile (uždarius programą, įvesti duomenys nedingtų)
• Atvaizduotų jau įvestas pajamas ir išlaidas
• Atvaizduotų įvestų pajamų ir išlaidų balansą (sudėtų visas pajamas ir išlaidas)
Patarimas:
• import pickle

• Perdaryti biudžeto programą su klasėmis (iš 6 paskaitos) taip, 
kad visos klasės būtų skirtinguose failuose.
"""
from ignas_t_biudzetas.moduliai.biudzetas import Biudzetas
import pickle
import os

# class Irasas:

# class PajamuIrasas(Irasas):

# class IslaiduIrasas(Irasas):

# class Biudzetas:


vartotojo_biudzetas = Biudzetas()

if os.path.exists("biudzetas.pkl"):
    with open("biudzetas.pkl", "rb") as pickle_in:
        vartotojo_biudzetas = pickle.load(pickle_in)

while True:
    try:
        pasirinkimas = int(input("""
1 - Įvesti įrašą
2 - Parodyti pajamų/išlaidų balansą
3 - Parodyti biudžeto ataskaitą
4 - Išeiti
Pasirinkite: """))
    except:
        print("Netinkamas pasirinkimas. Įveskite skaičių 1-4.")
        continue
    
    if pasirinkimas == 1:
        try:
            suma = float(input("Įveskite sumą (teigiamą arba neigiamą): "))
        except:
            print("Klaida1")
            continue
        if suma >= 0:
            siuntejas = input("Įveskite siuntėją: ")
            papildoma_informacija = input("Įveskite papildomą informaciją: ")
            print("Įrašas pridėtas")
            vartotojo_biudzetas.prideti_pajamu_irasa(suma,siuntejas,papildoma_informacija)
        elif suma < 0:
            atsiskaitymo_budas = input("Įveskite atsiskaitymo būdą: ")
            isigyta_preke_paslauga = input("Įveskite įsigytą prekę ar paslaugą: ")

            print("Įrašas pridėtas")
            vartotojo_biudzetas.prideti_islaidu_irasa(suma,atsiskaitymo_budas,isigyta_preke_paslauga)

    if pasirinkimas == 2:
        #Pasirinkta rodyti balansa
        vartotojo_biudzetas.rodyti_balansa()

    if pasirinkimas == 3:
        #Pasirinkta rodyti ataskaita
        vartotojo_biudzetas.rodyti_ataskaita()

    if pasirinkimas == 4:
        print("Išeita")
        break

    with open("biudzetas.pkl", "wb") as pickle_out:
        pickle.dump(vartotojo_biudzetas, pickle_out)
