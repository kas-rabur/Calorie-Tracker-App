import socket
import customtkinter as ctk

class LogInClient(ctk.CTk):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.setup_ui()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

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
        self.chat_frame = ctk.CTkFrame(self.container)

        for frame in (self.login_frame, self.register_frame, self.chat_frame):
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_widgets()

    def show_frame(self, frame):
        frame.tkraise()

    def login(self, choice):
        username = self.username_field_login.get()
        password = self.password_field_login.get()

        if username == "" or password == "":
            self.login_chat_box.configure(state='normal')  # Enable the text box
            self.login_chat_box.delete("1.0", "end")  # Clear the chat box
            self.login_chat_box.insert("1.0", "No username or password provided")
            self.login_chat_box.configure(state='disabled')  # Disable the text box again
            print("No username or password provided")
            return
        else:
            self.client.send(choice.encode())
            message = self.client.recv(1024).decode() 
            print(message)
        
            self.client.send(username.encode())
            self.client.send(password.encode())
            message = self.client.recv(1024).decode()
            self.login_chat_box.configure(state='normal')  # Enable the text box
            self.login_chat_box.delete("1.0", "end")  # Clear the chat box
            self.login_chat_box.insert("1.0", message)
            self.login_chat_box.configure(state='disabled')  # Disable the text box again

            if message == "Login Successful!":
                self.show_frame(self.chat_frame)



    def register(self, choice):
        username = self.username_field_register.get()
        password = self.password_field_register.get()

        if username == "" or password == "":
            self.register_chat_box.configure(state='normal')  # Enable the text box
            self.login_chat_box.delete("1.0", "end")  # Clear the chat box
            self.register_chat_box.insert("1.0", "No username or password provided")
            self.register_chat_box.configure(state='disabled')  # Disable the text box again
            print("No username or password provided")
            return
        else:
            self.client.send(choice.encode())
            message = self.client.recv(1024).decode()
            print(message)

            self.client.send(username.encode())
            self.client.send(password.encode())
            message = self.client.recv(1024).decode()
            self.register_chat_box.configure(state='normal')  # Enable the text box
            self.register_chat_box.delete("1.0", "end")  # Clear the chat box
            self.register_chat_box.insert("1.0", message)
            self.register_chat_box.configure(state='disabled')  # Disable the text box again

    def create_widgets(self):

        # Login frame

        login_label = ctk.CTkLabel(self.login_frame, text="Login Screen")
        login_label.pack(pady=12, padx=10)

        self.username_field_login = ctk.CTkEntry(self.login_frame, placeholder_text="Username")
        self.username_field_login.pack(pady=12, padx=10)

        self.password_field_login = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_field_login.pack(pady=12, padx=10)

        login_confirm_button = ctk.CTkButton(self.login_frame, text="Login", command=lambda: self.login("LOGIN"))
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

        register_confirm_button = ctk.CTkButton(self.register_frame, text="Register", command=lambda: self.register("REGISTER"))
        register_confirm_button.pack(pady=12, padx=10)

        register_button = ctk.CTkButton(self.register_frame, text="Go to Login", command=lambda: self.show_frame(self.login_frame))
        register_button.pack(pady=12, padx=10)

        self.register_chat_box = ctk.CTkTextbox(self.register_frame, width=150, height=50)
        self.register_chat_box.pack(pady=12, padx=10)
        self.register_chat_box.configure(state='disabled')

        # Chat frame

        chat_label = ctk.CTkLabel(self.chat_frame, text="Chat")
        chat_label.pack(pady=12, padx=10)

        chat_box = ctk.CTkTextbox(self.chat_frame, width=400, height=350)
        chat_box.pack(pady=12, padx=10)
        chat_box.configure(state='disabled')

        chat_field = ctk.CTkEntry(self.chat_frame, placeholder_text="Message here")
        chat_field.pack(pady=12, padx=10)

        chat_send_button = ctk.CTkButton(self.chat_frame, text="Send")
        chat_send_button.pack(pady=12, padx=10)

        self.login_frame.tkraise()

if __name__ == "__main__":
    app = LogInClient("127.0.0.1", 55555)
    app.mainloop()
