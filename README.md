# Expense Tracker

Python command line expense tracker application.

## Features
- Add, list, and delete expenses (amount, category, description, date)
- Stroes date as a JSON file
- Spending reports: total, average, breakdown by category, biggest expense
- Input validation with custom exceptions

## Project structure
- `expense.py`:  the Expense model + validation
- `tracker.py`:  ExpenseTracker: manages expenses, persistence, and reports
- `main.py`:  interactive command-line menu

