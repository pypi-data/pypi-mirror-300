from biudzetas_1.Modules import IncomeEntry, ExpenseEntry
from biudzetas_1.Modules import Entry
class Budget:
    def __init__(self, journal: list[Entry] = []) -> None:
        self.journal = journal

    def add_income(self, entry: IncomeEntry):
        self.journal.append(entry)
    
    def add_expense(self, entry: ExpenseEntry):
        self.journal.append(entry)

    def get_balance(self):
        balance = 0
        for entry in self.journal:
            if isinstance(entry, IncomeEntry):
                balance += entry.amount
            else:
                balance -= entry.amount
        return balance
    
    # def statement(self):
    #     statement = []
    #     i = 1
    #     for entry in self.journal:
    #         if entry.is_income:
    #             i = 1
    #         else:
    #             i = -1
    #     statement.append({"Paskirtis":entry.reference,"Suma:": entry.amount*i})

    #     return round(statement,2)
    
    def print_statement(self):
        if self.journal:
            incomes = []
            expenses = []
            for entry in self.journal:
                if isinstance(entry,IncomeEntry):
                    # print("-"*51)
                    # print(f"{'PASKIRTIS':<30}|{'SUMA':>20}")
                    # print("-"*51)
                    incomes.append(entry)
                else:
                    expenses.append(entry)
            if incomes:
                print("-"*51)
                print(f"{'SIUNTEJAS':<30}|{'PAPILDOMA INFO':<30}|{'SUMA':>20}")
                print("-"*51)
                for income in incomes:
                    print(f"{income.sender:<30}|{income.extra:<30}|{income.amount:>20}")

            if expenses:
                print("-"*51)
                print(f"{'PASKIRTIS':<30}|{'MOKEJIMO BUDAS':<30}|{'SUMA':>20}")
                print("-"*51)
                for expense in expenses:
                    print(f"{expense.reference:<30}|{expense.payment_type:<30}|{expense.amount*-1:>20}")

            print("-"*51)
            print(f"{'BALANSAS:':>30}|{self.get_balance():>20}")
            print("-"*51)
        else:
            print("Nėra jokių įrašų")