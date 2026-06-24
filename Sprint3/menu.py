#This is the menu, will be improved soon
# Imports customtkinter for the GUI
# Imports datetime to handle history updates
import customtkinter
from datetime import datetime
# Matplotlib important for creating the required graphs for this project
# Choose matplotlib because it is pretty effective and is the most convienient
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#A class for the investment menu, a controller is used to go back and forth between interfaces
class InvestmentMenu:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.menuGui()
    
    # Creates a Graph, Based on the available data, if no history no graph
    def show_graph(self, frame):
        if not self.controller.history:
            return

        dates = [d for d, v in self.controller.history]
        values = [v for d, v in self.controller.history]

        fig, ax = plt.subplots(figsize=(6, 3))

        ax.plot(dates, values, marker="o", color="#06402B")
        ax.set_title("Portfolio Balance")
        ax.set_ylabel("Value ($)")
        ax.grid(True)

        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # A function to update balance
    def update_balance(self):
        balance = sum(inv.amount for inv in self.controller.portfolio)
        self.accountbalance.configure(text=f"Account Balance: ${balance:,.2f}")

    #This is the GUI for the menu
    # Datetime is used to show current date, i thought it would be interesting to put datetime, so it really set the vibe of investing
    def menuGui(self):
        self.controller.clear_window()
        date = datetime.now().strftime("%A, %d %B %Y")
        self.time = customtkinter.CTkLabel(self.app, text=date,font=("BahnSchrift", 18))
        self.time.place(relx=0.98, rely=0.02, anchor="ne")  

        #Framing
        self.left_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=600, height=650)
        self.left_frame.grid(row=1, column=0, rowspan=2, padx=(20, 10), pady=20, sticky="nsew")
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_propagate(False)

        right_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=800, height=650)
        right_frame.grid(row=1, column=1, padx=(10, 20), pady=20, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_propagate(False)

        #Buttons, labels and more
        customtkinter.CTkLabel(self.app, font=("Bahnschrift", 45), text_color="#06402B", text="Smart Investments").grid(row=0, column=0, padx=20, pady=5, sticky="w")

        saving_button = customtkinter.CTkButton(right_frame,text="Saving Account", fg_color="#06402B", height=100)
        saving_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        certificatofdeposit_button = customtkinter.CTkButton(right_frame,text="Certificate Of Deposit", fg_color="#06402B", height=100, command=self.controller.operate_investment)
        certificatofdeposit_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")        
        indexfund_button = customtkinter.CTkButton(right_frame,text="Index Fund", fg_color="#06402B", height=100)
        indexfund_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")        
        individualstocks_button = customtkinter.CTkButton(right_frame,text="Stock Market", fg_color="#06402B", height=100)
        individualstocks_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # Creates the graph and updates balance
        self.accountbalance = customtkinter.CTkLabel(self.left_frame, text="Account Balance: $0.00", font=("Banschrift", 16))
        self.accountbalance.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.graph_frame = customtkinter.CTkFrame(self.left_frame)
        self.graph_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.show_graph(self.graph_frame)

        self.update_balance()




        