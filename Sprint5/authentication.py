#This is the main addition in sprint 5 the authentication system
#The authentication systems acts as a security barrier, creating different user profiles to save data and continuosly grow investments
#Imports customtkinter for GUI
#Imporst hashlib for encryption
#Imports uuid to store user_data
#Imports cod, index saving and stocks to connect to user profiles
#Imports functions from userdata, important for data management and user manipulation
import customtkinter
import hashlib
import uuid
import saving
import cod
import index
import stock
from userdata import load_users, save_users

# A class for the authentication system, containing all authentication variables and connected to main.py
class AuthenticationSystem:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.authenticationgui()

    #A function to encyrpt password for user
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # A function for registering, user inputs username and password
    def handle_register(self):
        username = self.user_entry.get().strip()
        password = self.password_entry.get().strip()

        #If there is no username or nor password in the entries, an error message pops up
        if not username or not password:
            self.status.configure(text="The Inputs cannot be empty", text_color="red")
            return

        #Load the users for json to check if they exists
        users = load_users()
        if any(u["username"] == username for u in users.values()):
            self.status.configure(text="User already exists!", text_color="red")
            return

        #When creating user id's, each user has a json data storage, it is formated like this
        #The user data is saved into on json file
        user_id = str(uuid.uuid4())
        users[user_id] = {
                        "username": username,
                        "password": self.hash_password(password),
                        "mainportfolio": 500.0,
                        "balances": {
                            "total": 500.0,
                            "hysa": 0.0,
                            "cod": 0.0,
                            "indexfund": 0.0,
                            "stocks": 0.0
                        },
                        "savings_portfolio": [],
                        "cod_portfolio": [],
                        "indexfund_portfolio": [],
                        "stockmarket_portfolio": [],
                        "history": []
                    }
        save_users(users)
        #Prints registration successful if user registers successfully
        self.status.configure(text="Registration Successful!", text_color="green")
    
    #A function for loggining to smartinvestment, user inputs password and username
    #Password immediately becomes hashed
    def handle_login(self):
        username = self.user_entry.get().strip()
        password = self.password_entry.get().strip()
        hashed = self.hash_password(password)

        #Loads users and creates variables for user, sets up the whole maininvestment program if login sucessful
        users = load_users()
        for user_id, data in users.items():
            if data["username"] == username and data["password"] == hashed:
                self.controller.users_data = users
                self.controller.current_user_token = user_id
                self.controller.current_user = username
                self.controller.mainportfolio = data.get("mainportfolio", 500.0)
                self.resetportfolios()
                self.constructportfolios(data)   
                self.controller.operate_menu()
                return

        #If login fails
        self.status.configure(text="Invalid Username or Password", text_color="red")

    # A function to reset portfolios, creating new investment oppurtunities portfolios
    def resetportfolios(self):
        self.controller.savings_portfolio = []
        self.controller.cod_portfolio = []
        self.controller.indexfund_portfolio = []
        self.controller.stockmarket_portfolio = []

    # A function to construct portfolios, constantly rebuilds investment oppurtunity portfolios
    def constructportfolios(self, data):
        self.controller.savings_portfolio = [saving.Investment("Savings",item["amount"],item.get("rate", 0.05))for item in data.get("savings_portfolio", [])]
        self.controller.cod_portfolio = []
        for item in data.get("cod_portfolio", []):
            inv = cod.Investment(item["name"],item["amount"],item["years"])
            inv.compounded = item.get("compounded", False)
            self.controller.cod_portfolio.append(inv)
        self.controller.indexfund_portfolio = [index.Investment(item["symbol"],item["shares"])for item in data.get("indexfund_portfolio", [])]
        self.controller.stockmarket_portfolio = [stock.Investment(item["symbol"],item["shares"],0)for item in data.get("stockmarket_portfolio", [])]

    # Creates the Authentication GUI, this will be the first GUI interface you will view, constructs labels, buttons and entrys
    # The only GUI that uses pack because my project before this used .pack
    def authenticationgui(self):
        
        title = customtkinter.CTkLabel(self.app, text="SmartInvestments Login",text_color="#06402B", font=("Bahnschrift", 60))
        title.pack(pady=20)

        customtkinter.CTkLabel(self.app, font=("Bahnschrift", 20), text="Enter Username").pack(pady=5)
        self.user_entry = customtkinter.CTkEntry(self.app, width=300)
        self.user_entry.pack(pady=10)
        customtkinter.CTkLabel(self.app, font=("Bahnschrift", 20), text="Enter Password").pack(pady=5)
        self.password_entry = customtkinter.CTkEntry(self.app, width=300, show="*")
        self.password_entry.pack(pady=10)
        btn = customtkinter.CTkFrame(self.app, fg_color="transparent")
        btn.pack(pady=10)

        customtkinter.CTkButton(btn, text="Login", fg_color="#06402B", command=self.handle_login).pack(side="left", padx=5)
        customtkinter.CTkButton(btn, text="Register", fg_color="#06402B", command=self.handle_register).pack(side="left", padx=5)
        self.status = customtkinter.CTkLabel(self.app, text="")
        self.status.pack(pady=10)