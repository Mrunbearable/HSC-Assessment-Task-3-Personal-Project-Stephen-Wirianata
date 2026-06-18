import customtkinter
import requests
import pandas as pd
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

API_KEY = "N8I5DJYIP7RH1BC6"
SYMBOLS = {"NVDA", "ALAB", "ORCL", "GOOGL", "SPCX"}
    
class StockMarketApp:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.stocks = SYMBOLS   
        self.menuGui()
        self.update_balance()

    def stockdatarequests(self):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        time_series = data.get("Time Series (Daily)", {})
        dataframe = pd.DataFrame.from_dict(time_series, orient="index")
        dataframe = dataframe.astype(float)
        dataframe.index = pd.to_datetime(dataframe.index)
        dataframe = dataframe.sort_index()

        return dataframe

    def setup_graph(self, frame):
            self.figure, self.axis = plt.subplots(figsize=(6, 3))
            self.canvas = FigureCanvasTkAgg(self.figure, master=frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_graph(self, frame):
        data = self.indexdatarequests()
        if data.empty:
            frame.after(60000, self.update_graph, frame)
            return

        latest_price = data.iloc[-1]["4. close"]
        self.marketprice_label.configure(text=f"Current market price: ${latest_price:.2f}")

        start = float(data["4. close"].iloc[0])
        end = float(data["4. close"].iloc[-1])
        growth = ((end - start) / start) * 100
        self.marketgrowth_label.configure(text=f"Market growth: {growth:.2f}%")

        self.axis.clear()
        self.axis.plot(data.index, data["4. close"], color="#06402B")
        self.axis.set_title("VOO Live Price")
        self.axis.set_ylabel("Price")
        self.axis.grid(True)
        self.figure.autofmt_xdate()
        self.canvas.draw()

        frame.after(60000, self.update_graph, frame)

    def get_latest_price(self, data):
        return float(data["4. close"].iloc[-1])

    def buy(self):
        data = self.indexdatarequests()
        if data.empty:
            return

        price = float(data["4. close"].iloc[-1])
        cash = float(self.amount_entry.get())
        shares = int(cash // price)

        if shares <= 0:
            print("Not enough money to buy 1 share")
            return

        cost = shares * price

        if self.controller.mainportfolio < cost:
            print("Not enough cash in account")
            return
        self.controller.mainportfolio -= cost

        inv = Investment(name=SYMBOL, amount=shares, rate_of_return=0)
        self.controller.savings_portfolio.append(inv)
        self.controller.history.append((datetime.now(), self.controller.totalaccountbalance()))
        self.update_balance()

    def sell(self):
        data = self.indexdatarequests()
        if data.empty:
          return

        price = float(data["4. close"].iloc[-1])
        shares_to_sell = int(float(self.amount_entry.get()))
        total_shares = sum(inv.amount for inv in self.controller.savings_portfolio)

        if shares_to_sell > total_shares:
            print("Not enough shares")
            return

        remaining = shares_to_sell
        new_portfolio = []

        for inv in self.controller.savings_portfolio:
            if remaining <= 0:
                new_portfolio.append(inv)

            elif inv.amount <= remaining:
                remaining -= inv.amount

            else:
                inv.amount -= remaining
                new_portfolio.append(inv)
                remaining = 0

        self.controller.savings_portfolio = new_portfolio
        self.controller.mainportfolio += shares_to_sell * price
        self.controller.history.append((datetime.now(), self.controller.totalaccountbalance()))
        self.update_balance()
        
    def update_balance(self):
        data = self.indexdatarequests()
        if data.empty:
            return

        price = float(data["4. close"].iloc[-1])
        shares = sum(inv.amount for inv in self.controller.savings_portfolio)
        value = shares * price

        self.balance_label.configure(text=f"Portfolio Value: ${value:.2f} ({shares:.0f} shares)")

    def returnback(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    def menuGui(self):
        for i, stock in enumerate(self.stocks):
            stockframe = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=600, height=750)
            stockframe.grid(row=i+1, column=0, rowspan=2, padx=(20, 10), pady=20, sticky="nsew")
            stockframe.grid_columnconfigure(0, weight=1)
            stockframe.grid_propagate(False)

            marketprice_label = customtkinter.CTkLabel(stockframe, text=f"{stock} Price: --",font=("Bahnschrift", 10))
            marketprice_label.grid(row=0, column=0, padx=10)

            marketgrowth_label = customtkinter.CTkLabel(stockframe, text=f"{stock} Price: --",font=("Bahnschrift", 10))
            marketgrowth_label.grid(row=0, column=1, padx=10)

        right_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=800, height=750)
        right_frame.grid(row=1, column=1, padx=(10, 20), pady=(20, 10), sticky="nsew")
        right_frame.grid_propagate(False)
        right_frame.grid_columnconfigure(0, weight=1)
        
        self.balance_label = customtkinter.CTkLabel(right_frame,text="Savings: $0.00",font=("Bahnschrift", 18))
        self.balance_label.grid(row=0, column=0, pady=10)

        #returnback_button = customtkinter.CTkButton(self.app,text="Back to Main Menu", fg_color="#06402B", width=1500, height=30,command=self.returnback)
        #returnback_button.place(x=20, y=640)

        self.setup_graph(stockframe, stockframe2, stockframe, stockframe4, stockframe5)
        self.update_graph(stockframe, stockframe2, stockframe3, stockframe4, stockframe5)


