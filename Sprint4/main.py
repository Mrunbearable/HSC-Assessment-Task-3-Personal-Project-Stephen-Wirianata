import customtkinter
from datetime import datetime
from menu import InvestmentMenu
from cod import CertificateofDepositApp
from saving import SavingsApp
from index import IndexApp

class SmartInvestmentApp:
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.title("SMART INVESTMENTS")
        self.app.geometry("1400x1000")
        self.savings_portfolio = []
        self.cod_portfolio = []
        self.indexfund_portfolio = []
        self.stockmarktet_portfolio = []
        self.history = []
        self.mainportfolio = 100.0

        customtkinter.set_appearance_mode("Light")
        self.app.configure(fg_color="#F7E7CE")  

        self.operate_menu()
        self.app.after(10000, self.interestautomation)

    def apply_interest(self):
        for inv in self.savings_portfolio:
            if inv.rate_of_return > 0:
                inv.compound_weekly()
        
        for inv in self.cod_portfolio:
                if not inv.compounded:
                    inv.compound_period(inv.years)
                    inv.compounded = True

        self.history.append((datetime.now(), self.totalaccountbalance()))


    def interestautomation(self):
        self.apply_interest()
        self.app.after(5000, self.interestautomation) 

    def totalaccountbalance(self):
        savings = sum(inv.amount for inv in self.savings_portfolio)
        cod = sum(inv.amount for inv in self.cod_portfolio)
        index = sum(inv.shares * inv.buy_price for inv in self.indexfund_portfolio)

        return self.mainportfolio + savings + cod + index
        
    def clear_window(self):
        for widget in self.app.winfo_children():
            widget.destroy()

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

    