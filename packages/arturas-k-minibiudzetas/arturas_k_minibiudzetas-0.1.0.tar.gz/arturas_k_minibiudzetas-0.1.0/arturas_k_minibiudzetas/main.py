import pickle
import arturas_k_minibiudzetas.module.budget as biudzetas
import os

bd = biudzetas.Budget()

def input_incomes_or_expenses(Budget, in_list: list = []):
    if in_list:
        for i in in_list:
            if i[0] > 0:
                Budget.add_incomes(float(i[0]), i[1])
            elif i[0] < 0:
                Budget.add_expenses(float(i[0]), i[1]) 
    else:
        msg = "\nPridėkite įrašus:\n"
        msg += " +SUMA : pajamos:\n"
        msg += " -SUMA : išlaidos:\n"
        msg += "     i : išeiti iš įvedimo"
        print(msg)
        while True:
            str_in = input(" -> ")
            if str_in == "i":
                break
            try:
                tmp_sum = float(str_in)
            except ValueError:
                print("Netinkama suma! Bandykite dar kartą.")
                print(msg)
                continue
            if tmp_sum > 0:
                Budget.add_incomes(tmp_sum, (input(" Siuntėjas: "), input(" Papildoma informacija: ")))
            elif tmp_sum < 0:
                Budget.add_expenses(tmp_sum, (input(" Mokėjimo būdas: "), input(" Paskirtis: "))) 
            else:
                print("Įveskite ne nulį.")
                print(msg)


journal_entries = [
    (800, ("Darbdavys", "Atlyginimas")), 
    (-11.3, ("Mokėjimas kortele", "Prekė")),
    (-150, ("Pavedimu", "Paslauga")),
    (-35, ("Grynais", "Paslauga")),
    (200, ("Darbdavys", "Avansas")),
    (-38.49, ("Mokėjimas kortele", "Prekė")),
    (-0.99, ("Mokėjimas kortele", "Prekė")),
    (-55.99, ("Mokėjimas kortele", "Prekė")),
    (-10, ("Mokėjimas kortele", "Prekė")),
    (-4, ("Mokėjimas kortele", "Prekė"))
]

msg = "\nPasirinkite funkcijas:\n"
msg += " pr   : pridėti pajamas/išlaidas\n"
msg += " bl   : rodyti balansą\n"
msg += " at   : rodyti pilną ataskaitą\n"
msg += " test : importuoti testinius duomenis\n"
msg += " ins  : ataskaita su isinstance()\n"
msg += " i    : išeiti iš programos"

print(msg)


path = "biudzetas.pkl"
if os.path.exists(path):
    with open(path, "rb") as failas:
        bd = pickle.load(failas)

while True:
    str_in = input(" -> ")
    if str_in == "i":
        with open(path, "wb") as failas:
            pickle.dump(bd, failas) 
        print("Programa baigta ir biudžetas išsaugotas.")
        break
    elif str_in == "pr":
        input_incomes_or_expenses(bd)
        print(msg)
    elif str_in == "bl":
        print(f"\nPajamų / Išlaidų balansas: {bd.get_balance()}\n")
    elif str_in == "at":
        print(bd)
    elif str_in == "test":
        bd.journal = []  
        input_incomes_or_expenses(bd, journal_entries)
        print(bd, "Testiniai duomenys suimportuoti!\n")
    elif str_in == "ins":
        print(bd.show_info())
    else:
        print(msg)
