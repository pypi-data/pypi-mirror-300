class Entry:
    def __init__(self, amount: float) -> None:
        self.amount = amount

class ExpenseEntry(Entry):
    def __init__(self, amount: float, reference: str, payment_type: str) -> None:
        super().__init__(amount)
        self.reference = reference
        self.payment_type = payment_type

class IncomeEntry(Entry):
    def __init__(self, amount: float, sender: str, extra: str) -> None:
        super().__init__(amount)
        self.sender = sender
        self.extra = extra