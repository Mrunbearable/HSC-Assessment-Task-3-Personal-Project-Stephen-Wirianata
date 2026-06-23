import customtkinter
from datetime import datetime
from userdata import save_users

class Investment:
    def __init__(self, name, amount, rate_of_return=0, years=0):
        self.name = name    
        self.amount = float(amount)
        self.rate_of_return = float(rate_of_return)
        self.years = years

    def compound_weekly(self, weeks=1):
        weekly_rate = self.rate_of_return / 52
        self.amount *= (1 + weekly_rate) ** weeks

class SavingsApp:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.active = True
        self.menuGui()
        self.update_balance()

    def deposit(self):
        deposit = float(self.amount_entry.get())

        if deposit > self.controller.mainportfolio:
            self.status.configure(text="Not enough cash.", text_color="red")
            return

        self.controller.mainportfolio -= deposit
        self.controller.frequentdatarefresh()   
        inv = Investment("Savings", deposit, rate_of_return=0.05)
        self.controller.savings_portfolio.append(inv)
        self.controller.users_data[self.controller.current_user_token]["history"].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.controller.totalaccountbalance()))
        self.controller.connectdatabase()
        self.update_balance()

    def withdraw(self):
        withdraw = float(self.amount_entry.get())
        total = sum(inv.amount for inv in self.controller.savings_portfolio)

        if withdraw > total:
            self.status.configure(text="Not enough funds in savings.", text_color="red")
            return

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

        self.controller.savings_portfolio = new_portfolio
        self.controller.mainportfolio += withdraw
        self.controller.frequentdatarefresh()
        self.controller.users_data[self.controller.current_user_token]["history"].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.controller.totalaccountbalance()))
        self.controller.connectdatabase()
        self.update_balance()

    def update_balance(self):
        balance = sum(inv.amount for inv in self.controller.savings_portfolio)
        self.balance.configure(text=f"Savings: ${balance:.2f}")

    def autorefresh_balance(self):
        if not self.active or not self.controller.running:
            return
        self.update_balance()
        if self.active and self.controller.running:
            self.app.after(10000, self.autorefresh_balance)

    def returnback(self):
        self.active = False
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    def menuGui(self):
        savings_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=1500, height=600)
        savings_frame.grid(row=1, column=0, rowspan=2, padx=20, pady=20, sticky="nsew")
        savings_frame.grid_columnconfigure(0, weight=1)
        savings_frame.grid_propagate(False)

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

        self.autorefresh_balance()