import csv
from datetime import datetime
# Function to get the customer's file name based on their ID
def get_filename(customer_id):
    return f"{customer_id}.csv"

# Load expenses from the customer's CSV file
def load_expenses(customer_id):
    expenses = []
    filename = get_filename(customer_id)
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["amount"] = float(row["amount"])  # Convert amount back to float
                expenses.append(row)
    except FileNotFoundError:
        pass  # If the file doesn't exist, just return an empty list
    return expenses

# Save expenses to the customer's CSV file
def save_expenses(customer_id, expenses):
    filename = get_filename(customer_id)
    with open(filename, "a", newline="") as file:
        fieldnames = ["date", "category", "description", "amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # If the file is empty, write the header
        if file.tell() == 0:  # Check if file is empty
            writer.writeheader()
        
        writer.writerows(expenses)

# Add a new expense
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

# View all expenses
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

# Generate a summary report
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

# Main function to run the tracker
def main():
    # Ask for the customer ID (person's unique identifier)
    customer_id = input("Enter your Customer ID: ").strip()
    
    # Load the customer's expenses from the corresponding file
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
