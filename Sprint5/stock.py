import customtkinter
import requests
import pandas as pd
import time
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from functools import partial
from userdata import save_users

TICKERS = ["NVDA", "ALAB", "ORCL", "GOOGL", "SPCX"]
CACHELIMITSECONDS = 60
TWELVEDATA_API_KEY = "91002cdaa44445d99142fd352da2e0dc"
TWELVEDATA_BASE_URL = "https://api.twelvedata.com"

class Investment:
    def __init__(self, name, amount, rate_of_return):
        self.name = name
        self.amount = amount
        self.rate_of_return = rate_of_return


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

    def stockdatarequests(self, ticker):
        now = time.time()
        cached = self.cache.get(ticker)
        if cached is not None and (now - cached["time"]) < CACHELIMITSECONDS:
            return cached["data"]

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

    def get_latest_price(self, ticker):
        data = self.stockdatarequests(ticker)
        if data.empty:
            return None

        return float(data["4. close"].iloc[-1])

    def setup_graph(self, frame):

        figure, axis = plt.subplots(figsize=(6, 3))
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0,columnspan=2,sticky="nsew")
        
        return figure, axis, canvas

    def update_graph(self, frame, ticker, index):
        if not self.active or not self.controller.running:
            return

        data = self.stockdatarequests(ticker)

        if data.empty:
            self.marketpricestocks[index].configure(text=f"{ticker} Price: unavailable")
            if self.active and self.controller.running:
                frame.after(300000, self.update_graph, frame, ticker, index)
            return

        graph = self.graphs[index]
        axis = graph["axis"]
        figure = graph["figure"]
        canvas = graph["canvas"]

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

    def buy(self, stock):
        price = self.get_latest_price(stock)

        if price is None:
            print(f"[buy] No price data available for {stock}, aborting purchase")
            return

        index = self.stocks.index(stock)
        buyingshares = int(self.entry[index].get())

        if buyingshares <= 0:
            self.status.configure(text="Enter a valid number of shares.", text_color="red")
            return

        cost = buyingshares * price

        if self.controller.mainportfolio < cost:
            self.status.configure(text="Not enough cash.", text_color="red")
            return

        self.controller.mainportfolio -= cost

        inv = Investment(stock, buyingshares, 0)
        self.controller.stockmarket_portfolio.append(inv)
        self.controller.frequentdatarefresh()

        self.controller.users_data[self.controller.current_user_token]["history"].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.controller.totalaccountbalance()))

        save_users(self.controller.users_data)

        self.currentshares(stock)
        self.update_balance()

    def sell(self, stock):
        price = self.get_latest_price(stock)

        if price is None:
            print(f"[sell] No price data available for {stock}, aborting sale")
            return

        index = self.stocks.index(stock)
        sellingshares = int(self.entry[index].get())
        total_shares = sum(inv.amount for inv in self.controller.stockmarket_portfolio if inv.name == stock)

        if sellingshares > total_shares:
            self.status.configure(text="Not enough shares to sell.", text_color="red")
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
        self.controller.frequentdatarefresh()
        self.controller.users_data[self.controller.current_user_token]["history"].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.controller.totalaccountbalance()))
        save_users(self.controller.users_data)
        self.currentshares(stock)
        self.update_balance()

    def currentshares(self, stock):
        index = self.stocks.index(stock)

        total_shares = sum(inv.amount for inv in self.controller.stockmarket_portfolio if inv.name == stock)
        self.shares[index].configure(text=f"Shares Owned: {total_shares}")

    def update_balance(self):
        total_value = 0

        for stock in self.stocks:
            price = self.get_latest_price(stock)
            if price is None:
                continue
            shares = sum(inv.amount for inv in self.controller.stockmarket_portfolio if inv.name == stock)
            total_value += shares * price

        self.balance.configure(text=f"Portfolio Value: ${total_value:.2f}")

    def returnback(self):
        self.active = False
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    def menuGui(self):
        for i in range(len(self.stocks)):
            self.app.grid_columnconfigure(i, weight=1)

        self.app.grid_rowconfigure(0, weight=1)
        self.balance = customtkinter.CTkLabel(self.app, text="Portfolio Value: $0.00", font=("Bahnschrift", 12))
        self.balance.grid(row=1, column=0, columnspan=len(self.stocks), pady=10)

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
        self.update_balance()