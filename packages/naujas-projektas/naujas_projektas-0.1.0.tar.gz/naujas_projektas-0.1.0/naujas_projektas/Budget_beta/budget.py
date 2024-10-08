import pickle
import os
from naujas_projektas.Budget_beta.expense_record import ExpenseRecord
from naujas_projektas.Budget_beta.income_record import IncomeRecord

class Budget:
    def __init__(self):
        self.journal = self.load_journal()

    def load_journal(self):
        if os.path.exists("journal.pkl"):
            with open("journal.pkl", "rb") as f:
                return pickle.load(f)
        else:
            return []

    def save_journal(self):
        with open("journal.pkl", "wb") as f:
            pickle.dump(self.journal, f)

    def add_income_record(self, amount, sender, additional_info):
        if amount < 0:
            expenses = ExpenseRecord(abs(amount), "Liquidated","Bankruptcy")
            self.journal.append(expenses)
        else:
            income = IncomeRecord(amount, sender, additional_info)
            self.journal.append(income)
        self.save_journal()

    def add_expense_record(self, amount, payment_method, purchased_item_service):
        expenses = ExpenseRecord(amount, payment_method, purchased_item_service)
        self.journal.append(expenses)
        self.save_journal()

    def delete_record(self, index):
        if index < len(self.journal):
            del self.journal[index]
            self.save_journal()
        else:
            print("Invalid index.")

    def get_balance(self):
        income_sum = 0
        expense_sum = 0
        for record in self.journal:
            if isinstance(record, IncomeRecord):
                income_sum += record.amount
            elif isinstance(record, ExpenseRecord):
                expense_sum += record.amount
        print(f"Income sum: {income_sum}, Expense sum: {expense_sum}, Balance: {income_sum - expense_sum}")

    def display_report(self):
        column_width = 150
        format_string = f"|{{st1:>{column_width //2}}}|{{st2:<{column_width // 2}}}|"
        print("-" * column_width)
        for i, record in enumerate(self.journal, start=1):
            if isinstance(record, IncomeRecord):
                st1 = str(record)
                st2 = f"Sender: {record.sender}, Additional info: {record.additional_info}"
            elif isinstance(record, ExpenseRecord):
                st1 = str(record)
                st2 = f"Payment method: {record.payment_method}, Purchased item/service: {record.purchased_item_service}"
            print(f"{i}. {format_string.format(st1=st1, st2=st2)}")
        print("-" * column_width)