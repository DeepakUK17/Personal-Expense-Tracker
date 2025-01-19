import csv
from datetime import datetime
def get_filename(customer_id):
    return f"{customer_id}.csv"
def load_expenses(customer_id):
    expenses = []
    filename = get_filename(customer_id)
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["amount"] = float(row["amount"])
                expenses.append(row)
    except FileNotFoundError:
        pass
    return expenses
def save_expenses(customer_id, expenses):
    filename = get_filename(customer_id)
    with open(filename, "a", newline="") as file:
        fieldnames = ["date", "category", "description", "amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerows(expenses)
def add_expense(customer_id, expenses):
    category = input("Enter expense category (e.g., Food, Transport, Shopping): ").strip()
    description = input("Enter expense description: ").strip()
    try:
        amount = float(input("Enter expense amount: "))
    except ValueError:
        print("Invalid amount! Please enter a number.")
        return
    expense = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "category": category,
        "description": description,
        "amount": amount
    }
    expenses.append(expense)
    save_expenses(customer_id, expenses)
    print("Expense added successfully!")
def view_expenses(expenses):
    if not expenses:
        print("No expenses to show.")
        return
    print("\n--- EXPENSES ---")
    for expense in expenses:
        print(f"Date: {expense['date']}")
        print(f"Category: {expense['category']}")
        print(f"Description: {expense['description']}")
        print(f"Amount: ₹{expense['amount']}")
        print("-" * 40)
def generate_report(expenses):
    if not expenses:
        print("No expenses to report.")
        return
    total_expenses = sum(expense["amount"] for expense in expenses)
    category_totals = {}
    for expense in expenses:
        category_totals[expense["category"]] = category_totals.get(expense["category"], 0) + expense["amount"]
    print("\n--- EXPENSE REPORT ---")
    print(f"Total Expenses: ₹{total_expenses:.2f}")
    print("Expenses by Category:")
    for category, total in category_totals.items():
        percentage = (total / total_expenses) * 100
        print(f"  - {category}: ₹{total:.2f} ({percentage:.1f}%)")
    print("-" * 40)
def main():
    customer_id = input("Enter your Customer ID: ").strip()
    expenses = load_expenses(customer_id)
    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Generate Report")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_expense(customer_id, expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            generate_report(expenses)
        elif choice == "4":
            print("Thank you for using the Personal Expense Tracker!")
            break
        else:
            print("Invalid choice! Please try again.")
if __name__ == "__main__":
    main()