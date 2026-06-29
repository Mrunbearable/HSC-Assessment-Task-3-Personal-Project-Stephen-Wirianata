# The index file is important for index funds, and formatting to get price data and create graph
#Note the API has change for alpha vantage to twelve data
#Import CustomTkinter for GUI
#Import request to pull data from API   
#Import pandas to convert data into usable objects
#Import matplotlib to create a graph for index funds
#Import users to control each user account
import customtkinter
import requests
import pandas as pd
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from userdata import save_users
import os
from dotenv import load_dotenv

#API Key and Index fund Symbol ids are defined
#Note the API has changed from alpha vantage to twelve data
#load_dotenv() reads the .env file in the project folder and loads its values as environment variables
#The key itself is NOT written in this file - it's read from the environment so it isn't exposed in plaintext source code
load_dotenv()
SYMBOL = "VOO"
TWELVEDATA_API_KEY = os.environ.get("TWELVEDATA_API_KEY")
TWELVEDATA_BASE_URL = "https://api.twelvedata.com"

#Creates an investment class and variables
class Investment:
    def __init__(self, name, amount):
        self.name = name    
        self.amount = float(amount)
        self.rate_of_return = 0
        self.years = 0

#the class for index fund app is created    
class IndexApp:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.active = True
        self.menuGui()
        self.update_balance()

    #a function to obtain data from twelve data API, uses try and except to gracefully handle api errors
    def indexdatarequests(self):
        try:
            response = requests.get(
                f"{TWELVEDATA_BASE_URL}/time_series", params={ "symbol": SYMBOL, "interval": "1day", "outputsize": 60, "apikey": TWELVEDATA_API_KEY,}, timeout=10,)
            data = response.json()
        except Exception as e:
            print(f"[indexdatarequests] Exception fetching data: {e}")
            return pd.DataFrame()

        if not data or data.get("status") == "error" or "values" not in data:
            print(f"[indexdatarequests] No data for {SYMBOL}: {data}")
            return pd.DataFrame()

        #Saves the data so it can be used for investments
        values = data["values"]
        dataframe = pd.DataFrame({"4. close": [float(v["close"]) for v in values],}, index=pd.to_datetime([v["datetime"] for v in values]))
        dataframe = dataframe.sort_index()

        return dataframe

    #A function to set up graph, constructing dimensions and important components
    def setup_graph(self, frame):
        self.figure, self.axis = plt.subplots(figsize=(6, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    
    #Updates the graph, this is essential to ensure the code function like a proper investment app
    #Updates the graph every 10 mins
    def update_graph(self, frame):
        if not self.active or not self.controller.running:
            return

        data = self.indexdatarequests()
        if data.empty:
            if self.active and self.controller.running:
                frame.after(300000, self.update_graph, frame)
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

        if self.active and self.controller.running:
            frame.after(300000, self.update_graph, frame)
    
    # A function to obtain latest closing price for index fund
    def obtainlatestprice(self, data):
        return float(data["4. close"].iloc[-1])

    # A buy function to buy a share from index fund
    def buy(self):
        #error handling to check if data avaliable
        data = self.indexdatarequests()
        if data.empty:
            return

        #Check latest closing price and ask user to input shares
        price = float(data["4. close"].iloc[-1])

        #Try to convert the shares entry box text to a whole number. If the user typed letters
        #or left it blank, this catches the error instead of crashing the whole program
        try:
            shares = int(self.indexentry.get())
        except ValueError:
            self.status.configure(text="Enter valid shares.", text_color="red")
            return

        #if shares are less than 0, it will print error message in terminal 
        if shares <= 0:
            self.status.configure(text="Enter valid shares.", text_color="red")
            return

        #calculates cost by mutliply shares and price
        cost = shares * price

        #if cost of share is bigger than money in main portfolio, it will print error message in terminal 
        if self.controller.mainportfolio < cost:
            self.status.configure(text="Not enough cash in main portfolio.", text_color="red")
            return

        #Subtract money in account if share purchase is successful
        #Adds the share to investments and updates graph and balance
        #Saves the updates
        self.controller.mainportfolio -= cost
        inv = Investment(name=SYMBOL, amount=shares)
        self.controller.indexfund_portfolio.append(inv)
        self.controller.users_data[self.controller.current_user_token]["history"].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.controller.totalaccountbalance()))
        save_users(self.controller.users_data)
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

        #Try to convert the shares entry box text to a whole number. If the user typed letters
        #or left it blank, this catches the error instead of crashing the whole program
        try:
            sell_shares = int(self.indexentry.get())
        except ValueError:
            self.status.configure(text="Enter valid shares.", text_color="red")
            return

        total = sum(inv.amount for inv in self.controller.indexfund_portfolio)

        #If not enough shares/ or no shares, it will print error message in terminal
        if sell_shares > total:
            self.status.configure(text="Not enough shares to sell.", text_color="red")
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
        #Saves the updates
        self.controller.indexfund_portfolio = new_portfolio
        self.controller.mainportfolio += sell_shares * price
        self.controller.frequentdatarefresh()
        self.controller.users_data[self.controller.current_user_token]["history"].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.controller.totalaccountbalance()))
        save_users(self.controller.users_data)
        self.update_balance()
    
    # Function to update balance
    #Checks if the data in api is avaliable
    #obtains latest closing price and finds the value based on number of shares and price, changing index fund price and shares title
    def update_balance(self, data=None, price=None):
        if data is None:
            data = self.indexdatarequests()
            if data.empty:
                return
        if price is None:
            price = float(data["4. close"].iloc[-1])

        
        shares = sum(inv.amount for inv in self.controller.indexfund_portfolio if inv.name == SYMBOL)
        value = shares * price
        self.balance.configure(text=f"VOO Value: ${value:.2f} ({shares:.0f} shares)")

     # A function to return back to the main menu, destroys any widgets
    def returnback(self):
        self.active = False
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    #Creates the gui for indexfund
    def menuGui(self):
        #Creates the frames for index fund
        left_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=600, height=750)
        left_frame.grid(row=1, column=0, rowspan=2, padx=(20, 10), pady=20, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_propagate(False)

        right_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=800, height=750)
        right_frame.grid(row=1, column=1, padx=(10, 20), pady=(20, 10), sticky="nsew")
        right_frame.grid_propagate(False)
        right_frame.grid_columnconfigure(0, weight=1)

        #Creates the balances and labels for indexfund      
        self.balance = customtkinter.CTkLabel(right_frame,text="Portfolio: $0.00",font=("Bahnschrift", 30))
        self.balance.grid(row=0, column=0, pady=10)

        entry = customtkinter.CTkLabel(right_frame, text="Enter Number of Wanted Shares", font=("Bahnschrift", 20))
        entry.grid(row=1, column=0, pady=10)
        self.marketprice = customtkinter.CTkLabel(right_frame,text="Current market price: --",font=("Bahnschrift", 20))
        self.marketprice.grid(row=2, column=0, pady=10)
        self.marketgrowth = customtkinter.CTkLabel(right_frame, text="Current market growth: {}", font=("Bahnschrift", 20))
        self.marketgrowth.grid(row=3, column=0, pady=10)
        self.indexentry = customtkinter.CTkEntry(right_frame, placeholder_text="Enter amount")
        self.indexentry.grid(row=4, column=0, pady=10)

        #Savings button frame with buy and sell buttons
        savingsbutton_frame = customtkinter.CTkFrame(right_frame, fg_color="#E2C3A9")
        savingsbutton_frame.grid(row=5, column=0, pady=(15, 60))
        deposit_button = customtkinter.CTkButton(savingsbutton_frame, text="Buy", fg_color="#06402B", command=self.buy) 
        deposit_button.grid(row=0, column=0, padx=6)
        withdraw_button = customtkinter.CTkButton(savingsbutton_frame, text="Sell", fg_color="#06402B", command=self.sell)
        withdraw_button.grid(row=0, column=1, padx=6)

        #Error message ouput widget/label
        self.status = customtkinter.CTkLabel(right_frame, text="")
        self.status.grid(row=7, column=0, columnspan=2, pady=10)

        returnback_button = customtkinter.CTkButton(self.app,text="Back to Main Menu", fg_color="#06402B", width=800, height=30,command=self.returnback)
        returnback_button.place(x=520, y=740)

        #Sets up and updates graph in the left frame
        self.setup_graph(left_frame)
        self.update_graph(left_frame)