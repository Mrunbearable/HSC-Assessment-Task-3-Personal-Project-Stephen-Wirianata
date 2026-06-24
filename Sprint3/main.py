# This file operates between different interfaces, it also set up how the acutal interface will look
# imports customtkinter for the GUI
# imports time for updating history
import customtkinter
from datetime import datetime
#Connection between menu.py and main.py
#imports InvestmentMenu class from menu.py to main.py
from menu import InvestmentMenu
#Connection between investment.py and main.py
#imports InvestmentApp class from investment.py to main.py
from investment import InvestmentApp

# The main app class to define variable for how the GUI will look
# Also the Connection between the different interfaces, it operates the menu and investment interface
class SmartInvestmentApp:
    # defines the main app variables
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.title("SMART INVESTMENTS")
        self.app.geometry("1400x1000")
        self.portfolio = []
        self.history = []

        customtkinter.set_appearance_mode("Light")
        self.app.configure(fg_color="#F7E7CE")  

        self.operate_menu()

    # a function to clear the window, this is used when switching between interfaces
    def clear_window(self):
        for widget in self.app.winfo_children():
            widget.destroy()

    #a function to run the investment interface
    def operate_investment(self):
        self.clear_window()
        InvestmentApp(self)

    # a function to run the menu interface
    def operate_menu(self):
        self.clear_window()
        InvestmentMenu(self)

    # a function to start the program
    def start(self):
        self.app.mainloop()

# Starts the program by checking if there is smartinvestmentapp
if __name__ == "__main__":
    app = SmartInvestmentApp()
    app.start()

    