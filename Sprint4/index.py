# The index file is important for index funds, utlises the ALPHA vantage api and formatting to get price data and create graph
#Import CustomTkinter for GUI
#Import request to pull data from API   
#Import pandas to convert data into usable objects
#Import matplotlib to create a graph for index funds
import customtkinter
import requests
import pandas as pd
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

#API Key and Index fund Symbol ids are defined
API_KEY = "N8I5DJYIP7RH1BC6"
SYMBOL = "VOO"

#Creates an investment class
class Investment:
    #defines the variables for ivnestment class
    def __init__(self, name, amount):
        self.name = name    
        self.amount = float(amount)
        self.rate_of_return = 0
        self.years = 0

#The class for the index fund app
#Connect user interfaces through controller    
class IndexApp:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.menuGui()
        self.update_balance()

    # A function to pull data from the api, pulls from using json
    def indexdatarequests(self):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        #formatting and setting variables for database of indexfund
        time_series = data.get("Time Series (Daily)", {})
        dataframe = pd.DataFrame.from_dict(time_series, orient="index")
        dataframe = dataframe.astype(float)
        dataframe.index = pd.to_datetime(dataframe.index)
        dataframe = dataframe.sort_index()

        return dataframe

    # A function to create graphs, setting dimensions and important components
    def setup_graph(self, frame):
        self.figure, self.axis = plt.subplots(figsize=(6, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    #Updates the graph, this is essential to ensure the code function like a proper investment app
    #Updates the graph every 10 mins
    def update_graph(self, frame):
        data = self.indexdatarequests()
        if data.empty:
            frame.after(600000, self.update_graph, frame)
            return

        #Finds the latests closing price and changes label of market price
        latest_price = data.iloc[-1]["4. close"]
        self.marketprice.configure(text=f"Current market price: ${latest_price:.2f}")

        #Finds the start and end of closing price and calculates growth, outputting market growth
        start = float(data["4. close"].iloc[0])
        end = float(data["4. close"].iloc[-1])
        growth = ((end - start) / start) * 100
        self.marketgrowth.configure(text=f"Market growth: {growth:.2f}%")

        #Creates the updated graph and updates every 600000 seconds
        self.axis.clear()
        self.axis.plot(data.index, data["4. close"], color="#06402B")
        self.axis.set_title("VOO Live Price")
        self.axis.set_ylabel("Price")
        self.axis.grid(True)
        self.figure.autofmt_xdate()
        self.canvas.draw()

        frame.after(600000, self.update_graph, frame)

    # A function to fetch the latest closed market price
    def get_latest_price(self, data):
        return float(data["4. close"].iloc[-1])

    # A buy function to buy a share from index fund
    def buy(self):
        #error handling to check if data avaliable
        data = self.indexdatarequests()
        if data.empty:
            return

        #Check latest closing price and ask user to input shares
        price = float(data["4. close"].iloc[-1])
        shares = int(self.indexentry.get())

        #if shares are less than 0, it will print error message in terminal 
        if shares <= 0:
            print("Enter valid shares")
            return

        #calculates cost by mutliply shares and price
        cost = shares * price

        #if cost of share is bigger than money in main portfolio, it will print error message in terminal 
        if self.controller.mainportfolio < cost:
            print("Not enough cash in main portfolio")
            return

        #Subtract money in account if share purchase is successful
        #Adds the share to investments and updates graph and balance
        self.controller.mainportfolio -= cost
        inv = Investment(name=SYMBOL, amount=shares)
        self.controller.indexfund_portfolio.append(inv)
        self.controller.history.append((datetime.now(), self.controller.totalaccountbalance()))
        self.update_balance()
    
    # A function to sell shares
    #Check if data avaible to sell avaliable shares
    def sell(self):
        data = self.indexdatarequests()
        if data.empty:
            return

        #obtain closing price of share and ask user how many shares they want to sell
        #gathers total amount of money in indexfund portfolio
        price = float(data["4. close"].iloc[-1])
        sell_shares = int(self.indexentry.get())
        total = sum(inv.amount for inv in self.controller.indexfund_portfolio)

        #If not enough shares/ or no shares, it will print error message in terminal
        if sell_shares > total:
            print("Not enough shares")
            return

        #number of shares remaining which will be sold, creates a new portfolio for remaining investments
        remaining = sell_shares
        new_portfolio = []
        
        # A for loop to test remaining shares
        # If all the shares have been sold, no updates, if the share can be sold, remove the shares from portfolio, otherwise sell part of it and keep the rest, ensuring remaing shares have been sold
        for inv in self.controller.indexfund_portfolio:
            if remaining <= 0:
                new_portfolio.append(inv)
            elif inv.amount <= remaining:
                remaining -= inv.amount
            else:
                inv.amount -= remaining
                new_portfolio.append(inv)
                remaining = 0

        #Replaces and updates portfolio, updates balance and history
        self.controller.indexfund_portfolio = new_portfolio
        self.controller.mainportfolio += sell_shares * price
        self.controller.history.append((datetime.now(), self.controller.totalaccountbalance()))
        self.update_balance()
    
    # Function to update balance
    #Checks if the data in api is avaliable
    def update_balance(self):
        data = self.indexdatarequests()
        if data.empty:
            return

        #obtains latest closing price and finds the value based on number of shares and price, changing index fund price and shares title
        price = float(data["4. close"].iloc[-1])
        shares = sum(inv.amount for inv in self.controller.indexfund_portfolio if inv.name == SYMBOL)
        value = shares * price
        self.balance.configure(text=f"VOO Value: ${value:.2f} ({shares:.0f} shares)")
    
    # A function to return back to the main menu, destroys any widgets
    def returnback(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()
    
    #Creates the gui for indexfund
    def menuGui(self):
        #Creates the frames for indexfund
        left_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=600, height=750)
        left_frame.grid(row=1, column=0, rowspan=2, padx=(20, 10), pady=20, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_propagate(False)

        right_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=800, height=750)
        right_frame.grid(row=1, column=1, padx=(10, 20), pady=(20, 10), sticky="nsew")
        right_frame.grid_propagate(False)
        right_frame.grid_columnconfigure(0, weight=1)

        #Creates the balances and labels for indexfund
        self.balance = customtkinter.CTkLabel(right_frame,text="Portfolio: $0.00",font=("Bahnschrift", 18))
        self.balance.grid(row=0, column=0, pady=10)

        entry = customtkinter.CTkLabel(right_frame, text="Enter Number of Wanted Shares", font=("Bahnschrift", 10))
        entry.grid(row=1, column=0, pady=10)

        self.marketprice = customtkinter.CTkLabel(right_frame,text="Current market price: --",font=("Bahnschrift", 10))
        self.marketprice.grid(row=2, column=0, pady=10)

        self.marketgrowth = customtkinter.CTkLabel(right_frame, text="Current market growth: {}", font=("Bahnschrift", 10))
        self.marketgrowth.grid(row=3, column=0, pady=10)

        self.indexentry = customtkinter.CTkEntry(right_frame, placeholder_text="Enter amount")
        self.indexentry.grid(row=4, column=0, pady=10)

        #Savings button frame with buy and sell buttons
        savingsbutton_frame = customtkinter.CTkFrame(right_frame, fg_color="#E2C3A9")
        savingsbutton_frame.grid(row=5, column=0, pady=(15, 60))

        deposit_button = customtkinter.CTkButton(savingsbutton_frame, text="Deposit", fg_color="#06402B", command=self.buy) 
        deposit_button.grid(row=0, column=0, padx=6)

        withdraw_button = customtkinter.CTkButton(savingsbutton_frame, text="Withdraw", fg_color="#06402B", command=self.sell)
        withdraw_button.grid(row=0, column=1, padx=6)

        returnback_button = customtkinter.CTkButton(self.app,text="Back to Main Menu", fg_color="#06402B", width=800, height=30,command=self.returnback)
        returnback_button.place(x=600, y=650)

        #Sets up and updates graph in the left frame
        self.setup_graph(left_frame)
        self.update_graph(left_frame)

