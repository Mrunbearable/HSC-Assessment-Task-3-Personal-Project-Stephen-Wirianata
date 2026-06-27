#The stock interface performs very similarly to the index fund but with more indivdidual graphs and information, and formatting to get price data and create graph
#Note the API has changed for alpha vantage to twelvedata
#Import CustomTkinter for GUI
#Import request to pull data from API   
#Import pandas to convert data into usable objects
#Import matplotlib to create a graph for index funds
#Import functools to automatically remember inputs so it becomes easier to manipulate later
#Import user data to control each user accounts
import customtkinter
import requests
import pandas as pd
import time
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from functools import partial
from userdata import save_users

#API Key and stock market Symbols ids are defined
#Note the API has changed
#ALSO implement caching to stop crashing errors
TICKERS = ["NVDA", "ALAB", "ORCL", "GOOGL", "SPCX"]
CACHELIMITSECONDS = 60
TWELVEDATA_API_KEY = "91002cdaa44445d99142fd352da2e0dc"
TWELVEDATA_BASE_URL = "https://api.twelvedata.com"

#Creates the invesment class and variables
class Investment:
    def __init__(self, name, amount, rate_of_return):
        self.name = name
        self.amount = amount
        self.rate_of_return = rate_of_return

#Creates the stock market class and variables, portfolios, dictionaries to handle each stock easier
class StockMarketApp:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.active = True

        self.stocks = TICKERS
        self.marketpricestocks = []
        self.marketgrowthstocks = []
        self.shares = []
        self.graphs = []
        self.entry = []
        self.cache = {}
        self.menuGui()

    # A function to handle stock data requests
    def stockdatarequests(self, ticker):
        now = time.time()
        cached = self.cache.get(ticker)
        if cached is not None and (now - cached["time"]) < CACHELIMITSECONDS:
            return cached["data"]

        #Utlises a try and response to get data of different stock, ensuring errors can be handled reliably
        #Obtains the data from the API and saves the data so it can be used for investments
        try:
            response = requests.get(
                f"{TWELVEDATA_BASE_URL}/time_series",
                params={"symbol": ticker,"interval": "1day","outputsize": 60,"apikey": TWELVEDATA_API_KEY,},timeout=10,)
            data = response.json()
        except Exception as e:
            print(f"[stockdatarequests] Exception fetching {ticker}: {e}")
            return cached["data"] if cached is not None else pd.DataFrame()

        if not data or data.get("status") == "error" or "values" not in data:
            print(f"[stockdatarequests] No data for {ticker}: {data}")
            return cached["data"] if cached is not None else pd.DataFrame()

        values = data["values"]
        dataframe = pd.DataFrame({"4. close": [float(v["close"]) for v in values],}, index=pd.to_datetime([v["datetime"] for v in values]))
        dataframe = dataframe.sort_index()

        self.cache[ticker] = {"data": dataframe, "time": now}
        return dataframe
    
    # A function to get lastest closing price of different ticker/stocks
    def get_latest_price(self, ticker):
        data = self.stockdatarequests(ticker)
        if data.empty:
            return None

        return float(data["4. close"].iloc[-1])

    # a function to setup graphs of different ticker/stocks
    def setup_graph(self, frame):

        figure, axis = plt.subplots(figsize=(6, 3))
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0,columnspan=2,sticky="nsew")
        
        return figure, axis, canvas

    # a function to update graphs of different ticker/stocks
    def update_graph(self, frame, ticker, index):
        if not self.active or not self.controller.running:
            return

        data = self.stockdatarequests(ticker)

        #error message if data requests is unsuccessful
        if data.empty:
            self.marketpricestocks[index].configure(text=f"{ticker} Price: unavailable")
            if self.active and self.controller.running:
                frame.after(300000, self.update_graph, frame, ticker, index)
            return

        #Creates the graph
        graph = self.graphs[index]
        axis = graph["axis"]
        figure = graph["figure"]
        canvas = graph["canvas"]

        #Calculates market price and market growth and plots it below the graph
        latest_price = float(data["4. close"].iloc[-1])
        start = float(data["4. close"].iloc[0])
        end = float(data["4. close"].iloc[-1])
        growth = ((end - start) / start) * 100

        self.marketpricestocks[index].configure(text=f"{ticker} Price: ${latest_price:.2f}")
        self.marketgrowthstocks[index].configure(text=f"Growth: {growth:.2f}%")
        axis.clear()
        axis.plot(data.index, data["4. close"], color="#06402B")
        axis.set_title(f"{ticker} Price")
        axis.set_ylabel("Price")
        axis.grid(True)

        figure.autofmt_xdate()
        canvas.draw()

        if self.active and self.controller.running:
            frame.after(300000, self.update_graph, frame, ticker, index)

    # A function to buy different stocks/tickers, establishing the latest closing price
    def buy(self, stock):
        price = self.get_latest_price(stock)

        #Error handling if obtaining price fails
        if price is None:
            print(f"[buy] No price data available for {stock}, aborting purchase")
            return

        #Get user stock input
        index = self.stocks.index(stock)
        buyingshares = int(self.entry[index].get())

        #if shares are less than 0, it will print error message in terminal 
        if buyingshares <= 0:
            self.status.configure(text="Enter a valid number of shares.", text_color="red")
            return

        #calculates cost by mutliply shares and price
        cost = buyingshares * price

        #calculates cost by mutliply shares and price
        if self.controller.mainportfolio < cost:
            self.status.configure(text="Not enough cash.", text_color="red")
            return

        #Subtract money in account of current user if share purchase is successful
        #Adds the share to investments and updates graph and balance
        #Saves any updates 
        self.controller.mainportfolio -= cost
        inv = Investment(stock, buyingshares, 0)
        self.controller.stockmarket_portfolio.append(inv)
        self.controller.frequentdatarefresh()
        self.controller.users_data[self.controller.current_user_token]["history"].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.controller.totalaccountbalance()))
        save_users(self.controller.users_data)
        self.currentshares(stock)
        self.update_balance()

    # A function to sell different tickers/stock, establishing the latest closing price
    def sell(self, stock):
        price = self.get_latest_price(stock)

        #Error handling if obtaining price fails
        if price is None:
            print(f"[sell] No price data available for {stock}, aborting sale")
            return

        #gather total amount of shares in stockmarket portfolio for the specific stock/ticker
        index = self.stocks.index(stock)
        sellingshares = int(self.entry[index].get())
        total_shares = sum(inv.amount for inv in self.controller.stockmarket_portfolio if inv.name == stock)

        #If not enough shares/ or no shares, it will print error message in terminal
        if sellingshares > total_shares:
            self.status.configure(text="Not enough shares to sell.", text_color="red")
            return

        #number of shares remaining which will be sold, creates a new portfolio for remaining investments for current user
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

                        
        #Replaces and updates portfolio, updates balance and history for current user
        self.controller.stockmarket_portfolio = new_portfolio
        self.controller.mainportfolio += sellingshares * price
        self.controller.frequentdatarefresh()
        self.controller.users_data[self.controller.current_user_token]["history"].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.controller.totalaccountbalance()))
        save_users(self.controller.users_data)
        self.currentshares(stock)
        self.update_balance()

     # A function to calculate current number of shares of current user and output numbers of shares in label
    def currentshares(self, stock):
        index = self.stocks.index(stock)

        total_shares = sum(inv.amount for inv in self.controller.stockmarket_portfolio if inv.name == stock)
        self.shares[index].configure(text=f"Shares Owned: {total_shares}")

    #A function to update balance of current user, setting total value to 0
    def update_balance(self):
        total_value = 0

        # For loop, checking latest closed market price and number of shares of specfic stock to calculate total value
        # Returns portfolio value in a label
        for stock in self.stocks:
            price = self.get_latest_price(stock)
            if price is None:
                continue
            shares = sum(inv.amount for inv in self.controller.stockmarket_portfolio if inv.name == stock)
            total_value += shares * price

        self.balance.configure(text=f"Portfolio Value: ${total_value:.2f}")

    # A function to return back to main menu, destroying widgets
    def returnback(self):
        self.active = False
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    # A function to create stock market GUI
    def menuGui(self):
        for i in range(len(self.stocks)):
            self.app.grid_columnconfigure(i, weight=1)

        self.app.grid_rowconfigure(0, weight=1)
        self.balance = customtkinter.CTkLabel(self.app, text="Portfolio Value: $0.00", font=("Bahnschrift", 12))
        self.balance.grid(row=1, column=0, columnspan=len(self.stocks), pady=10)

        # For each stock, creates frame, labels, entries, buttons and graphs
        for i, stock in enumerate(self.stocks):
            stockframe = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=600, height=750)
            stockframe.grid(row=0, column=i, rowspan=2, padx=(20, 10), pady=20, sticky="nsew")
            stockframe.grid_columnconfigure(0, weight=1)
            stockframe.grid_columnconfigure(1, weight=1)
            stockframe.grid_rowconfigure(2, weight=1)

            marketprice = customtkinter.CTkLabel(stockframe, text=f"{stock} Price: --", font=("Bahnschrift", 25))
            marketprice.grid(row=1, column=0, padx=10)
            marketgrowth = customtkinter.CTkLabel(stockframe, text="Growth: --", font=("Bahnschrift", 25))
            marketgrowth.grid(row=2, column=0, padx=10)

            shares = customtkinter.CTkLabel(stockframe, text="Shares Owned: 0", font=("Bahnschrift", 25))
            shares.grid(row=3, column=0, padx=10)

            self.shares.append(shares)
            self.marketpricestocks.append(marketprice)
            self.marketgrowthstocks.append(marketgrowth)

            fig, axis, canvas = self.setup_graph(stockframe)

            entry = customtkinter.CTkEntry(stockframe, placeholder_text="Enter amount")
            entry.grid(row=4, column=0, pady=10)
            button_frame = customtkinter.CTkFrame(stockframe, fg_color="#E2C3A9")
            button_frame.grid(row=5, column=0, pady=(15, 60))
            buy_button = customtkinter.CTkButton(button_frame, text="Buy SHARE", fg_color="#06402B", command=partial(self.buy, stock))
            buy_button.grid(row=0, column=0, padx=6)

            sell_button = customtkinter.CTkButton(button_frame, text="Sell SHARE", fg_color="#06402B", command=partial(self.sell, stock))
            sell_button.grid(row=0, column=1, padx=6)
            self.entry.append(entry)
            self.graphs.append({"figure": fig, "axis": axis, "canvas": canvas})

            self.update_graph(stockframe, stock, i)
            self.currentshares(stock)

        self.status = customtkinter.CTkLabel(self.app, text="")
        self.status.grid(row=1, column=0, columnspan=len(self.stocks), pady=10)
        returnback_button = customtkinter.CTkButton(self.app,text="Back to Main Menu", fg_color="#06402B", width=1500, height=30,command=self.returnback)
        returnback_button.grid(row=2, column=0, columnspan=5, padx=10)
        #Frequently updating balance
        self.update_balance()