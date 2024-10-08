from naujas_projektas.Budget_beta.record import Record

class ExpenseRecord(Record):
    def __init__(self, amount, payment_method, purchased_item_service):
        super().__init__(abs(amount))  
        self.payment_method = payment_method
        self.purchased_item_service = purchased_item_service

    def __str__(self):
        return f"Expenses: {self.amount}"