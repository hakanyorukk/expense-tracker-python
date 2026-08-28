from collections import defaultdict, Counter
from datetime import date

from expense import Expense

class ExpenseTracker:
    def __init__(self, storage):
        self.storage = storage
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def list_expenses(self):
        expenses = ""
        for expense in self.expenses:
            expenses+=f"{expense}\n"
        return expenses

    def total(self):
        total = 0
        for expense in self.expenses:
            total += expense.amount
        return total

    def __len__(self):
        return len(self.expenses)

    def __iter__(self):
        return iter(self.expenses)

    def __contains__(self, expense):
        return expense in self.expenses

    def __repr__(self):
        return f"ExpenseTracker({len(self)} expenses, total={self.total():.2f})"

    def save_to_file(self):

        # object to dict
        data = [e.to_dict() for e in self.expenses]
        self.storage.save(data)
        # with open(filename, "w") as file:
        #     json.dump(data, file)

    def load_from_file(self):

        self.expenses = []
        for d in self.storage.load():
            expense = Expense(d["amount"], d["category"], d.get("description", ""), date.fromisoformat(d["date"]))
            self.expenses.append(expense)
        return self.expenses

    def total_by_category(self):
        totals = {}
        for e in self.expenses:
            totals[e.category] = totals.get(e.category, 0) + e.amount
        return totals

    def average(self):
        if len(self) == 0:
            return 0
        return self.total() / len(self)

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
                f"Number of expenses: {len(self)}\n"
                f"Average expense: {self.average():.2f}\n\n"
                f"By category:\n")
        for category, amount in self.total_by_category().items():
            report += f"    {category}: {amount:.2f}\n"

        biggest = self.biggest_expense()
        if biggest is not None:
            report += f"\nBiggest expense: {biggest}"
        return report

    def list_with_index(self):
        for i, expense in enumerate(self.expenses):
            print(f"{i}: {expense}")


    def sorted_by_amount(self, descending=True):
        return sorted(self.expenses, key=lambda e: e.amount, reverse=descending)

    def sorted_by_date(self):
        return sorted(self.expenses, key=lambda e: e.date)

    def sorted_by_category_then_amount(self):
        return sorted(self.expenses, key=lambda i: (i.category, -i.amount))

    def count_by_category(self):
        return dict(Counter(e.category for e in self.expenses))

    def most_common_categories(self, n=3):
         return Counter(e.category for e in self.expenses).most_common(n)

    def by_month(self):
        by_month_list = defaultdict(list)
        for e in self.expenses:
            expense_date = f"{e.date.year}-{e.date.month:02d}"
            by_month_list[expense_date].append(e)
        return dict(by_month_list)

    def total_by_month(self):
        totals = defaultdict(float)
        for e in self.expenses:
            expense_month = f"{e.date.year}-{e.date.month:02d}"
            totals[expense_month] += e.amount
        return dict(totals)

    def summary(self):
        return {"sorted by amount": self.sorted_by_amount(),
               "sorted by date": self.sorted_by_date(),
               "sorted by category": self.sorted_by_category_then_amount(),
               "count by category": self.count_by_category(),
               "most common categories": self.most_common_categories(),
               "by month": self.by_month(),
               "total by month": self.total_by_month()}


