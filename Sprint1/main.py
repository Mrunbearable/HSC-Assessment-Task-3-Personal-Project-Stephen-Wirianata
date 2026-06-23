# Creates a dictionary to store the investment details, this is important for the app to function properly.
portfolio = []

#A function to calculate future value of investment, compounding function which is important for app purposes
def calculate_return(amount, rate_of_return, years):
    return amount * ((1 + rate_of_return/100) ** years)

# A Function to Add investment to portfolio
def add_investment():

    #User Inputs for name, float and rate of return  
    name = input("Enter Investment name: ")
    amount = float(input("Enter an investment amount: "))
    rate_of_return = float(input("Enter rate of return: "))

    # Adds these details to the specific investments and then prints that the investment was added successfully
    portfolio.append({"name": name, "amount": amount, "rate_of_return": rate_of_return})
    print(f"Investment {name} added successfully \n")

#A function to view portfolio, allowing user to manage and see all their investments
def view_portfolio():

    #If there is nothing in portfolio, it returns an empty portfolio message
    if not portfolio:
        print("your portfolio is empty")
        return
    
    #prints "Your Investments" 
    print("Your Investments")

    # A for loop is utilised to print out the details of each investment in the portfolio,the name, amount and rate of return.
    # The for loop is effective in saving code and making it more efficient
    for i, investment in enumerate(portfolio, start=1):
        print(f"{i}. {investment['name']}{investment['amount']}{investment['rate_of_return']}")

    print()

# A function to calculate returns of investments
def calculate_returns():

    #If there is nothing in portfolio, it returns an empty portfolio message
    if not portfolio:
        print("Your portfolio is empty \n")
        return

    # Asks the user to input number of years
    years = int(input("enter number of years"))
    print ("projected returns")

    # A for loop is utilised to calculate the future value of each investment in the portfolio using the calculate_return function,
    # Prints out the projected returns for each investment after the specified number of years.
    for investment in portfolio:
        future_value = calculate_return(investment['amount'], investment['rate_of_return'], years)
        print(f"{investment['name']}{investment['amount']} After {years} years: {future_value:.2f}")

    print()

# A function to remove an investment from the portfolio, organising the portfolio and allowing users to manage their investments effectively.
def remove_investment():

    #If there is nothing in portfolio, it returns an empty portfolio message    
    if not portfolio:
        print("Your portfolio is empty \n")
        return

    # Displays the current portfolio to the user, allowing them to see the investments and choose which one to remove
    view_portfolio()
    index = int(input("enter a number of the investment to remove: ")) - 1

    # Checks if the index is valid, if it is, it removes the investment from the portfolio and prints a success message, otherwise it prints an invalid selection message.
    if 0 <= index < len(portfolio):
        removed = portfolio.pop(index)
        print(f"Investment {removed['name']} removed successfully \n")
    else:
        print("Investment invalid selection \n")

# A function to view balance of the portfolio, allowing users to see the total value of their investments and manage their finances effectively.
def view_balance(): 

    #If there is nothing in portfolio, it returns an empty portfolio message
    if not portfolio:
        print("Your portfolio is empty \n")
        return

    # Sets Balance to 0
    balance = 0

    # A for loop is utilised to iterate through each investment in the portfolio and adds up the amount of each investment to calculate the total balance of the portfolio
    for investment in portfolio:
        balance += investment['amount']

    print(f"Total Portfolio Balance: {balance}\n")

# This is the menu function, essential for the navigation of the app, allowing users to choose what they want to do
def menu():
    #While loop used to continuously show the menu until the user decides to exit, allowing for multiple actions without restarting the app 
    while True:
        #Options to choose from
        view_balance()
        print("-----InvestmentApp menu-----")
        print("1. Add Investment")
        print("2. View portfolio")
        print("3. Calculate Returns")
        print("4. Remove Investment")
        print("5. Exit")

        #User inputs choice
        choice = input("choose an option:")

        #If Statements to guide the user from choice
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

# Runs the menu function to start the app
menu()
