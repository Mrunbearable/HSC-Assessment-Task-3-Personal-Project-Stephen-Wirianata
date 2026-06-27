#An interesting functionality, a leadboard to show growth between players and promote healthy friendly competition
#Import CustomTKinter for GUI
import customtkinter

#Initals Starting balance as 500 dollars
STARTING_BALANCE = 500

#Gets the total balance of the current user
def obtainbalancekey(entry):
    return entry["total"]

# A Leaderboard Class, containing all leaderboard function and connecting to main.py
class LeaderboardApp:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.menuGui()

    # A function to get ranking of user
    def get_rankings(self):
        #Gets user
        users = self.controller.users_data
        #Creates ranking list
        rankings = []

        # A foor loop to get user, total and growth variables, adding it to leaderboard
        for user_id, data in users.items():
            username = data.get("username", "Unknown")
            total = data.get("balances", {}).get("total", 0.0)
            growth = ((total - STARTING_BALANCE) / STARTING_BALANCE) * 100

            rankings.append({"username": username, "total": total, "growth": growth})

        #Sort by rankings
        rankings.sort(key=obtainbalancekey, reverse=True)

        return rankings

    #Refreshes the list frequently
    def listrefresh(self):
        #destroying widgets so program doesn't crash
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        #fetches rankings
        rankings = self.get_rankings()
        #If there are no users in rankings, display error message and stop code
        if not rankings:
            label = customtkinter.CTkLabel(self.list_frame, text="No users to display.", font=("Bahnschrift", 14), text_color="#2B2B2B")
            label.pack(pady=20)
            return

        #Visual elements for Leaderboard
        headerformat = f"{'Rank':<6}{'Username':<20}{'Balance':<18}{'Growth'}"
        header = customtkinter.CTkLabel(self.list_frame, text=headerformat, font=("Bahnschrift", 14, "bold"), text_color="#06402B")
        header.pack(anchor="w", padx=20, pady=(10, 4))

        #A for loop to display every ranking, checking every condition for right output
        for i, entry in enumerate(rankings, start=1):
            balanceformat = f"${entry['total']:,.2f}"
            sign = "+" if entry["growth"] >= 0 else ""
            growthformat = f"{sign}{entry['growth']:.2f}%"

            rowformat = f"{str(i) + '.':<6}{entry['username']:<20}{balanceformat:<18}{growthformat}"
            row = customtkinter.CTkLabel(self.list_frame, text=rowformat, font=("Bahnschrift", 16), text_color="#2B2B2B")
            row.pack(anchor="w", padx=20, pady=8)

    # A button to return back to main menu, destroying widgets
    def returnback(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.controller.operate_menu()

    # Creates the leaderboard GUI, comparing balance and growth of different users
    def menuGui(self):
        main_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=900, height=750)
        main_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_propagate(False)

        self.title = customtkinter.CTkLabel(main_frame, text="Leaderboard", font=("Bahnschrift", 30), text_color="#06402B")
        self.title.grid(row=0, column=0, padx=20, pady=(30, 10), sticky="w")

        self.list_frame = customtkinter.CTkFrame(main_frame, fg_color="#F7E7CE")
        self.list_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_rowconfigure(1, weight=1)

        self.listrefresh()

        returnback_button = customtkinter.CTkButton(self.app, text="Back to Main Menu", fg_color="#06402B", width=900, height=30, command=self.returnback)
        returnback_button.place(x=20, y=735)