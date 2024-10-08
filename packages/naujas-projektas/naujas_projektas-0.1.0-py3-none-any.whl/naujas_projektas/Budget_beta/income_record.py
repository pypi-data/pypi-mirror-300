from naujas_projektas.Budget_beta.record import Record

class IncomeRecord(Record):
    def __init__(self, amount, sender, additional_info):
        super().__init__(amount)
        self.sender = sender
        self.additional_info = additional_info

    def __str__(self):
        return f"Income: {self.amount}"