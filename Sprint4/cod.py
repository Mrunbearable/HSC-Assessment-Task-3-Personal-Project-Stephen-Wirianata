import customtkinter
from datetime import datetime
from functools import partial

class Investment:
    def __init__(self, name, amount, rate_of_return, years):
        self.name = name
        self.amount = float(amount)
        self.rate_of_return = float(rate_of_return)
        self.years = years 

    def calculate_return(self, years):
        return self.amount * ((1 + self.rate_of_return/100) ** years)

class CertificateofDepositApp:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.portfolio = controller.portfolio
        self.time_options = {"6 months": 0.5,"12 months": 1,"5 years": 5,"10 years": 10,"20 years": 20} 
        self.selected_years = 1

        self.menuGui()

    def add_investment(self):
        name = self.entry_name.get()
        amount = self.entry_amount.get()
        rate_of_return = self.entry_rateofreturn.get()

        new_investment = Investment(name, amount, rate_of_return, self.selected_years)
        self.portfolio.append(new_investment)
        self.view_portfolio()

        for entry in [self.entry_name, self.entry_amount, self.entry_rateofreturn]:
            entry.delete(0, 'end')

        self.controller.history.append((datetime.now(), sum(inv.amount for inv in self.controller.portfolio)))

    def view_portfolio(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
            
        if not self.portfolio:
            label = customtkinter.CTkLabel(self.display_frame, text="Your portfolio is empty.", font=("Banschrift", 14), text_color="#2B2B2B")
            label.pack(pady=20)
            return

        for i, investment in enumerate(self.portfolio, start=1):
            text = f"{i}. {investment.name} - ${investment.amount:,.2f} ({investment.rate_of_return}% ROI, {investment.years} years)"
            label = customtkinter.CTkLabel(self.display_frame, text=text, font=("Banschrift", 12), text_color="#2B2B2B")
            label.pack(anchor="w", padx=10, pady=2)

    def calculate_returns(self):
        returns = []

        for investment in self.portfolio:
            future_value = investment.calculate_return(investment.years)
            returns.append(
                f"{investment.name}: ${future_value:,.2f}"
            )

        self.returns_label.configure(text="\n".join(returns))

    def remove_investment(self):
        name = self.entry_remove_name.get().strip()

        for investment in self.portfolio:
            if investment.name.lower() == name.lower():
                self.portfolio.remove(investment)
                self.view_portfolio()
                self.entry_remove_name.delete(0, "end")
                return

        self.controller.history.append((datetime.now(), sum(inv.amount for inv in self.controller.portfolio)))
    
    def set_years(self, option):    
        self.selected_years = self.time_options[option]
        self.returns_label.configure(text=f"Selected: {option}")

    def returnback(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    def menuGui(self):
        
        left_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=600, height=750)
        left_frame.grid(row=1, column=0, rowspan=2, padx=(20, 10), pady=20, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_propagate(False)

        righttop_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=800, height=350)
        righttop_frame.grid(row=1, column=1, padx=(10, 20), pady=(20, 10), sticky="nsew")
        righttop_frame.grid_columnconfigure(0, weight=1)
        righttop_frame.grid_propagate(False)
        righttop_frame.grid_rowconfigure(0, weight=1)
        righttop_frame.grid_columnconfigure(0, weight=1)

        rightbottom_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=800, height=300)
        rightbottom_frame.grid(row=2, column=1, padx=(10, 20), pady=(10, 20), sticky="new")
        rightbottom_frame.grid_columnconfigure(0, weight=1)
        rightbottom_frame.grid_propagate(False)

        customtkinter.CTkLabel(left_frame, text="Investment Name").grid(row=0, column=0, padx=20, pady=5, sticky="w")
        self.entry_name = customtkinter.CTkEntry(left_frame)
        self.entry_name.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        customtkinter.CTkLabel(left_frame, text="Amount").grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.entry_amount = customtkinter.CTkEntry(left_frame)
        self.entry_amount.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        customtkinter.CTkLabel(left_frame, text="Rate of Return (%)").grid(row=4, column=0, padx=20, pady=5, sticky="w")
        self.entry_rateofreturn = customtkinter.CTkEntry(left_frame)
        self.entry_rateofreturn.grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        period_frame = customtkinter.CTkFrame(left_frame, fg_color="transparent")
        period_frame.grid(row=7, column=0, padx=20, pady=10, sticky="nsew")
        period_frame.grid_columnconfigure((0, 1, 2), weight=1)

        customtkinter.CTkLabel(left_frame, text="Time Periods").grid(row=6, column=0, padx=20, pady=5, sticky="w")
        row = 0
        column = 0

        for option in self.time_options:
            optionsbutton = customtkinter.CTkButton(period_frame,text=option,width=40,height=40,corner_radius=999,fg_color="#06402B",command=partial(self.set_years, option))
            optionsbutton.grid(row=row, column=column, padx=5, pady=5, sticky="ew")

            column += 1
            if column == 2:  
                column = 0
                row += 1

        addinvestment_button = customtkinter.CTkButton(left_frame,text="Add Investment", fg_color="#06402B", command=self.add_investment)
        addinvestment_button.grid(row=13, column=0, padx=20, pady=10, sticky="ew")

        customtkinter.CTkLabel(left_frame,text="Remove an Investment").grid(row=14, column=0, padx=20, pady=(20, 5), sticky="w")
        self.entry_remove_name = customtkinter.CTkEntry(left_frame,placeholder_text="Investment name")
        self.entry_remove_name.grid(row=15, column=0, padx=20, pady=5, sticky="ew")

        removeinvestment_button = customtkinter.CTkButton(left_frame,text="Remove Investment", fg_color="#06402B", command=self.remove_investment)
        removeinvestment_button.grid(row=16, column=0, padx=20, pady=10, sticky="ew")

        self.display_frame = customtkinter.CTkFrame(righttop_frame)
        self.display_frame.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
        self.view_portfolio()

        customtkinter.CTkLabel(rightbottom_frame,text="Calculate Return On Investments").grid(row=0, column=0, padx=20, pady=5, sticky="w")
        self.entry_years = customtkinter.CTkEntry(rightbottom_frame)
        self.entry_years.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        
        calculate_button = customtkinter.CTkButton(rightbottom_frame,text="Calculate Returns", fg_color="#06402B", command=self.calculate_returns)
        calculate_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.returns_label = customtkinter.CTkLabel(rightbottom_frame, text="")
        self.returns_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        rightbottom_frame.grid_columnconfigure(0, weight=1)

        returnback_button = customtkinter.CTkButton(self.app,text="Back to Main Menu", fg_color="#06402B", width=800, height=30,command=self.returnback)
        returnback_button.place(x=640, y=735)