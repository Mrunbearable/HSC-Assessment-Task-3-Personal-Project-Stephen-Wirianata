import customtkinter
from datetime import datetime
from menu import InvestmentMenu
from cod import CertificateofDepositApp
from saving import SavingsApp
from index import IndexApp
from stock import StockMarketApp
from authentication import AuthenticationSystem
from leaderboard import LeaderboardApp
from userdata import load_users, save_users

class SmartInvestmentApp:
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.title("SMART INVESTMENTS")
        self.app.geometry("1400x1000")
        customtkinter.set_appearance_mode("Light")
        self.app.configure(fg_color="#F7E7CE")
        self.savings_portfolio = []
        self.cod_portfolio = []
        self.indexfund_portfolio = []
        self.stockmarket_portfolio = []
        self.history = []
        self.mainportfolio = 500.0
        self.current_user = None
        self.current_user_token = None

        self.users_data = load_users()
        self.operate_authenticationsystem()
        self.app.after(10000, self.interestautomation)
        self.app.after(300000, self.frequenthistoryrefresh)

    def apply_interest(self):
        if not self.current_user_token:
            return

        for inv in self.savings_portfolio:
            if inv.rate_of_return > 0:
                inv.compound_weekly()

        for inv in self.cod_portfolio:
            if not inv.compounded:
                inv.compound_period()
                inv.compounded = True

        self.frequentdatarefresh()
        self.users_data[self.current_user_token]["history"].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.totalaccountbalance()))
        save_users(self.users_data)

    def frequenthistoryrefresh(self):
        if self.current_user_token:
            self.users_data[self.current_user_token]["history"].append(
                (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    self.totalaccountbalance()
                )
            )
            save_users(self.users_data)

        self.app.after(300000, self.frequenthistoryrefresh)

    def interestautomation(self):
        self.apply_interest()
        self.app.after(10000, self.interestautomation)

    def totalaccountbalance(self):
        savings = sum(inv.amount for inv in self.savings_portfolio)
        cod = sum(inv.amount for inv in self.cod_portfolio)
        indexfund = sum(inv.amount for inv in self.indexfund_portfolio)
        stockmarket = sum(inv.amount for inv in self.stockmarket_portfolio)

        return self.mainportfolio + savings + cod + indexfund + stockmarket

    def frequentdatarefresh(self):
        if not self.current_user_token:
            return

        user = self.users_data[self.current_user_token]

        savings = sum(inv.amount for inv in self.savings_portfolio)
        cod = sum(inv.amount for inv in self.cod_portfolio)
        indexfund = sum(inv.amount for inv in self.indexfund_portfolio)
        stocks = sum(inv.amount for inv in self.stockmarket_portfolio)

        total = self.mainportfolio + savings + cod + indexfund + stocks

        user["balances"] = {"total": total,"hysa": savings, "cod": cod, "indexfund": indexfund, "stocks": stocks}
        user["savings_portfolio"] = [{"amount": inv.amount,"rate": inv.rate_of_return} for inv in self.savings_portfolio]
        user["cod_portfolio"] = [{"name": inv.name,"amount": inv.amount,"years": inv.years,"compounded": inv.compounded} for inv in self.cod_portfolio]
        user["indexfund_portfolio"] = [{"symbol": inv.name,"shares": inv.amount}for inv in self.indexfund_portfolio]
        user["stockmarket_portfolio"] = [{"symbol": inv.name,"shares": inv.amount} for inv in self.stockmarket_portfolio]
        user["mainportfolio"] = self.mainportfolio
        save_users(self.users_data)

    def connectdatabase(self):
        self.frequentdatarefresh()
        save_users(self.users_data)
    
    def clear_window(self):
        for widget in self.app.winfo_children():
            widget.destroy()

    def operate_authenticationsystem(self):
        self.clear_window()
        AuthenticationSystem(self)

    def operate_leaderboard(self):
        self.clear_window()
        LeaderboardApp(self)

    def operate_cod(self):
        self.clear_window()
        CertificateofDepositApp(self)

    def operate_savings(self):
        self.clear_window()
        SavingsApp(self)

    def operate_index(self):
        self.clear_window()
        IndexApp(self)

    def operate_stock(self):
        self.clear_window()
        StockMarketApp(self)

    def operate_menu(self):
        self.clear_window()
        InvestmentMenu(self)

    def start(self):
        self.app.mainloop()


if __name__ == "__main__":
    app = SmartInvestmentApp()
    app.start()