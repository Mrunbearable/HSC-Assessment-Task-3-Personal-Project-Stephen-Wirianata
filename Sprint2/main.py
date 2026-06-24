# Introduction of a GUI, from a console UI
# Imports Custotkinter library, to create the GUI for the invest app
# This will allow users to interact with the app in a more user-friendly way, making it easier to manage their investments and view their portfolio.
import customtkinter

#Introduction of Object-Oriented Programming, creating an Investment class to represent each investment in the portfolio
class Investment:
    #Defining attributes of the Investment class
    def __init__(self, name, amount, rate_of_return):
        self.name = name
        self.amount = float(amount)
        self.rate_of_return = float(rate_of_return) 
    # A function to calculate the future value of investment, compounding function which is important for app purposes
    def calculate_return(self, years):
        return self.amount * ((1 + self.rate_of_return/100) ** years)

# Another class created using OOP, to represent the main application and its functionalities, allowing for better organization and modularity of the code.
class InvestmentApp:
    #defining attributes of the InvestmentApp class, including the main portfolio, GUI Specifications and the user's current investments
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.title("SMART INVESTMENTS")
        self.app.geometry("1400x1000")
        self.portfolio = []

        customtkinter.set_appearance_mode("Light")

        self.app.configure(fg_color="#F7E7CE")

    # A function to add an investment to the portfolio, allowing users to input the details of their investment and have it added to their portfolio for management and tracking purposes.
    def add_investment(self):
        # User inputs for investment details
        name = self.entry_name.get()
        amount = self.entry_amount.get()
        rate_of_return = self.entry_rateofreturn.get()

        # Saves details for specfic investments and adds to porfolio list
        new_investment = Investment(name, amount, rate_of_return)
        self.portfolio.append(new_investment)
        self.view_portfolio()

        # Clears the input fields after adding an investment, improving user experience by allowing them to easily add multiple investments without having to manually clear the fields each time.
        for entry in [self.entry_name, self.entry_amount, self.entry_rateofreturn]:
            entry.delete(0, 'end')

    # A function to view the current portfolio, displaying the details of each investment in a user-friendly format, allowing users to easily see and manage their investments.
    #Clears widgets before displaying the portfolio, ensuring that the display is updated correctly and prevents any overlapping or cluttered information on the screen.
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
            text = f"{i}. {investment.name} - ${investment.amount:,.2f} ({investment.rate_of_return}%)"
            label = customtkinter.CTkLabel(self.display_frame, text=text, font=("Banschrift", 12), text_color="#2B2B2B")
            label.pack(anchor="w", padx=10, pady=2)

    # a function to calculate the returns on investments, allowing users to input the number of years and see the future value of their investmens
    # creates a returns list
    def calculate_returns(self):
            years = int(self.entry_years.get())
            returns = []
            
            # a for loop to calculate the future value of each investment
            # prints each invesment's name, amount and future value after the specified number of years
            for investment in self.portfolio:
                future_value = investment.calculate_return(years)
                print(f"{investment.name}{investment.amount:.2f} After {years} years: {future_value:.2f}")
                returns.append(f"{investment.name}: ${future_value:.2f}")
                self.returns_label.configure(text="\n".join(returns))

    # A function to remove investments from the portfolio
    def remove_investment(self):
        # Enter the name of invesment
        name = self.entry_remove_name.get().strip()

        # Finds the name in lowercase in the portolio and remove it
        for investment in self.portfolio:
            if investment.name.lower() == name.lower():
                self.portfolio.remove(investment)
                self.view_portfolio()
                self.entry_remove_name.delete(0, "end")
                return

    #Creates the menu GUI, allowing users to interact with graphical user interface
    def menuGui(self):
        
        #Creates frames for the layout of the GUI, organizing the different sections of the interface for better user experience and navigation.
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

        rightbottom_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=800, height=350)
        rightbottom_frame.grid(row=2, column=1, padx=(10, 20), pady=(10, 20), sticky="nsew")
        rightbottom_frame.grid_columnconfigure(0, weight=1)
        rightbottom_frame.grid_propagate(False)

        #Creates the labels, entry fields and buttons for the GUI, allowing users to input their investment details, view their portfolio, calculate returns, and remove investments in an interactive and user-friendly way.
        customtkinter.CTkLabel(left_frame, text="Investment Name").grid(row=0, column=0, padx=20, pady=5, sticky="w")
        self.entry_name = customtkinter.CTkEntry(left_frame)
        self.entry_name.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        customtkinter.CTkLabel(left_frame, text="Amount").grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.entry_amount = customtkinter.CTkEntry(left_frame)
        self.entry_amount.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        customtkinter.CTkLabel(left_frame, text="Rate of Return (%)").grid(row=4, column=0, padx=20, pady=5, sticky="w")
        self.entry_rateofreturn = customtkinter.CTkEntry(left_frame)
        self.entry_rateofreturn.grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        addinvestment_button = customtkinter.CTkButton(left_frame,text="Add Investment",command=self.add_investment)
        addinvestment_button.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        customtkinter.CTkLabel(left_frame,text="Remove an Investment").grid(row=7, column=0, padx=20, pady=(20, 5), sticky="w")
        self.entry_remove_name = customtkinter.CTkEntry(left_frame,placeholder_text="Investment name")
        self.entry_remove_name.grid(row=8, column=0, padx=20, pady=5, sticky="ew")

        removeinvestment_button = customtkinter.CTkButton(left_frame,text="Remove Investment",command=self.remove_investment)
        removeinvestment_button.grid(row=9, column=0, padx=20, pady=10, sticky="ew")

        # A special frame to store buttons
        self.display_frame = customtkinter.CTkFrame(righttop_frame)
        self.display_frame.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
        self.view_portfolio()

        customtkinter.CTkLabel(rightbottom_frame,text="Calculate Return On Investments").grid(row=0, column=0, padx=20, pady=5, sticky="w")
        self.entry_years = customtkinter.CTkEntry(rightbottom_frame)
        self.entry_years.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        
        calc_button = customtkinter.CTkButton(rightbottom_frame,text="Calculate Returns",command=self.calculate_returns)
        calc_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.returns_label = customtkinter.CTkLabel(rightbottom_frame, text="")
        self.returns_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        rightbottom_frame.grid_columnconfigure(0, weight=1)

        #Run the application
        self.app.mainloop()

#If the applications is running, run the menu GUI, allowing users to interact with the application and manage their investments through the graphical user interface.
if __name__ == "__main__":

    app = InvestmentApp()
    app.menuGui()
        