import customtkinter
from menu import InvestmentMenu
from investment import InvestmentApp

class SmartInvestmentApp:
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.title("SMART INVESTMENTS")
        self.app.geometry("1400x1000")
        self.portfolio = []

        customtkinter.set_appearance_mode("Light")

        self.app.configure(fg_color="#F7E7CE")
        self.operate_menu()

    def clear_window(self):
        for widget in self.app.winfo_children():
            widget.destroy()

    def operate_investment(self):
        self.clear_window()
        InvestmentApp(self)

    def operate_menu(self):
        self.clear_window()
        InvestmentMenu(self)

    def start(self):
        self.app.mainloop()


if __name__ == "__main__":
    app = SmartInvestmentApp()
    app.start()