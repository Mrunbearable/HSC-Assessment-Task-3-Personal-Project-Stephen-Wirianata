import customtkinter
import requests
import pandas as pd
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from userdata import save_users

SYMBOL = "VOO"
TWELVEDATA_API_KEY = "91002cdaa44445d99142fd352da2e0dc"
TWELVEDATA_BASE_URL = "https://api.twelvedata.com"

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
        try:
            response = requests.get(
                f"{TWELVEDATA_BASE_URL}/time_series",
                params={
                    "symbol": SYMBOL,
                    "interval": "1day",
                    "outputsize": 60,
                    "apikey": TWELVEDATA_API_KEY,
                },
                timeout=10,
            )
            data = response.json()
        except Exception as e:
            print(f"[indexdatarequests] Exception fetching data: {e}")
            return pd.DataFrame()

        if not data or data.get("status") == "error" or "values" not in data:
            print(f"[indexdatarequests] No data for {SYMBOL}: {data}")
            return pd.DataFrame()

        values = data["values"]
        dataframe = pd.DataFrame({
            "4. close": [float(v["close"]) for v in values],
        }, index=pd.to_datetime([v["datetime"] for v in values]))
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
            frame.after(300000, self.update_graph, frame)
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

        frame.after(300000, self.update_graph, frame)

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
        self.controller.users_data[self.controller.current_user_token]["history"].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.controller.totalaccountbalance()))
        save_users(self.controller.users_data)
        self.update_balance()

    def sell(self):
        data = self.indexdatarequests()
        if data.empty:
            return

        price = float(data["4. close"].iloc[-1])
        sell_shares = int(self.indexentry.get())
        total = sum(inv.amount for inv in self.controller.indexfund_portfolio)

        if sell_shares > total:
            self.status.configure(text="Not enough shares to sell.", text_color="red")
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
        self.controller.frequentdatarefresh()
        self.controller.users_data[self.controller.current_user_token]["history"].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.controller.totalaccountbalance()))
        save_users(self.controller.users_data)
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
        
        self.balance = customtkinter.CTkLabel(right_frame,text="Portfolio: $0.00",font=("Bahnschrift", 35))
        self.balance.grid(row=0, column=0, pady=10)

        entry = customtkinter.CTkLabel(right_frame, font=("Bahnschrift", 20), text="Enter Number of Wanted Shares")
        entry.grid(row=1, column=0, pady=10)
        self.marketprice = customtkinter.CTkLabel(right_frame,text="Current market price: --",font=("Bahnschrift", 20))
        self.marketprice.grid(row=2, column=0, pady=10)
        self.marketgrowth = customtkinter.CTkLabel(right_frame, font=("Bahnschrift", 20), text="Current market growth: {}")
        self.marketgrowth.grid(row=3, column=0, pady=10)
        self.indexentry = customtkinter.CTkEntry(right_frame, placeholder_text="Enter amount")
        self.indexentry.grid(row=4, column=0, pady=10)

        savingsbutton_frame = customtkinter.CTkFrame(right_frame, fg_color="#E2C3A9")
        savingsbutton_frame.grid(row=5, column=0, pady=(15, 60))
        deposit_button = customtkinter.CTkButton(savingsbutton_frame, text="Buy", fg_color="#06402B", command=self.buy) 
        deposit_button.grid(row=0, column=0, padx=6)
        withdraw_button = customtkinter.CTkButton(savingsbutton_frame, text="Sell", fg_color="#06402B", command=self.sell)
        withdraw_button.grid(row=0, column=1, padx=6)

        self.status = customtkinter.CTkLabel(self.app, text="", font=("Bahnschrift", 20))
        self.status.grid(row=2, column=0, columnspan=2, pady=10)

        returnback_button = customtkinter.CTkButton(self.app,text="Back to Main Menu", fg_color="#06402B", width=800, height=30,command=self.returnback)
        returnback_button.place(x=500, y=720)

        self.setup_graph(left_frame)
        self.update_graph(left_frame)