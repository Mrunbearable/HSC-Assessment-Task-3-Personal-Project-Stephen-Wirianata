#This is the final savings, renamed to high yield saving account, it allows users to deposit money and let it compound interest over time
#Import customTkinter for GUI
#Import Datetime for handling updates
#Import Userdata to control different user account saving portfolios
import customtkinter
from datetime import datetime
from userdata import save_users

#Creates the investment class and defines essential variables
class Investment:
    def __init__(self, name, amount, rate_of_return=0, years=0):
        self.name = name    
        self.amount = float(amount)
        self.rate_of_return = float(rate_of_return)
        self.years = years

    # a function to compound interest
    def compound_weekly(self, weeks=1):
        weekly_rate = self.rate_of_return / 52
        self.amount *= (1 + weekly_rate) ** weeks

# Creates the savings app
class SavingsApp:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.active = True
        self.menuGui()
        self.update_balance()

    # A function to deposit money into the high yield saving account, user inputs a selected amount of money
    def deposit(self):
        #Try to convert the entry box text to a number. If the user typed letters or left it
        #blank, this catches the error instead of crashing the whole program
        try:
            deposit = float(self.amount_entry.get())
        except ValueError:
            self.status.configure(text="Enter a valid amount.", text_color="red")
            return

        #Error message if not enough of cash to deposit into savings from main portfolio
        if deposit > self.controller.mainportfolio:
            self.status.configure(text="Not enough cash.", text_color="red")
            return

        #If successfull, deposit removes money from main portfolio, adding investment to saving portfolio and updating neccessary information like history and balance
        #Allows money to compound over time
        self.controller.mainportfolio -= deposit
        self.controller.frequentdatarefresh()   
        inv = Investment("Savings", deposit, rate_of_return=0.05)
        self.controller.savings_portfolio.append(inv)
        self.controller.users_data[self.controller.current_user_token]["history"].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.controller.totalaccountbalance()))
        self.controller.connectdatabase()
        self.update_balance()

    # A function to withdraw money, user inputs money to withdraw
    def withdraw(self):
        #Try to convert the entry box text to a number. If the user typed letters or left it
        #blank, this catches the error instead of crashing the whole program
        try:
            withdraw = float(self.amount_entry.get())
        except ValueError:
            self.status.configure(text="Enter a valid amount.", text_color="red")
            return

        total = sum(inv.amount for inv in self.controller.savings_portfolio)

        # Error message if money wanting to withdraw is bigger than total money in savings portfolio
        if withdraw > total:
            self.status.configure(text="Not enough funds in savings.", text_color="red")
            return

        # A for loop to handle remaining investments
        # If all the money has been sold, no updates, if the money can be sold, remove the savings from portfolio, otherwise sell part of it and keep the rest, ensuring remaing savings have been sold
        remaining = withdraw
        new_portfolio = []

        for inv in self.controller.savings_portfolio:
            if remaining <= 0:
                new_portfolio.append(inv)
            elif inv.amount <= remaining:
                remaining -= inv.amount
            else:
                inv.amount -= remaining
                new_portfolio.append(inv)
                remaining = 0

        #Replaces and updates portfolio, updates balance and history for current user
        self.controller.savings_portfolio = new_portfolio
        self.controller.mainportfolio += withdraw
        self.controller.frequentdatarefresh()
        self.controller.users_data[self.controller.current_user_token]["history"].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.controller.totalaccountbalance()))
        self.controller.connectdatabase()
        self.update_balance()

    # A function to update account balance, updating savings text with current balance of current user
    def update_balance(self):
        balance = sum(inv.amount for inv in self.controller.savings_portfolio)
        self.balance.configure(text=f"Savings: ${balance:.2f}")

    # A function to automatically refresh the balance of the current user
    def autorefresh_balance(self):
        if not self.active or not self.controller.running:
            return
        self.update_balance()
        if self.active and self.controller.running:
            self.app.after(10000, self.autorefresh_balance)

    # A function to return to main menu, destroying widgets
    def returnback(self):
        self.active = False
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    #Creates the saving GUI, basically the same as the sprint 4 one, but font changes
    def menuGui(self):
        #Creates neccessary frames
        savings_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=1500, height=600)
        savings_frame.grid(row=1, column=0, rowspan=2, padx=20, pady=20, sticky="nsew")
        savings_frame.grid_columnconfigure(0, weight=1)
        savings_frame.grid_propagate(False)

        #Creates labels, buttons, enteries
        self.balance = customtkinter.CTkLabel(savings_frame, text="Savings: $0.00", font=("Bahnschrift", 35))
        self.balance.grid(row=0, column=0, pady=(60, 10))
        enter = customtkinter.CTkLabel(savings_frame, text="Enter Currency", font=("Bahnschrift", 25))
        enter.grid(row=1, column=0, pady=10)
        interestrate = customtkinter.CTkLabel(savings_frame, text="Current interest rate: 5%", font=("Bahnschrift", 25))
        interestrate.grid(row=2, column=0, pady=10)

        self.amount_entry = customtkinter.CTkEntry(savings_frame, placeholder_text="Enter amount")
        self.amount_entry.grid(row=3, column=0, pady=10)
        savingsbutton_frame = customtkinter.CTkFrame(savings_frame, fg_color="#E2C3A9")
        savingsbutton_frame.grid(row=4, column=0, pady=(15, 60))
        deposit_button = customtkinter.CTkButton(savingsbutton_frame, text="Deposit", fg_color="#06402B", command=self.deposit)
        deposit_button.grid(row=0, column=0, padx=6)
        withdraw_button = customtkinter.CTkButton(savingsbutton_frame, text="Withdraw", fg_color="#06402B", command=self.withdraw)
        withdraw_button.grid(row=0, column=1, padx=6)
        self.status = customtkinter.CTkLabel(savings_frame, text="")
        self.status.grid(row=5, column=0, pady=10)

        returnback_button = customtkinter.CTkButton(self.app,text="Back to Main Menu", fg_color="#06402B", width=1500, height=30,command=self.returnback)
        returnback_button.place(x=20, y=640)
        #Runs neccessary functions
        self.autorefresh_balance()