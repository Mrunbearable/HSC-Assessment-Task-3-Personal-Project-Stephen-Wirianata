import customtkinter
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InvestmentMenu:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.active = True
        self.menuGui()

    def show_graph(self, frame):
        user_id = self.controller.current_user_token

        if not self.controller.users_data[user_id]["history"]:
            return

        history = self.controller.users_data[user_id]["history"][-10:]

        dates = [d for d, v in history]
        values = [v for d, v in history]

        fig, ax = plt.subplots(figsize=(6, 3))

        ax.plot(dates, values, marker="o", color="#06402B")
        ax.set_title("Portfolio Balance")
        ax.set_ylabel("Value")
        ax.grid(True)

        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_balance(self):
        balance = self.controller.totalaccountbalance()
        self.accountbalance.configure(text=f"Account Balance: ${balance:,.2f}")

    def update_breakdown(self):
        savings = sum(inv.amount for inv in self.controller.savings_portfolio)
        cod = sum(inv.amount for inv in self.controller.cod_portfolio)
        indexfund = sum(inv.amount for inv in self.controller.indexfund_portfolio)
        stocks = sum(inv.amount for inv in self.controller.stockmarket_portfolio)

        self.freecash.configure(text=f"Free Cash: ${self.controller.mainportfolio:,.2f}")
        self.savings.configure(text=f"Savings: ${savings:,.2f}")
        self.cod.configure(text=f"Certificate of Deposit: ${cod:,.2f}")
        self.indexfund.configure(text=f"Index Fund: ${indexfund:,.2f}")
        self.stocks.configure(text=f"Stock Market: ${stocks:,.2f}")

    def balancerefresh(self):
        if not self.active:
            return
        self.update_balance()
        self.update_breakdown()
        self.app.after(10000, self.balancerefresh)

    def display_userinfo(self):
        username = self.controller.current_user
        self.username.configure(text=f"Username: {username}")

    def graphrefresh(self):
        if not self.active:
            return

        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        self.show_graph(self.graph_frame)
        self.app.after(300000, self.graphrefresh)

    def logout(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_authenticationsystem()

    def exit(self):
        self.app.destroy()

    def menuGui(self):
        self.controller.clear_window()
        date = datetime.now().strftime("%A, %d %B %Y")
        self.time = customtkinter.CTkLabel(self.app, text=date,font=("BahnSchrift", 18))
        self.time.place(relx=0.98, rely=0.02, anchor="ne")  
        self.left_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=600, height=650)
        self.left_frame.grid(row=1, column=0, rowspan=2, padx=(20, 10), pady=20, sticky="nsew")
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_propagate(False)

        right_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=800, height=650)
        right_frame.grid(row=1, column=1, padx=(10, 20), pady=20, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_propagate(False)

        customtkinter.CTkLabel(self.app, font=("Bahnschrift", 45), text_color="#06402B", text="Smart Investments").grid(row=0, column=0, padx=20, pady=5, sticky="w")

        saving_button = customtkinter.CTkButton(right_frame,text="High Yield Savings Account", fg_color="#06402B", height=100,  command=self.controller.operate_savings)
        saving_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        certificatofdeposit_button = customtkinter.CTkButton(right_frame,text="Certificate Of Deposit", fg_color="#06402B", height=100, command=self.controller.operate_cod)
        certificatofdeposit_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")        
        indexfund_button = customtkinter.CTkButton(right_frame,text="Index Fund", fg_color="#06402B", height=100,  command=self.controller.operate_index)
        indexfund_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")        
        individualstocks_button = customtkinter.CTkButton(right_frame,text="Stock Market", fg_color="#06402B", height=100, command=self.controller.operate_stock)
        individualstocks_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        leaderboard_button = customtkinter.CTkButton(self.app, text="Leaderboard", fg_color="#06402B", width=120, command=self.controller.operate_leaderboard)
        leaderboard_button.place(relx=0.85, rely=0.02, anchor="ne")
        exit_button = customtkinter.CTkButton(self.app, text="Exit", fg_color="#06402B", width=120, command=self.exit)
        exit_button.place(relx=0.75, rely=0.02, anchor="ne")
        logout_button = customtkinter.CTkButton(self.app, text="Logout", fg_color="#06402B", width=120, command=self.logout)
        logout_button.place(relx=0.65, rely=0.02, anchor="ne")

        self.accountbalance = customtkinter.CTkLabel(self.left_frame, text="Account Balance: $0.00", font=("Banschrift", 16, "bold"))
        self.accountbalance.grid(row=2, column=0, padx=10, pady=(10, 4), sticky="w")

        self.username = customtkinter.CTkLabel(self.left_frame, text="Username: ", font=("Banschrift", 16))
        self.username.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")

        self.freecash = customtkinter.CTkLabel(self.left_frame, text="Free Cash: $0.00", font=("Banschrift", 14))
        self.freecash.grid(row=4, column=0, padx=10, pady=2, sticky="w")

        self.savings = customtkinter.CTkLabel(self.left_frame, text="Savings: $0.00", font=("Banschrift", 14))
        self.savings.grid(row=5, column=0, padx=10, pady=2, sticky="w")

        self.cod = customtkinter.CTkLabel(self.left_frame, text="Certificate of Deposit: $0.00", font=("Banschrift", 14))
        self.cod.grid(row=6, column=0, padx=10, pady=2, sticky="w")

        self.indexfund = customtkinter.CTkLabel(self.left_frame, text="Index Fund: $0.00", font=("Banschrift", 14))
        self.indexfund.grid(row=7, column=0, padx=10, pady=2, sticky="w")

        self.stocks = customtkinter.CTkLabel(self.left_frame, text="Stock Market: $0.00", font=("Banschrift", 14))
        self.stocks.grid(row=8, column=0, padx=10, pady=(2, 10), sticky="w")

        self.graph_frame = customtkinter.CTkFrame(self.left_frame)
        self.graph_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.display_userinfo()
        self.balancerefresh()
        self.graphrefresh()