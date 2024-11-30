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
        self.attributes('-fullscreen', True)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.login_frame = ctk.CTkFrame(self.container)
        self.register_frame = ctk.CTkFrame(self.container)
        self.chat_frame = ctk.CTkFrame(self.container)

        for frame in (self.login_frame, self.register_frame, self.chat_frame):
            frame.grid(row=0, column=1, sticky="nsew")

        self.create_widgets()

    def show_frame(self, frame):
        frame.tkraise()

    def login(self):
        username = self.username_field_login.get()
        password = self.password_field_login.get()
        self.client.send(username.encode())
        self.client.send(password.encode())
        message = self.client.recv(1024).decode()
        print(message)

    def register(self):
        username = self.username_field_register.get()
        password = self.password_field_register.get()
        self.client.send(username.encode())
        self.client.send(password.encode())
        message = self.client.recv(1024).decode()
        print(message)

    def choice_handle(self, choice):

        if choice == "LOGIN":
            self.client.send(choice.encode())
            message = self.client.recv(1024).decode() 
            print(message)
            self.login()        
           
        elif choice == "REGISTER":
            self.client.send(choice.encode())
            message = self.client.recv(1024).decode()
            print(message)
            self.register()
        else:
            self.client.send("EMPTY".encode()) 
            message = self.client.recv(1024).decode()
            print(message)

    def create_widgets(self):

        # Login frame

        login_label = ctk.CTkLabel(self.login_frame, text="Login Screen")
        login_label.pack(pady=12, padx=10)

        self.username_field_login = ctk.CTkEntry(self.login_frame, placeholder_text="Username")
        self.username_field_login.pack(pady=12, padx=10)

        self.password_field_login = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_field_login.pack(pady=12, padx=10)

        login_confirm_button = ctk.CTkButton(self.login_frame, text="Login", command=lambda: self.choice_handle("LOGIN"))
        login_confirm_button.pack(pady=12, padx=10)

        login_button = ctk.CTkButton(self.login_frame, text="Go to Register", command=lambda: self.show_frame(self.register_frame))
        login_button.pack(pady=12, padx=10)

        test_confirm_button = ctk.CTkButton(self.login_frame, text="SWITCH FRAME", command=lambda: self.show_frame(self.chat_frame))
        test_confirm_button.pack(pady=12, padx=10)

        login_chat_box = ctk.CTkTextbox(self.login_frame, width=100, height=50)
        login_chat_box.pack(pady=12, padx=10)
        login_chat_box.configure(state='disabled')

        # Register frame


        register_label = ctk.CTkLabel(self.register_frame, text="Register Screen")
        register_label.pack(pady=12, padx=10)

        self.username_field_register = ctk.CTkEntry(self.register_frame, placeholder_text="Username")
        self.username_field_register.pack(pady=12, padx=10)

        self.password_field_register = ctk.CTkEntry(self.register_frame, placeholder_text="Password", show="*")
        self.password_field_register.pack(pady=12, padx=10)

        register_confirm_button = ctk.CTkButton(self.register_frame, text="Register", command=lambda: self.choice_handle("REGISTER"))
        register_confirm_button.pack(pady=12, padx=10)

        register_button = ctk.CTkButton(self.register_frame, text="Go to Login", command=lambda: self.show_frame(self.login_frame))
        register_button.pack(pady=12, padx=10)

        register_chat_box = ctk.CTkTextbox(self.register_frame, width=100, height=50)
        register_chat_box.pack(pady=12, padx=10)
        register_chat_box.configure(state='disabled')

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
