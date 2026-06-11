class Investment:
    
    def __init__(self, name, amount, rate_of_return):
        self.name = name
        self.amount = amount
        self.rate_of_return = rate_of_return 

    def calculate_return(self, years):
        return self.amount * ((1 + self.rate_of_return/100) ** years)

class InvestmentApp:

    def __init__(self):
        self.portfolio = []

    def add_investment(self):
        
        name = input("Enter Investment name:")

        amount = float(input("Enter an investment amount"))

        rate_of_return = float(input("Enter rate of return:"))

        self.portfolio.append(Investment(name, amount, rate_of_return))

        print(f"Investment {name} added successfully \n")

    def view_portfolio(self):

        if not self.portfolio:

            print("your portfolio is empty")

            return
        
        print("Your Investments")

        for i, investment in enumerate(self.portfolio, start=1):
            print (f"{i}. {investment.name}{investment.amount}{investment.rate_of_return}")

        print()

    def calculate_returns(self):

        if not self.portfolio:

            print("Your portfolio is empty \n")

            return

        years = int(input("enter number of years"))

        print ("projected returns")

        for Investment in self.portfolio:

            future_value = investment.calculate_return(years)

            print(f"{investment.name}{investment.amount} After {years} years: {future_value:.2f}")

        print()

    def remove_investment(self):
        
        if not self.portfolio:

            print("Your portfolio is empty \n")

            return

        self.view_portfolio()

        index = int(input("enter a number of the investment to remove: ")) - 1

        if 0 <= index < len(self.portfolio):

            removed = self.portfolio.pop(index)

            print(f"Investment {removed.name} removed successfully \n")

        else:

            print("Investment invalid selection \n")

    def menu(self):
        
        while True:
            print("-----InvesmentApp menu-----")
            print("1. Add Investment")
            print("2. View portfolio")
            print("3. Calculate Returns")
            print("4. Remove Investment")
            print("5. Exit")

            choice = input("choose an option:")

            if choice == "1":
                self.add_investment()
            elif choice == "2":
                self.view_portfolio()
            elif choice == "3":
                self.calculate_returns()
            elif choice == "4":
                self.remove_investment()
            elif choice == "5":
                print("Exiting the App. Goodbye")
                break
            else:
                print("Invalid Choice, Please try again\n")

if __name__ == "__main__":

    app = InvestmentApp()
    app.menu()