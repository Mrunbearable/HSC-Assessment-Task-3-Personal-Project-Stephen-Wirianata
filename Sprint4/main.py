import customtkinter
from datetime import datetime
from menu import InvestmentMenu
from cod import CertificateofDepositApp
from saving import SavingsApp

class SmartInvestmentApp:
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.title("SMART INVESTMENTS")
        self.app.geometry("1400x1000")
        self.portfolio = []
        self.history = []

        customtkinter.set_appearance_mode("Light")
        self.app.configure(fg_color="#F7E7CE")  

        self.operate_menu()

    def clear_window(self):
        for widget in self.app.winfo_children():
            widget.destroy()

    def operate_cod(self):
        self.clear_window()
        CertificateofDepositApp(self)

    def operate_savings(self):
        self.clear_window()
        SavingsApp(self)

    def operate_menu(self):
        self.clear_window()
        InvestmentMenu(self)

    def start(self):
        self.app.mainloop()


if __name__ == "__main__":
    app = SmartInvestmentApp()
    app.start()

    