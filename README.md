Python command line expense tracker application.

## Features
- Add, list, and delete expenses (amount, category, description, date)
- Saves data to a JSON file
- Reports: total, average, biggest expense, breakdown by category and by month
- Sorting by amount, date, or category-then-amount
- Validation with a custom exception hierarchy

## Project structure
- expense.py:  the Expense model + validation
- tracker.py:  ExpenseTracker: manages expenses, persistence, and reports
- main.py:  interactive command-line menu
- storage.py: Storage abstract base class with JsonStorage and CsvStorage

## Usage

```
add / list / report / delete / import / summary / quit
> add
Category: food
Amount: 12.50
Description: lunch
Added.
```

