from unicodedata import category

from tracker import ExpenseTracker
from expense import Expense, InvalidExpenseError

FILENAME = "expenses.json"

def main():
    tracker = ExpenseTracker()
    tracker.load_from_file(FILENAME)

    while True:
        print("add / list / report / delete / quit")
        choice = input("> ").lower()

        if choice == "quit":
            break

        if choice == "add":
            try:
                category = input("Category: ")
                amount = float(input("Amount: "))
                description = input("Description: ")
                #tracker.add_expense({"amount":{amount},"category":{category}, "description":{description}})
                tracker.add_expense(Expense(amount, category, description))
                tracker.save_to_file(FILENAME)
                print("Added.")
            except ValueError:
                print("Amount must be a number.")
            except InvalidExpenseError as error:
                print(f"Invalid expense: {error}")

        if choice == "list":
            tracker.list_expenses()

        if choice == "report":
            print(tracker.print_report())

        if choice == "delete":
            tracker.list_with_index()
            try:
                delete_choice = int(input("Which one to delete?"))

                if 0 <= delete_choice < len(tracker.expenses):
                    removed = tracker.expenses.pop(delete_choice)
                    tracker.save_to_file(FILENAME)
                    print(f"Deleted: {removed}")
                else:
                    print("No expense with that number")
            except ValueError:
                    print("Please enter a number")

if __name__ == "__main__":
    main()