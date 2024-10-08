from arturas_k_minibiudzetas.module.income import IncomeEntry
from arturas_k_minibiudzetas.module.expenses import ExpensesEntry

class Budget():
    def __init__(self) -> None:
        self.journal: list = []
        self.balance = 0                

    def add_incomes(self, sum_in: float, info=[]):
        entry = IncomeEntry()
        entry.set_type(1) 
        entry.set_sum(sum_in)
        entry.set_info(info[0], info[1])
        self.journal.append(entry)  

    def add_expenses(self, sum_out: float, info=[]):
        entry = ExpensesEntry()
        entry.set_type(-1)  
        entry.set_sum(-sum_out)  
        entry.set_info(info[0], info[1])
        self.journal.append(entry) 

    def get_balance(self):
        self.balance = 0
        for jr in self.journal:
            self.balance += jr.get_sum()  
        return "{:.2f}".format(self.balance)

    def show_info(self):
        if self.journal:
            result = "------------------------------------------------------------\n"
            result += "| Įrašo tipas  | Suma      | Informacija                   | \n"
            result += "------------------------------------------------------------\n"
            for jr in self.journal:
                if isinstance(jr, IncomeEntry):  
                    result += f"{jr.__str__()}i\n"
                elif isinstance(jr, ExpensesEntry): 
                    result += f"{jr.__str__()}e\n"
            result += "------------------------------------------------------------\n"
        else:
            result = "Duomenų nėra. Prašome įvesti!\n"
        return result

    def __repr__(self) -> str:
        if self.journal:
            result = "------------------------------------------------------------\n"
            result += "| Įrašo tipas  | Suma      | Informacija                   | \n"
            result += "------------------------------------------------------------\n"
            for jr in self.journal:
                result += f"{jr}\n"
            result += "------------------------------------------------------------\n"
        else:
            result = "Duomenų nėra. Prašome įvesti!\n"
        return result
