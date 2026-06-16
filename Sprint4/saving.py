import customtkinter
from datetime import datetime

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
        self.menuGui()
        self.update_balance()

    def deposit(self):
        deposit = float(self.amount_entry.get())
        inv = Investment("Savings", deposit, rate_of_return=0.05)
        self.controller.savings_portfolio.append(inv)
        self.controller.history.append((datetime.now(), sum(inv.amount for inv in self.controller.savings_portfolio)))
        self.update_balance()

    def withdraw(self):
        withdraw = float(self.amount_entry.get())
        total = sum(inv.amount for inv in self.controller.savings_portfolio)

        if total >= withdraw:
            remaining = withdraw

            new_portfolio = []

            for inv in self.controller.portfolio:
                if remaining <= 0:
                    new_portfolio.append(inv)
                    continue
                elif inv.amount <= remaining:
                    remaining -= inv.amount
                else:
                    inv.amount -= remaining
                    remaining = 0
                    new_portfolio.append(inv)

            self.controller.savings_portfolio = new_portfolio   
            self.controller.history.append((datetime.now(), sum(inv.amount for inv in self.controller.savings_portfolio)))
        else:
            self.controller.history.append((datetime.now(), total))

        self.update_balance()

    def update_balance(self):
        balance = sum(inv.amount for inv in self.controller.savings_portfolio)
        self.balance_label.configure(text=f"Savings: ${balance:.2f}")

    def returnback(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    def menuGui(self):
        savings_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=1500, height=600)
        savings_frame.grid(row=1, column=0, rowspan=2, padx=20, pady=20, sticky="nsew")
        savings_frame.grid_columnconfigure(0, weight=1)
        savings_frame.grid_propagate(False)

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

        self.update_balance()
