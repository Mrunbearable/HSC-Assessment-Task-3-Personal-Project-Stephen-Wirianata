import customtkinter
import hashlib
import uuid
import saving
import cod
import index
import stock
from userdata import load_users, save_users

class AuthenticationSystem:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.authenticationgui()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def handle_register(self):
        username = self.user_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.status.configure(text="The Inputs cannot be empty", text_color="red")
            return

        users = load_users()
        if any(u["username"] == username for u in users.values()):
            self.status.configure(text="User already exists!", text_color="red")
            return

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
        self.status.configure(text="Registration Successful!", text_color="green")

    def handle_login(self):
        username = self.user_entry.get().strip()
        password = self.password_entry.get().strip()
        hashed = self.hash_password(password)

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

        self.status.configure(text="Invalid Username or Password", text_color="red")

    def resetportfolios(self):
        self.controller.savings_portfolio = []
        self.controller.cod_portfolio = []
        self.controller.indexfund_portfolio = []
        self.controller.stockmarket_portfolio = []

    def constructportfolios(self, data):
        self.controller.savings_portfolio = [saving.Investment("Savings",item["amount"],item.get("rate", 0.05))for item in data.get("savings_portfolio", [])]
        self.controller.cod_portfolio = []
        for item in data.get("cod_portfolio", []):
            inv = cod.Investment(item["name"],item["amount"],item["years"])
            inv.compounded = item.get("compounded", False)
            self.controller.cod_portfolio.append(inv)
        self.controller.indexfund_portfolio = [index.Investment(item["symbol"],item["shares"])for item in data.get("indexfund_portfolio", [])]
        self.controller.stockmarket_portfolio = [stock.Investment(item["symbol"],item["shares"],0)for item in data.get("stockmarket_portfolio", [])]


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