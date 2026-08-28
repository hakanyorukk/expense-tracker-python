from datetime import date
from expense import Expense
from tracker import ExpenseTracker
from storage import JsonStorage

t = ExpenseTracker(JsonStorage("ignore.json"))   # never saved, no file created
for a, c, d, dt in [
    (12.50, "food",      "lunch",    date(2026, 8, 1)),
    (40.00, "transport", "bus card", date(2026, 8, 3)),
    (8.20,  "food",      "coffee",   date(2026, 8, 3)),
    (60.00, "rent",      "august",   date(2026, 7, 28)),
    (25.00, "food",      "dinner",   date(2026, 7, 15)),
    (15.00, "transport", "taxi",     date(2026, 8, 10)),
]:
    t.add_expense(Expense(a, c, d, dt))

def desc(expenses):
    return [e.description for e in expenses]

checks = [
    ("T1 by_amount desc",   desc(t.sorted_by_amount()),
        ["august", "bus card", "dinner", "taxi", "lunch", "coffee"]),
    ("T1 by_amount asc",    desc(t.sorted_by_amount(descending=False)),
        ["coffee", "lunch", "taxi", "dinner", "bus card", "august"]),
    ("T2 by_date",          desc(t.sorted_by_date()),
        ["dinner", "august", "lunch", "bus card", "coffee", "taxi"]),
    ("T3 cat then amount",  [(e.category, e.amount) for e in t.sorted_by_category_then_amount()],
        [("food", 25.0), ("food", 12.5), ("food", 8.2),
         ("rent", 60.0), ("transport", 40.0), ("transport", 15.0)]),
    ("T4 count_by_category", t.count_by_category(),
        {"food": 3, "transport": 2, "rent": 1}),
    ("T4 is a plain dict",   type(t.count_by_category()).__name__, "dict"),
    ("T5 most_common(2)",    t.most_common_categories(2),
        [("food", 3), ("transport", 2)]),
    ("T6 by_month keys",     sorted(t.by_month()),
        ["2026-07", "2026-08"]),
    ("T6 august contents",   desc(t.by_month()["2026-08"]),
        ["lunch", "bus card", "coffee", "taxi"]),
    ("T6 is a plain dict",   type(t.by_month()).__name__, "dict"),
    ("T7 total_by_month",    {k: round(v, 2) for k, v in t.total_by_month().items()},
        {"2026-08": 75.70, "2026-07": 85.00}),
]

failed = 0
for name, got, want in checks:
    if got == want:
        print(f"PASS  {name}")
    else:
        failed += 1
        print(f"FAIL  {name}\n      got : {got}\n      want: {want}")
print(f"\n{len(checks) - failed}/{len(checks)} passed")