# This is the main menu, connecting all different investment oppurtunities
# Import CustomTkinter for GUI
# Import datetime to handle history and updates
# Import Investment classes from different python files, allowing interfaces to work collectively
import customtkinter
from datetime import datetime
from menu import InvestmentMenu
from cod import CertificateofDepositApp
from saving import SavingsApp
from index import IndexApp
from stock import StockMarketApp

#Smart Investment APP, creates the variable to set up GUI interface and its aesthetics, this is also where the main and seperate investment portfolios are made
# Sets mainportfolio money to 10000 dollars
# Start program at menu interface
class SmartInvestmentApp:
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.title("SMART INVESTMENTS")
        self.app.geometry("1400x1000")
        self.savings_portfolio = []
        self.cod_portfolio = []
        self.indexfund_portfolio = []
        self.stockmarket_portfolio = []
        self.history = []
        self.mainportfolio = 10000.0

        customtkinter.set_appearance_mode("Light")
        self.app.configure(fg_color="#F7E7CE")  

        self.operate_menu()
        self.app.after(300000, self.interestautomation)

    # A function to apply interest for savings and cod investment oppurtunities
    #updates balance based on interest
    def apply_interest(self):
        for inv in self.savings_portfolio:
            if inv.rate_of_return > 0:
                inv.compound_weekly()
        
        for inv in self.cod_portfolio:
                if not inv.compounded:
                    inv.compound_period()
                    inv.compounded = True

        self.history.append((datetime.now(), self.totalaccountbalance()))

    # The interestautomation function which automatically applies interest to savings and py
    def interestautomation(self):
        self.apply_interest()
        self.app.after(300000, self.interestautomation) 

    # A function for the total account balance, calculates total money in all for investment oppurtunities and returns total money/account balance
    def totalaccountbalance(self):
        savings = sum(inv.amount for inv in self.savings_portfolio)
        cod = sum(inv.amount for inv in self.cod_portfolio)
        indexfund = sum(inv.amount for inv in self.indexfund_portfolio)
        stockmarket = sum(inv.amount for inv in self.stockmarket_portfolio)

        return self.mainportfolio + savings  + cod + indexfund + stockmarket 
    
    # A function for clearing the windo, destroying widgets.
    def clear_window(self):
        for widget in self.app.winfo_children():
            widget.destroy()

    # a function to run cod interface
    def operate_cod(self):
        self.clear_window()
        CertificateofDepositApp(self)

    # a function to run savings interface
    def operate_savings(self):
        self.clear_window()
        SavingsApp(self)

    #A function to run index interface
    def operate_index(self):
        self.clear_window()
        IndexApp(self)

    # A function to run stock interface
    def operate_stock(self):
        self.clear_window()
        StockMarketApp(self)

    # A function to run menu interface  
    def operate_menu(self):
        self.clear_window()
        InvestmentMenu(self)

    #A function to start program
    def start(self):
        self.app.mainloop()

#Starts program by checking if there is smart investment app
if __name__ == "__main__":
    app = SmartInvestmentApp()
    app.start()

    