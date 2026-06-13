import customtkinter

class InvestmentMenu:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app  

        self.menuGui()
            
    def menuGui(self):
        
        left_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=600, height=650)
        left_frame.grid(row=1, column=0, rowspan=2, padx=(20, 10), pady=20, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_propagate(False)

        right_frame = customtkinter.CTkFrame(self.app, fg_color="#D2C3A9", width=800, height=650)
        right_frame.grid(row=1, column=1, padx=(10, 20), pady=20, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_propagate(False)

        customtkinter.CTkLabel(self.app, font=("Bahnschrift", 45), text_color="#D2C3A9", text="Smart Investments").grid(row=0, column=0, padx=20, pady=5, sticky="w")

        