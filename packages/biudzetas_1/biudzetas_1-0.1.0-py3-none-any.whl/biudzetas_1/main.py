import biudzetas_1.Modules as budget

my_budget = budget.Budget()
################ SAMPLE DATA #############################
# my_budget.add_income(15.5,"Palūkanos")                  ##
# my_budget.add_income(1956,"Už paslaugas")               ##
# my_budget.add_expense(569.57, "Paskolos grąžinimas")    ##
# my_budget.add_income(155,"Pagal SF")                    ##
# my_budget.add_expense(39.99, "Už internetą")            ##
# my_budget.add_expense(28.9, "Už telefoną")              ##
# my_budget.add_income(15.5,"Palūkanos")                  ##
# my_budget.add_expense(850, "Nuoma")                     ##
# my_budget.add_expense(6580.22, "Atlyginimai")           ##
################ SAMPLE DATA #############################

while True:
    print("""
    Ką norite daryti?
    1 - Įvesti pajamas.
    2 - Įvesti išlaidas.
    3 - Parodyti balansą.
    4 - Parodyti pilną išrašą.
    0 - Išeiti iš programos
          """)
    match input():
        case "1":
            while True:
                amount = input("Įveskite pajamų sumą: ")

                try:
                    amount = float(amount)
                except:
                    print("Pajamos turi būti teigiamas skaičius")
                    continue

                sender = input("Įveskite pajamų paskirtį: ")
                extra = input("Iveskite papildoma info")

                entry = budget.IncomeEntry(amount,sender,extra)

                my_budget.add_income(entry)
                break
        
        case "2":
            while True:
                amount = input("Įveskite išlaidų sumą: ")

                try:
                    amount = float(amount)
                except:
                    print("Išlaidos turi būti teigiamas skaičius")
                    continue

                reference = input("Įveskite išlaidų paskirtį: ")
                payment_type = input("Iveskite mokejimo buda")

                entry = budget.ExpenseEntry(amount,reference, payment_type)
                
                my_budget.add_expense(entry)

                break
        
        case "3":
            print(f"Jūsų balansas: {my_budget.get_balance()}")

        case "4":
            my_budget.print_statement()
        
        case "0":
            break
        case _:
            print("Neatpažinta komanda")