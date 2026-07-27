from datetime import date as date_type

class InvalidExpenseError(Exception):
    pass

class Expense:
    def __init__(self, amount, category, description="", date=None):
        if amount <= 0:
            raise InvalidExpenseError("Amount must be positive")
        self.amount = amount

        if category == "":
            raise InvalidExpenseError("Category is required")


        self.category = category
        self.description = description

        if date is None:
            date = date_type.today()
        self.date = date

    def __str__(self):
        return f"{self.date} | {self.category} | {self.amount:.2f} | {self.description}"

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": str(self.date)
        }


if __name__ == "__main__":
    e = Expense(12.50, "food", "lunch")
    print(e)
    try:
        bad = Expense(-5, "food")
    except InvalidExpenseError as error:
        print({error})