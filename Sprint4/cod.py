#This is where the Certificate of Deposit (COD) interface is created, it purpose is to replicate a COD account in a bank
#Import CustomTkinter for GUI 
#Import datetime to time and update history
#Import partial to update progress bars in real time, and to automatically remember inputs so it becomes easier to manipulate later
import customtkinter
from datetime import datetime
from functools import partial

#Invesment Class is created to store the name, amount, rate of return, and years of the investment. 
#It also has a method to compound the investment and a method to calculate the progress of the investment.
class Investment:
    def __init__(self, name, amount, years):
        self.name = name
        self.amount = float(amount)
        self.rate_of_return = 5
        self.years = years
        self.compounded = False
        self.start = datetime.now()
    
    # A function to compound the investment amount based on the rate of return and the number of years. 
    # It updates the amount and sets compounded to True.
    def compound_period(self):
        self.amount *= (1 + self.rate_of_return / 100) ** float(self.years)
        self.compounded = True

    # A function to move the progress bar
    # Important to manipulate the feeling of a real COD investment
    def progress(self):
        total_seconds = self.years * 60
        elapsed = (datetime.now() - self.start).total_seconds()
        return min(elapsed / total_seconds, 1.0)

# A CertificateOfDepoist class for the COD investment
class CertificateofDepositApp:
    #Defining the variables
    #Controller used to go to different interface
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.portfolio = controller.cod_portfolio
        self.time_options = {"6 months": 0.5,"12 months": 1,"5 years": 5,"10 years": 10,"20 years": 20} 
        self.selected_years = 1

        self.menuGui()

    #A Function to add investments
    # User inputs name and amount of money
    #Check if the investment transfer is sucessful
    def add_investment(self):
        name = self.entry_name.get()
        amount = float(self.entry_amount.get())

        transfersuccess = self.deposit(amount)

        #If the transcation is not successful returns error message
        if not transfersuccess:
            self.returns_label.configure(text="Insufficient funds")
            return
        
        #Add specific data to specfic investment and adds investment to portfolio
        #Updates the history of accountbalance
        new_investment = Investment(name, amount, self.selected_years)
        self.portfolio.append(new_investment)
        self.controller.history.append((datetime.now(), self.controller.totalaccountbalance()))

        self.view_portfolio()
    
    #a function to deposit money
    def deposit(self, amount):
        # if the amount of money is more than the amount of money in main portfolio, you move the money from the account balance to the COD ivnestment
        if amount > self.controller.mainportfolio:
            return False
        self.controller.mainportfolio -= amount
        return True

    # A function to view portfolio, it destroys widgets and goes to one of two paths
    # if no portfolio, a message will be visible in a frame saying your portfolio is empty
    # if there is a portfolio, a message will be visible showing details for each investment a bar displaying progress based on time periods
    def view_portfolio(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
            
        if not self.portfolio:
            label = customtkinter.CTkLabel(self.display_frame, text="Your portfolio is empty.", font=("Banschrift", 14), text_color="#2B2B2B")
            label.pack(pady=20)
            return

        #For loop to show information for each investment if successful
        for i, investment in enumerate(self.portfolio, start=1):
            text = f"{i}. {investment.name} - ${investment.amount:,.2f} {investment.rate_of_return}%, {investment.years} yrs"
            time = customtkinter.CTkLabel(self.display_frame,text=text,font=("Banschrift", 12), text_color="#2B2B2B")
            time.pack(anchor="w", padx=10, pady=(6, 0))
            bar = customtkinter.CTkProgressBar(self.display_frame)
            bar.set(investment.progress())
            bar.pack(fill="x", padx=10, pady=(0, 8))

    #A function on calulate final return based on input, creates a new returns list
    def calculate_returns(self):
        returns = []
        for investment in self.portfolio:
            investment.compounded = False 
            investment.compound_period() 
            returns.append(f"{investment.name}: ${investment.amount:,.2f}")

        self.returns_label.configure(text="\n".join(returns))

    # A function to remove investment from portfolio
    # User enters name and it gets removed from portfolio based on lowercase name
    def remove_investment(self):
        name = self.entry_remove_name.get().strip()

        for investment in self.portfolio:
            if investment.name.lower() == name.lower():
                self.portfolio.remove(investment)
                self.controller.history.append((datetime.now(),sum(inv.amount for inv in self.controller.cod_portfolio)))
                self.view_portfolio()
                self.entry_remove_name.delete(0, "end")
                return

    #A function to verify the invesment progress/ bar progress
    def verify_cod(self):
        for investment in self.portfolio:
            if not investment.compounded and investment.progress() >= 1.0:
                investment.compound_period()
                self.controller.mainportfolio += investment.amount

        self.view_portfolio()
        self.display_frame.after(1000, self.verify_cod)
    
    # An information function for time periods, selects years based on user choice input
    def set_years(self, option):    
        self.selected_years = self.time_options[option]
        self.returns_label.configure(text=f"Selected: {option}")

    #A button to return back to main menu
    def returnback(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    #Creates the COD GUI, the sprint before this all contain at least one version of the COD GUI
    def menuGui(self):
        # Creates neccessary left frames
        left_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=600, height=750)
        left_frame.grid(row=1, column=0, rowspan=2, padx=(20, 10), pady=20, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_propagate(False)

        righttop_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=800, height=350)
        righttop_frame.grid(row=1, column=1, padx=(10, 20), pady=(20, 10), sticky="nsew")
        righttop_frame.grid_columnconfigure(0, weight=1)
        righttop_frame.grid_propagate(False)
        righttop_frame.grid_rowconfigure(0, weight=1)

        rightbottom_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=800, height=300)
        rightbottom_frame.grid(row=2, column=1, padx=(10, 20), pady=(10, 20), sticky="new")
        rightbottom_frame.grid_columnconfigure(0, weight=1)
        rightbottom_frame.grid_propagate(False)

        #Creates buttons, labels and entrys
        customtkinter.CTkLabel(left_frame, text="Investment Name").grid(row=0, column=0, padx=20, pady=5, sticky="w")
        self.entry_name = customtkinter.CTkEntry(left_frame)
        self.entry_name.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        customtkinter.CTkLabel(left_frame, text="Amount").grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.entry_amount = customtkinter.CTkEntry(left_frame)
        self.entry_amount.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        period_frame = customtkinter.CTkFrame(left_frame, fg_color="transparent")
        period_frame.grid(row=7, column=0, padx=20, pady=10, sticky="nsew")
        period_frame.grid_columnconfigure((0, 1, 2), weight=1)

        #A for loop to showcase time options, saves space and is more efficient
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

        #Display frame from portfolio
        self.display_frame = customtkinter.CTkFrame(righttop_frame)
        self.display_frame.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
        self.view_portfolio()
        self.display_frame.after(1000, self.view_portfolio)

        customtkinter.CTkLabel(rightbottom_frame,text="Calculate Return On Investments").grid(row=0, column=0, padx=20, pady=5, sticky="w")
        calculate_button = customtkinter.CTkButton(rightbottom_frame,text="Calculate Returns", fg_color="#06402B", command=self.calculate_returns)
        calculate_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.returns_label = customtkinter.CTkLabel(rightbottom_frame, text="")
        self.returns_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        rightbottom_frame.grid_columnconfigure(0, weight=1)

        returnback_button = customtkinter.CTkButton(self.app,text="Back to Main Menu", fg_color="#06402B", width=800, height=30,command=self.returnback)
        returnback_button.place(x=640, y=735)
        # runs verify COD
        self.verify_cod()

        