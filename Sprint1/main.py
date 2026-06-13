portfolio = []

def calculate_return(amount, rate_of_return, years):
    return amount * ((1 + rate_of_return/100) ** years)

def add_investment():
        
    name = input("Enter Investment name: ")
    amount = float(input("Enter an investment amount: "))
    rate_of_return = float(input("Enter rate of return: "))

    portfolio.append({"name": name, "amount": amount, "rate_of_return": rate_of_return})
    print(f"Investment {name} added successfully \n")

def view_portfolio():

    if not portfolio:
        print("your portfolio is empty")
        return
        
    print("Your Investments")

    for i, investment in enumerate(portfolio, start=1):
        print(f"{i}. {investment['name']}{investment['amount']}{investment['rate_of_return']}")

    print()

def calculate_returns():

    if not portfolio:
        print("Your portfolio is empty \n")
        return

    years = int(input("enter number of years"))
    print ("projected returns")

    for investment in portfolio:
        future_value = calculate_return(investment['amount'], investment['rate_of_return'], years)
        print(f"{investment['name']}{investment['amount']} After {years} years: {future_value:.2f}")

    print()

def remove_investment():
        
    if not portfolio:
        print("Your portfolio is empty \n")
        return

    view_portfolio()
    index = int(input("enter a number of the investment to remove: ")) - 1

    if 0 <= index < len(portfolio):
        removed = portfolio.pop(index)
        print(f"Investment {removed['name']} removed successfully \n")
    else:
        print("Investment invalid selection \n")

def view_balance():

    if not portfolio:
        print("Your portfolio is empty \n")
        return

    balance = 0

    for investment in portfolio:
        balance += investment['amount']

    print(f"Total Portfolio Balance: {balance}\n")

def menu():
        
    while True:
        view_balance()
        print("-----InvestmentApp menu-----")
        print("1. Add Investment")
        print("2. View portfolio")
        print("3. Calculate Returns")
        print("4. Remove Investment")
        print("5. Exit")

        choice = input("choose an option:")

        if choice == "1":
            add_investment()
        elif choice == "2":
            view_portfolio()
        elif choice == "3":
            calculate_returns()
        elif choice == "4":
            remove_investment()
        elif choice == "5":
            print("Exiting the App. Goodbye")
            break
        else:
            print("Invalid Choice, Please try again\n")
menu()
