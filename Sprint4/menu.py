#The is the menu, showing graph, account balance and connects different investment oppurtunities
#Imports customtkinter for GUI
#Imports datetime to show date in top right corner and update graph
#Imports matplotlib to create and update graph
import customtkinter
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# A investmenu class to seamlessly switch between investent interfaces
class InvestmentMenu:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.menuGui()

    #A function to show graph, ensures it doesn't show graph is history doesn't exist
    def show_graph(self, frame):
        if not self.controller.history:
            return

        # Gathers the dates and values to plot on graph
        dates = [d for d, v in self.controller.history]
        values = [v for d, v in self.controller.history]

        #Defining variables and labels for the graph, and creates the graph with history data
        fig, ax = plt.subplots(figsize=(6, 3))

        ax.plot(dates, values, marker="o", color="#06402B")
        ax.set_title("Portfolio Balance")
        ax.set_ylabel("Value")
        ax.grid(True)

        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # A function to update the balance of user, changing the text in main menu
    def update_balance(self):
        balance = self.controller.totalaccountbalance()
        self.accountbalance.configure(text=f"Account Balance: ${balance:,.2f}")

    #Creates the menu GUI
    def menuGui(self):
        # This is for the date
        self.controller.clear_window()
        date = datetime.now().strftime("%A, %d %B %Y")
        self.time = customtkinter.CTkLabel(self.app, text=date,font=("BahnSchrift", 18))
        self.time.place(relx=0.98, rely=0.02, anchor="ne")  

        #Creates the frames
        self.left_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=600, height=650)
        self.left_frame.grid(row=1, column=0, rowspan=2, padx=(20, 10), pady=20, sticky="nsew")
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_propagate(False)

        right_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=800, height=650)
        right_frame.grid(row=1, column=1, padx=(10, 20), pady=20, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_propagate(False)
        #title
        customtkinter.CTkLabel(self.app, font=("Bahnschrift", 45), text_color="#06402B", text="Smart Investments").grid(row=0, column=0, padx=20, pady=5, sticky="w")
        #investment buttons
        saving_button = customtkinter.CTkButton(right_frame,text="High Yield Savings Account", fg_color="#06402B", height=100,  command=self.controller.operate_savings)
        saving_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        certificatofdeposit_button = customtkinter.CTkButton(right_frame,text="Certificate Of Deposit", fg_color="#06402B", height=100, command=self.controller.operate_cod)
        certificatofdeposit_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")        
        indexfund_button = customtkinter.CTkButton(right_frame,text="Index Fund", fg_color="#06402B", height=100,  command=self.controller.operate_index)
        indexfund_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")        
        individualstocks_button = customtkinter.CTkButton(right_frame,text="Stock Market", fg_color="#06402B", height=100, command=self.controller.operate_stock)
        individualstocks_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        #account balance and graph
        self.accountbalance = customtkinter.CTkLabel(self.left_frame, text="Account Balance: $0.00", font=("Banschrift", 16))
        self.accountbalance.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.graph_frame = customtkinter.CTkFrame(self.left_frame)
        self.graph_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.show_graph(self.graph_frame)
        #frequently updates balance
        self.update_balance()




        