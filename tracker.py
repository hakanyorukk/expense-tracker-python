from datetime import date

from expense import Expense, InvalidExpenseError
import json

class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def list_expenses(self):
        for expense in self.expenses:
            print(expense)

    def total(self):
        total = 0
        for expense in self.expenses:
            total += expense.amount
        return total

    def count(self):
        count = len(self.expenses)
        return count

    def save_to_file(self, filename):

        # object to dict
        data = [e.to_dict() for e in self.expenses]
        with open(filename, "w") as file:
            json.dump(data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        self.expenses = []
        for d in data:
            expense = Expense(d["amount"], d["category"], d["description"], d["date"])
            self.expenses.append(expense)
        return self.expenses
    def total_by_category(self):
        totals = {}
        for e in self.expenses:
            totals[e.category] = totals.get(e.category, 0) + e.amount
        return totals

    def average(self):
        if self.count() == 0:
            return 0
        return self.total() / self.count()

    def biggest_expense(self):
        if not self.expenses:
            return None
        biggest = self.expenses[0]
        for e in self.expenses:
            if e.amount > biggest.amount:
                biggest = e
        return biggest

    def print_report(self):
        report = (f"==== EXPENSE REPORT ====\n"
                f"Total spent: {self.total():.2f}\n"
                f"Number of expenses: {self.count()}\n"
                f"Average expense: {self.average():.2f}\n\n"
                f"By category:\n")
        for category, amount in self.total_by_category().items():
            report += f"    {category}: {amount:.2f}"

        biggest = self.biggest_expense()
        if biggest is not None:
            report += f"\nBiggest expense: {biggest}"
        return report

    def list_with_index(self):
        for i, expense in enumerate(self.expenses):
            print(f"{i}: {expense}")

if __name__ == "__main__":
    tracker = ExpenseTracker()
    print(tracker.load_from_file("expenses.json"))
    tracker.add_expense(Expense(12.50, "food", "lunch"))
    tracker.save_to_file("expenses.json")
    #tracker.list_expenses()
    #print(f"Total: {tracker.total():.2f}")
    #print(tracker.print_report())
