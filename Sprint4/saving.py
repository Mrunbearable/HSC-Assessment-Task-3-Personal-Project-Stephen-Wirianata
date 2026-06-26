# This is the saving investment oppurtunity, it operates on very simple code
# Imports customtkinter for code
# imports datetime to update history
import customtkinter
from datetime import datetime

#Creates the investment variables for the code to work
class Investment:
    def __init__(self, name, amount, rate_of_return=0, years=0):
        self.name = name    
        self.amount = float(amount)
        self.rate_of_return = float(rate_of_return)
        self.years = years

    # A interest compounding system to grow savings account
    def compound_weekly(self, weeks=1):
        weekly_rate = self.rate_of_return / 52
        self.amount *= (1 + weekly_rate) ** weeks

# Creates a savingapp class and connects it to main.py
class SavingsApp:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.menuGui()
        self.update_balance()

    # A function to deposit money from account balance, asks to input money
    def deposit(self):
        deposit = float(self.amount_entry.get())

        #Checks if there is enough cash in mainportfolio
        if deposit > self.controller.mainportfolio:
            print("Not enough cash")
            return

        # If successful, moves money from main portfolio and adds it to savings portofolio, adding interest to compound money
        # Updates history and balance
        self.controller.mainportfolio -= deposit
        inv = Investment("Savings", deposit, rate_of_return=0.05)
        self.controller.savings_portfolio.append(inv)
        self.controller.history.append((datetime.now(), self.controller.totalaccountbalance()))
        self.update_balance()

    # A withdraw function to take money out of savings portfolio, asking to input amount
    # Calculates total amount of money in saving portfolio
    def withdraw(self):
        withdraw = float(self.amount_entry.get())
        total = sum(inv.amount for inv in self.controller.savings_portfolio)

        # If not enough money in saving portfolio, prints error message in terminal
        if withdraw > total:
            print("Not enough savings")
            return

        # Calculate remaining amount of money to be sold
        remaining = withdraw
        # Create a new portfolio for remaining investment
        new_portfolio = []

        # A for loop to handle remaining investments
        # If all the money has been sold, no updates, if the money can be sold, remove the savings from portfolio, otherwise sell part of it and keep the rest, ensuring remaing savings have been sold
        for inv in self.controller.savings_portfolio:
            if remaining <= 0:
                new_portfolio.append(inv)
            elif inv.amount <= remaining:
                remaining -= inv.amount
            else:
                inv.amount -= remaining
                new_portfolio.append(inv)
                remaining = 0
                
        #Replaces and updates portfolio, updates balance and history
        self.controller.savings_portfolio = new_portfolio
        self.controller.mainportfolio += withdraw
        self.controller.history.append((datetime.now(), self.controller.totalaccountbalance()))
        self.update_balance()

    # A function to update account balance, updating savings text with current balance
    def update_balance(self):
        balance = sum(inv.amount for inv in self.controller.savings_portfolio)
        self.balance_label.configure(text=f"Savings: ${balance:.2f}")

    # A function to return to main menu, destorying widgets
    def returnback(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    # The GUI for the saving investment oppurtunity
    def menuGui(self):
        #Creates neccesary frames
        savings_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=1500, height=600)
        savings_frame.grid(row=1, column=0, rowspan=2, padx=20, pady=20, sticky="nsew")
        savings_frame.grid_columnconfigure(0, weight=1)
        savings_frame.grid_propagate(False)

        #Creates buttons, labels and entries
        self.balance_label = customtkinter.CTkLabel(savings_frame, text="Savings: $0.00", font=("Bahnschrift", 35))
        self.balance_label.grid(row=0, column=0, pady=(60, 10))

        enter_label = customtkinter.CTkLabel(savings_frame, text="Enter Currency", font=("Bahnschrift", 10))
        enter_label.grid(row=1, column=0, pady=10)

        interestrate_label = customtkinter.CTkLabel(savings_frame, text="Current interest rate: 5%", font=("Bahnschrift", 10))
        interestrate_label.grid(row=2, column=0, pady=10)

        self.amount_entry = customtkinter.CTkEntry(savings_frame, placeholder_text="Enter amount")
        self.amount_entry.grid(row=3, column=0, pady=10)

        savingsbutton_frame = customtkinter.CTkFrame(savings_frame, fg_color="#E2C3A9")
        savingsbutton_frame.grid(row=4, column=0, pady=(15, 60))

        deposit_button = customtkinter.CTkButton(savingsbutton_frame, text="Deposit", fg_color="#06402B", command=self.deposit)
        deposit_button.grid(row=0, column=0, padx=6)

        withdraw_button = customtkinter.CTkButton(savingsbutton_frame, text="Withdraw", fg_color="#06402B", command=self.withdraw)
        withdraw_button.grid(row=0, column=1, padx=6)

        returnback_button = customtkinter.CTkButton(self.app,text="Back to Main Menu", fg_color="#06402B", width=1500, height=30,command=self.returnback)
        returnback_button.place(x=20, y=640)

        #Frequently updates balance
        self.update_balance()
