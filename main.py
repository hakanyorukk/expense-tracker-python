from tracker import ExpenseTracker
from expense import Expense, InvalidExpenseError
from storage import JsonStorage
FILENAME = "expenses.json"

def main():
    storage = JsonStorage("expenses.json")
    tracker = ExpenseTracker(storage)
    tracker.load_from_file()

    while True:
        print("add / list / report / delete / quit / summary / import")
        choice = input("> ").lower()

        if choice == "quit":
            break

        elif choice == "add":
            try:
                category = input("Category: ")
                amount = float(input("Amount: "))
                description = input("Description: ")
                #tracker.add_expense({"amount":{amount},"category":{category}, "description":{description}})
                tracker.add_expense(Expense(amount, category, description))
                tracker.save_to_file()
                print("Added.")
            except ValueError:
                print("Amount must be a number.")
            except InvalidExpenseError as error:
                print(f"Invalid expense: {error}")

        elif choice == "list":
            print(tracker.list_expenses())

        elif choice == "report":
            print(tracker.print_report())

        elif choice == "delete":
            tracker.list_with_index()
            try:
                delete_choice = int(input("Which one to delete?"))

                if 0 <= delete_choice < len(tracker.expenses):
                    removed = tracker.expenses.pop(delete_choice)
                    tracker.save_to_file()
                    print(f"Deleted: {removed}")
                else:
                    print("No expense with that number")
            except ValueError:
                    print("Please enter a number")

        elif choice == "summary":
            print(tracker.summary())

        elif choice == "import":
            path = input("File: ")
            try:
                with open(path, encoding="utf-8") as file:
                    added, errors = tracker.import_from_text(file)
                tracker.save_to_file()
                print(f"Imported {added}, skipped {len(errors)}")
                for err in errors:
                    print("  ", err)
            except FileNotFoundError:
                print(f"No such file: {path}")

if __name__ == "__main__":
    main()