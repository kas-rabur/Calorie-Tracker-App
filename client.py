import socket
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
root = customtkinter.CTk()
root.geometry("500x300")

host = "127.0.0.1"
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def show_frame(frame):
    frame.tkraise()

def login():
    print("in login")
    username1 = username_field_login.get()
    password1 = password_field_login.get()
    print(f"username and password{username1}, {password1}")
    client.send(username1.encode())
    client.send(password1.encode())
    message1 = client.recv(1024).decode()
    print(f"Login Response: {message1}")

def register():
    username = username_field_register.get()
    password = password_field_register.get()
    client.send(username.encode())
    client.send(password.encode())
    message = client.recv(1024).decode()
    print(f"Register Response: {message}")

def choiceHandle(choice):
    client.send(choice.encode())
    message = client.recv(1024).decode()
    print(f"Choice Response: {message}")

    if choice == "LOGIN":
        login()
    elif choice == "REGISTER":
        register()

container = customtkinter.CTkFrame(root)
container.pack(fill="both", expand=True)

container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

login_frame = customtkinter.CTkFrame(container)
register_frame = customtkinter.CTkFrame(container)

for frame in (login_frame, register_frame):
    frame.grid(row=0, column=1, sticky="nsew")

login_label = customtkinter.CTkLabel(login_frame, text="Login Screen")
login_label.pack(pady=12, padx=10)

login_button = customtkinter.CTkButton(login_frame, text="Go to Register", command=lambda: show_frame(register_frame))
login_button.pack(pady=12, padx=10)

username_field_login = customtkinter.CTkEntry(login_frame, placeholder_text="Username")
username_field_login.pack(pady=12, padx=10)

password_field_login = customtkinter.CTkEntry(login_frame, placeholder_text="Password", show="*")
password_field_login.pack(pady=12, padx=10)

login_confirm_button = customtkinter.CTkButton(login_frame, text="Login", command=lambda: choiceHandle("LOGIN"))
login_confirm_button.pack(pady=12, padx=10)



register_label = customtkinter.CTkLabel(register_frame, text="Register Screen")
register_label.pack(pady=12, padx=10)

register_button = customtkinter.CTkButton(register_frame, text="Go to Login", command=lambda: show_frame(login_frame))
register_button.pack(pady=12, padx=10)

username_field_register = customtkinter.CTkEntry(register_frame, placeholder_text="Username")
username_field_register.pack(pady=12, padx=10)

password_field_register = customtkinter.CTkEntry(register_frame, placeholder_text="Password", show="*")
password_field_register.pack(pady=12, padx=10)

register_confirm_button = customtkinter.CTkButton(register_frame, text="Register", command=lambda: choiceHandle("REGISTER"))
register_confirm_button.pack(pady=12, padx=10)

root.mainloop()
