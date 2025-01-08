from expense import Expense
import calendar
import datetime


def main():
    print(f"🎯 Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = float(input("💸 What is your monthly budget?: "))
    
    while True:
        #Get user input
        expense = get_user_expense()
        

        #write expense to file
        save_expense_to_file(expense, expense_file_path)

        more_expenses = input("😕 Do you have mor expenses to add? (yes/no): ").strip().lower()
        if more_expenses not in ["yes", "y"]:
            break

    #read file and summarize expenses
    summarize_expense(expense_file_path, budget)


def get_user_expense():
    print(f"🎯 Getting User Expense")
    
    while True:
        expense_name = input("Enter expense name: ").capitalize()
        if expense_name.strip().isalpha():
            break
        elif expense_name.strip() and not expense_name.isdigit():
            break
        else:
            print("❌ Invalid name. Please enter a valid expense name (letters or words).")
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            break
        except ValueError:
            print("❌ Invalid amount. Please enter a valid number.")
    

    expense_categories = [
        "🍔 Food", 
        "🏡 Home", 
        "🗃️  Work", 
        "🎉 Fun", 
        "✨ Miscellaneous"
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"    {i+1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: "))-1
        try:

            if selected_index in range(len(expense_categories)):
                selected_category= expense_categories[selected_index]
                new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
                return new_expense

            else:
                print("❌ Invalid Category. Please Try Again!")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")
        

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name}, {expense.amount}, {expense.category}\n")

def summarize_expense(expense_file_path, budget):
    print(f"🎯 Summarizing User Expense")
    expenses: list[Expense]=[]
    with open(expense_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            stripped_line = line.strip()
            expense_name, expense_amount, expense_category = stripped_line.split(",")
            line_expense = Expense(
                name=expense_name, 
                amount=float(expense_amount), 
                category=expense_category
                )
            
            expenses.append(line_expense)
    
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category 📈: ")
    for key, amount in amount_by_category.items():
        print(f"    {key}: ${amount:.2f}")

    total_spent = sum([expense.amount for expense in expenses])
    print(f"💵 Total Spent: ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    if remaining_budget < 0:
        print(f"😭 You've spent more than your budget by ${abs(remaining_budget):.2f}!")
    else:
        print(f"✅ Budget Remaining: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month -now.day
    print("📅 Remaining days in the current month:", remaining_days)
 
    daily_budget = remaining_budget / remaining_days
    print(f"👉 Budget Per Day: ${daily_budget:.2f}")

if __name__ == "__main__":
    main()