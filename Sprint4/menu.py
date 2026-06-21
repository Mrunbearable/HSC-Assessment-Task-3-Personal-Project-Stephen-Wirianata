import customtkinter
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InvestmentMenu:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.menuGui()

    def show_graph(self, frame):
        if not self.controller.history:
            return

        dates = [d for d, v in self.controller.history]
        values = [v for d, v in self.controller.history]

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

    def menuGui(self):
        self.controller.clear_window()
        date = datetime.now().strftime("%A, %d %B %Y")
        self.time = customtkinter.CTkLabel(self.app, text=date,font=("BahnSchrift", 18))
        self.time.place(relx=0.98, rely=0.02, anchor="ne")  
        self.left_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=600, height=650)
        self.left_frame.grid(row=1, column=0, rowspan=2, padx=(20, 10), pady=20, sticky="nsew")
        self.left_frame.grid_columnconfigure(0, weight=1)
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

        self.accountbalance = customtkinter.CTkLabel(self.left_frame, text="Account Balance: $0.00", font=("Banschrift", 16))
        self.accountbalance.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.graph_frame = customtkinter.CTkFrame(self.left_frame)
        self.graph_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.show_graph(self.graph_frame)

        self.update_balance()




        