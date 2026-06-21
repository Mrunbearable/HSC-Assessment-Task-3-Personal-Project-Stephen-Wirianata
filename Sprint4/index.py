import customtkinter
import requests
import pandas as pd
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

API_KEY = "N8I5DJYIP7RH1BC6"
SYMBOL = "VOO"

class Investment:
    def __init__(self, name, amount):
        self.name = name    
        self.amount = float(amount)
        self.rate_of_return = 0
        self.years = 0
        

class IndexApp:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.menuGui()
        self.update_balance()

    def indexdatarequests(self):
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
        self.marketprice.configure(text=f"Current market price: ${latest_price:.2f}")

        start = float(data["4. close"].iloc[0])
        end = float(data["4. close"].iloc[-1])
        growth = ((end - start) / start) * 100
        self.marketgrowth.configure(text=f"Market growth: {growth:.2f}%")

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
        shares = int(self.indexentry.get())

        if shares <= 0:
            print("Enter valid shares")
            return

        cost = shares * price

        if self.controller.mainportfolio < cost:
            print("Not enough cash in main portfolio")
            return

        self.controller.mainportfolio -= cost
        inv = Investment(name=SYMBOL, amount=shares)
        self.controller.indexfund_portfolio.append(inv)
        self.controller.history.append((datetime.now(), self.controller.totalaccountbalance()))
        self.update_balance()

    def sell(self):
        data = self.indexdatarequests()
        if data.empty:
            return

        price = float(data["4. close"].iloc[-1])
        sell_shares = int(self.indexentry.get())
        total = sum(inv.amount for inv in self.controller.indexfund_portfolio)

        if sell_shares > total:
            print("Not enough shares")
            return

        remaining = sell_shares
        new_portfolio = []

        for inv in self.controller.indexfund_portfolio:
            if remaining <= 0:
                new_portfolio.append(inv)
            elif inv.amount <= remaining:
                remaining -= inv.amount
            else:
                inv.amount -= remaining
                new_portfolio.append(inv)
                remaining = 0

        self.controller.indexfund_portfolio = new_portfolio
        self.controller.mainportfolio += sell_shares * price
        self.controller.history.append((datetime.now(), self.controller.totalaccountbalance()))
        self.update_balance()
        
    def update_balance(self):
        data = self.indexdatarequests()
        if data.empty:
            return

        price = float(data["4. close"].iloc[-1])
        shares = sum(inv.amount for inv in self.controller.indexfund_portfolio if inv.name == SYMBOL)
        value = shares * price
        self.balance.configure(text=f"VOO Value: ${value:.2f} ({shares:.0f} shares)")

    def returnback(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    def menuGui(self):
        
        left_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=600, height=750)
        left_frame.grid(row=1, column=0, rowspan=2, padx=(20, 10), pady=20, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_propagate(False)

        right_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=800, height=750)
        right_frame.grid(row=1, column=1, padx=(10, 20), pady=(20, 10), sticky="nsew")
        right_frame.grid_propagate(False)
        right_frame.grid_columnconfigure(0, weight=1)
        
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

        savingsbutton_frame = customtkinter.CTkFrame(right_frame, fg_color="#E2C3A9")
        savingsbutton_frame.grid(row=5, column=0, pady=(15, 60))

        deposit_button = customtkinter.CTkButton(savingsbutton_frame, text="Deposit", fg_color="#06402B", command=self.buy) 
        deposit_button.grid(row=0, column=0, padx=6)

        withdraw_button = customtkinter.CTkButton(savingsbutton_frame, text="Withdraw", fg_color="#06402B", command=self.sell)
        withdraw_button.grid(row=0, column=1, padx=6)

        returnback_button = customtkinter.CTkButton(self.app,text="Back to Main Menu", fg_color="#06402B", width=800, height=30,command=self.returnback)
        returnback_button.place(x=1000, y=650)

        self.setup_graph(left_frame)
        self.update_graph(left_frame)

