# This is introduction of the 
# Imports customtkinter for GUI, allowing users to interact with the app in a more user-friendly way, making it easier to manage their investments and view their portfolio.
# Imports datetime for handling date and time, important for history updates
# Imports partial from functools for updating map in menu
import customtkinter
from datetime import datetime
from functools import partial

# An investment class is created to represent each investment in the portfolio, 
class Investment:
    #Defining the variables for the investment class, including the name, amount, rate of return and years
    def __init__(self, name, amount, rate_of_return, years):
        self.name = name
        self.amount = float(amount)
        self.rate_of_return = float(rate_of_return)
        self.years = years 

    # A calculation function to calculate the future value of investment, compounding function which is important for app purposes
    def calculate_return(self, years):
        return self.amount * ((1 + self.rate_of_return/100) ** years)

# Another class created using OOP, to represent the main application and its functionalities, allowing for better organization and modularity of the code.
class InvestmentApp:
    # defining attributes of the InvestmentApp class, including the main portfolio, GUI Specifications and the user's current investments
    # new addition of time periods, which is unique compared to other inputs
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.portfolio = controller.portfolio
        self.time_options = {"6 months": 0.5,"12 months": 1,"5 years": 5,"10 years": 10,"20 years": 20} 
        self.selected_years = 1

        self.menuGui()

    # A function to add an investment to the portfolio, allowing users to input the details of their investment
    def add_investment(self):
        name = self.entry_name.get()
        amount = self.entry_amount.get()
        rate_of_return = self.entry_rateofreturn.get()

        # adds specfic investments and adds to porfolio list
        new_investment = Investment(name, amount, rate_of_return, self.selected_years)
        self.portfolio.append(new_investment)
        self.view_portfolio()

        # Clears the input fields after adding an investment, improving user experience by allowing them to easily add multiple investments without having to manually clear the fields each time.
        for entry in [self.entry_name, self.entry_amount, self.entry_rateofreturn]:
            entry.delete(0, 'end')

        #Adds the update to the history in the main portfolio
        self.controller.history.append((datetime.now(), sum(inv.amount for inv in self.controller.portfolio)))

    # A function to view portfolio
    # destorys any widgets in the display frame to prevent crashing
    def view_portfolio(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        
        # Checks if the portfolio is empty and displays a message if it is, providing feedback to the user
        if not self.portfolio:
            label = customtkinter.CTkLabel(self.display_frame, text="Your portfolio is empty.", font=("Banschrift", 14), text_color="#2B2B2B")
            label.pack(pady=20)
            return

        # Displays each investment in the portfolio with its details, allowing users to easily see and manage their investments in a clear and organized manner.
        for i, investment in enumerate(self.portfolio, start=1):
            text = f"{i}. {investment.name} - ${investment.amount:,.2f} ({investment.rate_of_return}% ROI, {investment.years} years)"
            label = customtkinter.CTkLabel(self.display_frame, text=text, font=("Banschrift", 12), text_color="#2B2B2B")
            label.pack(anchor="w", padx=10, pady=2)

    # a function to calculate the returns on investments, allowing users to input the number of years and see the future value of their investmens
    # creates a returns list
    def calculate_returns(self):
        returns = []

        # A for loop to calculate the future value of each investment in the portfolio and add it to the returns list, allowing users to see the potential growth of their investments over time.
        for investment in self.portfolio:
            future_value = investment.calculate_return(investment.years)
            returns.append(
                f"{investment.name}: ${future_value:,.2f}"
            )

        self.returns_label.configure(text="\n".join(returns))

    # A function to remove investments from the portfolio
    # User enters name of investment to remove
    def remove_investment(self):
        name = self.entry_remove_name.get().strip()

        # Finds the name in lowercase in the portolio and remove it
        for investment in self.portfolio:
            if investment.name.lower() == name.lower():
                self.portfolio.remove(investment)
                self.view_portfolio()
                self.entry_remove_name.delete(0, "end")
                return

        #Adds the update to the history in the main portfolio
        self.controller.history.append((datetime.now(), sum(inv.amount for inv in self.controller.portfolio)))
    
    # a function set years for investment
    # sets selected years based on option chosen by user and returns a label saying selected options
    def set_years(self, option):    
        self.selected_years = self.time_options[option]
        self.returns_label.configure(text=f"Selected: {option}")

    # A function to return between interfaces
    def returnback(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    # A GUI function, this is the customisation of the graphical user interface
    def menuGui(self):
        
        # creates the frames for the layout of the GUI, organizing the different sections of the interface for better user experience and navigation.
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

        # Creates the labels, entry fields and buttons for the GUI, allowing users to input their investment details, view their portfolio, calculate returns, and remove investments in an interactive and user-friendly way.
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

        # specific to time period options, but creates buttons using for loop for each time period option
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

        # Continue adding buttons, labels and enetry files for GUI
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
        # BUtton to return back to menu
        returnback_button = customtkinter.CTkButton(self.app,text="Back to Main Menu", fg_color="#06402B", width=800, height=30,command=self.returnback)
        returnback_button.place(x=640, y=735)