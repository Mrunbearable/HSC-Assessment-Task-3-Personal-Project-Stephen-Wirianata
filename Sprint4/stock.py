# The stock interface performs very similarly to the index fund but with more indivdidual graphs and information, utlises the ALPHA vantage api and formatting to get price data and create graph
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
from functools import partial

#API Key and stock market Symbols ids are defined
API_KEY = "N8I5DJYIP7RH1BC6"
TICKERS = ["NVDA", "ALAB", "ORCL", "GOOGL", "SPCX"]

# Create an investment class
class Investment:
    #Defines the variables for investment class
    def __init__(self, name, amount, rate_of_return):
        self.name = name
        self.amount = amount
        self.rate_of_return = rate_of_return

#Creates The stock market Class, creating a connection to other interfaces, dictionaries to effectively handle different market stocks
class StockMarketApp:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.stocks = TICKERS
        self.marketpricestocks = []
        self.marketgrowthstocks = []
        self.shares = []
        self.graphs = []
        self.entry = []
        self.menuGui()

    # A function to pull data from the api, pulls from using json
    def stockdatarequests(self, tickers):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={tickers}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        time_series = data.get("Time Series (Daily)", {})

        if not time_series:
            return pd.DataFrame()
        
        #formatting and setting variables for database for stockmarket
        dataframe = pd.DataFrame.from_dict(time_series, orient="index")
        dataframe = dataframe.astype(float)
        dataframe.index = pd.to_datetime(dataframe.index)
        dataframe = dataframe.sort_index()

        return dataframe

    # A function to create graphs, setting dimensions and important components
    def setup_graph(self, frame):
        figure, axis = plt.subplots(figsize=(6, 3))
        canvas = FigureCanvasTkAgg(figure, master=frame)

        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, sticky="nsew")

        return figure, axis, canvas 

    #Updates the graph, this is essential to ensure the code function like a proper investment app
    #Updates the graph every 10 mins
    def update_graph(self, frame, tickers, index):
        data = self.stockdatarequests(tickers)
        if data.empty:
            frame.after(600000, self.update_graph, frame, tickers, index)
            return

        # Creates succint graph variables to utilse
        graph = self.graphs[index]
        axis = graph["axis"]
        figure = graph["figure"]
        canvas = graph["canvas"]

        #Finds the latests closing price and changes label of market price
        #Finds the start and end of closing price and calculates growth, outputting market growth
        latest_price = float(data.iloc[-1]["4. close"])
        start = float(data["4. close"].iloc[-2])
        end = float(data["4. close"].iloc[-1])
        growth = ((end - start) / start) * 100
        self.marketpricestocks[index].configure(text=f"{tickers} Price: ${latest_price:.2f}")
        self.marketgrowthstocks[index].configure(text=f"Growth: {growth:.2f}%")

        #Creates the updated graph and updates every 600000 seconds
        axis.clear()
        axis.plot(data.index, data["4. close"], color="#06402B")
        axis.set_title(f"{tickers} Price")
        axis.set_ylabel("Price")
        axis.grid(True)

        figure.autofmt_xdate()
        canvas.draw()
        frame.after(600000, self.update_graph, frame, tickers, index)

    # A function to buy stock from the market
    def buy(self, stock):
        #error handling to check if data avaliable
        data = self.stockdatarequests(stock)
        if data.empty:
            return

        #Check latest closing price for each stock and ask user to input shares
        price = float(data.iloc[-1]["4. close"])
        index = self.stocks.index(stock)
        buyingshares = int(self.entry[index].get())

        #if shares are less than 0, it will print error message in terminal 
        if buyingshares <= 0:
            print("Enter a valid number of shares")
            return

        #calculates cost by mutliply shares and price
        cost = buyingshares * price

        #if cost of share is bigger than money in main portfolio, it will print error message in terminal 
        if self.controller.mainportfolio < cost:
            print("Not enough cash")
            return

        #Subtract money in account if share purchase is successful
        #Adds the share to investments and updates graph and balance
        self.controller.mainportfolio -= cost
        inv = Investment(stock, buyingshares, 0)
        self.controller.stockmarket_portfolio.append(inv)
        self.controller.history.append((datetime.now(), self.controller.totalaccountbalance()))
        self.currentshares(stock)
        self.update_balance()

    # A function to sell shares
    #Check if data avaible to sell avaliable shares
    def sell(self, stock):
        data = self.stockdatarequests(stock)
        if data.empty:
            return

        #obtain closing price of share and ask user how many shares they want to sell
        #gathers total amount of money in stockmarket portfolio
        price = float(data.iloc[-1]["4. close"])
        index = self.stocks.index(stock)
        sellingshares = int(self.entry[index].get())
        total_shares = sum(inv.amount for inv in self.controller.stockmarket_portfolio if inv.name == stock)

        
        #If not enough shares/ or no shares, it will print error message in terminal
        if sellingshares > total_shares:
            print("Not enough shares")
            return

        #number of shares remaining which will be sold, creates a new portfolio for remaining investments
        remaining = sellingshares
        new_portfolio = []

        # A for loop to test remaining shares
        # If all the shares have been sold, no updates, if the share can be sold, remove the shares from portfolio, otherwise sell part of it and keep the rest, ensuring remaing shares have been sold
        for inv in self.controller.stockmarket_portfolio:
            if remaining <= 0:
                new_portfolio.append(inv)
            elif inv.amount <= remaining:
                remaining -= inv.amount
            else:
                inv.amount -= remaining
                new_portfolio.append(inv)
                remaining = 0
                
        #Replaces and updates portfolio, updates balance and history
        self.controller.stockmarket_portfolio = new_portfolio
        self.controller.mainportfolio += sellingshares * price
        self.controller.history.append((datetime.now(), self.controller.totalaccountbalance()) )
        self.currentshares(stock)
        self.update_balance()

    # A function to calculate current number of shares and output numbers of shares in label
    def currentshares(self, stock):
        index = self.stocks.index(stock)

        total_shares = sum(inv.amount for inv in self.controller.stockmarket_portfolio if inv.name == stock)
        self.shares[index].configure(text=f"Shares Owned: {total_shares}")
    
    # A function to update balance, setting total value to 0
    def update_balance(self):
        total_value = 0

        # For loop, checking latest closed market price and number of shares of specfic stock to calculate total value
        # Returns portfolio value in a label
        for stock in self.stocks:
            data = self.stockdatarequests(stock)
            if data.empty:
                continue

            price = float(data.iloc[-1]["4. close"])
            shares = sum(inv.amount for inv in self.controller.stockmarket_portfolio if inv.name == stock)
            total_value += shares * price

        self.balance.configure(text=f"Portfolio Value: ${total_value:.2f}")

    # A function to return back to main menu, destroying widgets
    def returnback(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    # A function to create stock market GUI, basically the same as index fund GUI by for loop and indexed
    def menuGui(self):
        for i in range(len(self.stocks)):
            self.app.grid_columnconfigure(i, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
            
        self.balance = customtkinter.CTkLabel(self.app,text="Portfolio Value: $0.00",font=("Bahnschrift", 12))
        self.balance.grid(row=1, column=0, columnspan=len(self.stocks), pady=10)

        # For each stock, creates frame, labels, entries, buttons and graphs
        for i, stock in enumerate(self.stocks):
            stockframe = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=600, height=750)
            stockframe.grid(row=0,column=i,rowspan=2,padx=(20, 10),pady=20,sticky="nsew")
            stockframe.grid_columnconfigure(0, weight=1)
            stockframe.grid_columnconfigure(1, weight=1)
            stockframe.grid_rowconfigure(2, weight=1)

            marketprice = customtkinter.CTkLabel(stockframe,text=f"{stock} Price: --",font=("Bahnschrift", 10))
            marketprice.grid(row=1, column=0, padx=10)
            marketgrowth = customtkinter.CTkLabel(stockframe,text=f"{stock} Growth: --",font=("Bahnschrift", 10))
            marketgrowth.grid(row=2, column=0, padx=10)
            shares = customtkinter.CTkLabel(stockframe, text="Shares Owned: 0", font=("Bahnschrift", 10))
            shares.grid(row=3, column=0, padx=10)

            self.shares.append(shares)
            self.marketpricestocks.append(marketprice)
            self.marketgrowthstocks.append(marketgrowth)
            fig, axis, canvas = self.setup_graph(stockframe)
            
            entry = customtkinter.CTkEntry(stockframe, placeholder_text="Enter amount")
            entry.grid(row=4, column=0, pady=10)
            savingsbutton_frame = customtkinter.CTkFrame(stockframe, fg_color="#E2C3A9")
            savingsbutton_frame.grid(row=5, column=0, pady=(15, 60))
            savingsbutton_frame.grid_columnconfigure(0, weight=1)
            savingsbutton_frame.grid_columnconfigure(1, weight=1)
            buy_button = customtkinter.CTkButton(savingsbutton_frame, text="Buy SHARE", fg_color="#06402B", command=partial(self.buy, stock))
            buy_button.grid(row=0, column=0, padx=6)
            sell_button = customtkinter.CTkButton(savingsbutton_frame, text="Sell SHARE", fg_color="#06402B", command=partial(self.sell, stock))
            sell_button.grid(row=0, column=1, padx=6)

            self.entry.append(entry)
            self.graphs.append({"figure": fig,"axis": axis,"canvas": canvas})
            self.update_graph(stockframe, stock, i)
            self.currentshares(stock)
        #Frequently updating balance
        self.update_balance()