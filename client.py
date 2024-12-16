import socket
import customtkinter as ctk

class LogInClient(ctk.CTk):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))


    def login(self, choice):
        username = widgets.username_field_login.get()
        password = widgets.password_field_login.get()
        print(username)
        print(password)


        if username == "" or password == "":
            widgets.login_chat_box.configure(state='normal')  # Enable the text box
            widgets.login_chat_box.delete("1.0", "end")  # Clear the chat box
            widgets.login_chat_box.insert("1.0", "No username or password provided")
            widgets.login_chat_box.configure(state='disabled')  # Disable the text box again
            print("No username or password provided")
            return
        else:
            self.client.send(choice.encode())
            message = self.client.recv(1024).decode() 
            print(message)
        
            self.client.send(username.encode())
            self.client.send(password.encode())
            message = self.client.recv(1024).decode()
            print(message)

            widgets.login_chat_box.configure(state='normal')  # Enable the text box
            widgets.login_chat_box.delete("1.0", "end")  # Clear the chat box
            widgets.login_chat_box.insert("1.0", message)
            widgets.login_chat_box.configure(state='disabled')  # Disable the text box again

            if message == "Login Successful!":
                widgets.show_frame(widgets.tracker_frame)


    def register(self, choice):
        username = widgets.username_field_register.get()
        password = widgets.password_field_register.get()

        if username == "" or password == "":
            widgets.register_chat_box.configure(state='normal')  # Enable the text box
            widgets.login_chat_box.delete("1.0", "end")  # Clear the chat box
            widgets.register_chat_box.insert("1.0", "No username or password provided")
            widgets.register_chat_box.configure(state='disabled')  # Disable the text box again
            print("No username or password provided")
            return
        else:
            self.client.send(choice.encode())
            message = self.client.recv(1024).decode()
            print(message)

            self.client.send(username.encode())
            self.client.send(password.encode())
            message = self.client.recv(1024).decode()
            widgets.register_chat_box.configure(state='normal')  # Enable the text box
            widgets.register_chat_box.delete("1.0", "end")  # Clear the chat box
            widgets.register_chat_box.insert("1.0", message)
            widgets.register_chat_box.configure(state='disabled')  # Disable the text box again


class Widgets(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        

    def setup_ui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.geometry("600x400")
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.login_frame = ctk.CTkFrame(self.container)
        self.register_frame = ctk.CTkFrame(self.container)
        self.tracker_frame = ctk.CTkFrame(self.container)

        for frame in (self.login_frame, self.register_frame, self.tracker_frame):
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_widgets()


    def show_frame(self, frame):
        frame.tkraise()


    def create_widgets(self):

        # Login frame

        login_label = ctk.CTkLabel(self.login_frame, text="Login Screen")
        login_label.pack(pady=12, padx=10)

        self.username_field_login = ctk.CTkEntry(self.login_frame, placeholder_text="Username")
        self.username_field_login.pack(pady=12, padx=10)

        self.password_field_login = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_field_login.pack(pady=12, padx=10)

        login_confirm_button = ctk.CTkButton(self.login_frame, text="Login", command=lambda: app.login("LOGIN"))
        login_confirm_button.pack(pady=12, padx=10)

        login_button = ctk.CTkButton(self.login_frame, text="Go to Register", command=lambda: self.show_frame(self.register_frame))
        login_button.pack(pady=12, padx=10)

        self.login_chat_box = ctk.CTkTextbox(self.login_frame, width=150, height=50)
        self.login_chat_box.pack(pady=12, padx=10)
        self.login_chat_box.configure(state='disabled')

        # Register frame


        register_label = ctk.CTkLabel(self.register_frame, text="Register Screen")
        register_label.pack(pady=12, padx=10)

        self.username_field_register = ctk.CTkEntry(self.register_frame, placeholder_text="Username")
        self.username_field_register.pack(pady=12, padx=10)

        self.password_field_register = ctk.CTkEntry(self.register_frame, placeholder_text="Password", show="*")
        self.password_field_register.pack(pady=12, padx=10)

        register_confirm_button = ctk.CTkButton(self.register_frame, text="Register", command=lambda: app.register("REGISTER"))
        register_confirm_button.pack(pady=12, padx=10)

        register_button = ctk.CTkButton(self.register_frame, text="Go to Login", command=lambda: self.show_frame(self.login_frame))
        register_button.pack(pady=12, padx=10)

        self.register_chat_box = ctk.CTkTextbox(self.register_frame, width=150, height=50)
        self.register_chat_box.pack(pady=12, padx=10)
        self.register_chat_box.configure(state='disabled')

        # Tracker frame

        tracker_label = ctk.CTkLabel(self.tracker_frame, text="Calorie Tracker") 
        tracker_label.pack(pady=12, padx=10)

        self.view_box = ctk.CTkTextbox(self.tracker_frame, width=400, height=200) 
        self.view_box.pack(pady=12, padx=10) 
        self.view_box.configure(state='disabled')

        add_button = ctk.CTkButton(self.tracker_frame, text="Add Food Item", command=self.add_food_items) 
        add_button.pack(pady=12, padx=10)

        view_button = ctk.CTkButton(self.tracker_frame, text="View Food Items", command=self.view_food_items) 
        view_button.pack(pady=12, padx=10)

        entry_field = ctk.CTkEntry(self.tracker_frame, placeholder_text="Message here") 
        entry_field.pack(pady=12, padx=10)

        self.login_frame.tkraise()


    def add_food_items(self):
        add_window = ctk.CTkToplevel(self) 
        add_window.title("Add Food Item") 
        add_window.geometry("300x200") 
        ctk.CTkLabel(add_window, text="Food Item").pack(pady=5) 
        food_entry = ctk.CTkEntry(add_window) 
        food_entry.pack(pady=5) 
        ctk.CTkLabel(add_window, text="Calories").pack(pady=5) 
        calories_entry = ctk.CTkEntry(add_window) 
        calories_entry.pack(pady=5) 
        ctk.CTkButton(add_window, text="Add", command=lambda: self.save_food_item(food_entry.get(), calories_entry.get(), add_window)).pack(pady=20)

    def view_food_items():
        pass

if __name__ == "__main__":
    app = LogInClient("127.0.0.1", 55555)
    widgets = Widgets()
    widgets.mainloop()
