import customtkinter
import requests
import pandas as pd
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from functools import partial

API_KEY = "N8I5DJYIP7RH1BC6"
TICKERS = ["NVDA", "ALAB", "ORCL", "GOOGL", "SPCX"]

class Investment:
    def __init__(self, name, amount, rate_of_return):
        self.name = name
        self.amount = amount
        self.rate_of_return = rate_of_return

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

    def stockdatarequests(self, tickers):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={tickers}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        time_series = data.get("Time Series (Daily)", {})

        if not time_series:
            return pd.DataFrame()

        dataframe = pd.DataFrame.from_dict(time_series, orient="index")
        dataframe = dataframe.astype(float)
        dataframe.index = pd.to_datetime(dataframe.index)
        dataframe = dataframe.sort_index()

        return dataframe

    def setup_graph(self, frame):
        figure, axis = plt.subplots(figsize=(6, 3))
        canvas = FigureCanvasTkAgg(figure, master=frame)

        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, sticky="nsew")

        return figure, axis, canvas 

    def update_graph(self, frame, tickers, index):
        data = self.stockdatarequests(tickers)

        if data.empty:
            frame.after(60000, self.update_graph, frame, tickers, index)
            return

        graph = self.graphs[index]
        axis = graph["axis"]
        figure = graph["figure"]
        canvas = graph["canvas"]

        latest_price = float(data.iloc[-1]["4. close"])
        start = float(data["4. close"].iloc[-2])
        end = float(data["4. close"].iloc[-1])
        growth = ((end - start) / start) * 100
        self.marketpricestocks[index].configure(text=f"{tickers} Price: ${latest_price:.2f}")
        self.marketgrowthstocks[index].configure(text=f"Growth: {growth:.2f}%")

        axis.clear()
        axis.plot(data.index, data["4. close"], color="#06402B")
        axis.set_title(f"{tickers} Price")
        axis.set_ylabel("Price")
        axis.grid(True)

        figure.autofmt_xdate()
        canvas.draw()
        frame.after(60000, self.update_graph, frame, tickers, index)

    def buy(self, stock):
        data = self.stockdatarequests(stock)
        if data.empty:
            return

        price = float(data.iloc[-1]["4. close"])
        index = self.stocks.index(stock)
        buyingshares = int(self.entry[index].get())

        if buyingshares <= 0:
            print("Enter a valid number of shares")
            return

        cost = buyingshares * price

        if self.controller.mainportfolio < cost:
            print("Not enough cash")
            return

        self.controller.mainportfolio -= cost
        inv = Investment(stock, buyingshares, 0)
        self.controller.stockmarket_portfolio.append(inv)
        self.controller.history.append((datetime.now(), self.controller.totalaccountbalance()))
        self.currentshares(stock)
        self.update_balance()

    def sell(self, stock):
        data = self.stockdatarequests(stock)
        if data.empty:
            return

        price = float(data.iloc[-1]["4. close"])
        index = self.stocks.index(stock)
        sellingshares = int(self.entry[index].get())
        total_shares = sum(inv.amount for inv in self.controller.stockmarket_portfolio if inv.name == stock)

        if sellingshares > total_shares:
            print("Not enough shares")
            return

        remaining = sellingshares
        new_portfolio = []

        for inv in self.controller.stockmarket_portfolio:
            if remaining <= 0:
                new_portfolio.append(inv)
            elif inv.amount <= remaining:
                remaining -= inv.amount
            else:
                inv.amount -= remaining
                new_portfolio.append(inv)
                remaining = 0

        self.controller.stockmarket_portfolio = new_portfolio
        self.controller.mainportfolio += sellingshares * price
        self.controller.history.append((datetime.now(), self.controller.totalaccountbalance()) )
        self.currentshares(stock)
        self.update_balance()

    def currentshares(self, stock):
        index = self.stocks.index(stock)

        total_shares = sum(inv.amount for inv in self.controller.stockmarket_portfolio if inv.name == stock)
        self.shares[index].configure(text=f"Shares Owned: {total_shares}")

    def update_balance(self):
        total_value = 0

        for stock in self.stocks:
            data = self.stockdatarequests(stock)
            if data.empty:
                continue

            price = float(data.iloc[-1]["4. close"])
            shares = sum(inv.amount for inv in self.controller.stockmarket_portfolio if inv.name == stock)
            total_value += shares * price

        self.balance.configure(text=f"Portfolio Value: ${total_value:.2f}")

    def returnback(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    def menuGui(self):
        for i in range(len(self.stocks)):
            self.app.grid_columnconfigure(i, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
            
        self.balance = customtkinter.CTkLabel(self.app,text="Portfolio Value: $0.00",font=("Bahnschrift", 12))
        self.balance.grid(row=1, column=0, columnspan=len(self.stocks), pady=10)

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

        self.update_balance()