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

# Implement login logic here
def login():
    username = username_field.get()
    password = password_field.get()
    client.send(username.encode())
    client.send(password.encode())
    message = client.recv(1024).decode()
    print(message)

def register():
    username = username_field.get()
    password = password_field.get()
    client.send(username.encode())
    client.send(password.encode())
    message = client.recv(1024).decode()
    print(message)

def choiceHandle(choice):
    if choice == "LOGIN":
        client.send("LOGIN".encode())
        message = client.recv(1024).decode()
        print(message)

        login()
    elif choice == "REGISTER":
        client.send("REGISTER".encode())
        message = client.recv(1024).decode()
        print(message)
        register()

container = customtkinter.CTkFrame(root)
container.pack(fill="both", expand=True)

container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

login_frame = customtkinter.CTkFrame(container)
register_frame = customtkinter.CTkFrame(container)

for frame in (login_frame, register_frame):
    frame.grid(row=0, column=1, sticky="nsew")

# Login Frame
login_label = customtkinter.CTkLabel(login_frame, text="Login Screen")
login_label.pack(pady=12, padx=10)

login_button = customtkinter.CTkButton(login_frame, text="Go to Register", command=lambda: show_frame(register_frame))
login_button.pack(pady=12, padx=10)

username_field = customtkinter.CTkEntry(login_frame, placeholder_text="Username")
username_field.pack(pady=12, padx=10)

password_field = customtkinter.CTkEntry(login_frame, placeholder_text="Password", show="*")
password_field.pack(pady=12, padx=10)

login_confirm_button = customtkinter.CTkButton(login_frame, text="Login", command=lambda: choiceHandle("LOGIN"))
login_confirm_button.pack(pady=12, padx=10)

# Register Frame
register_label = customtkinter.CTkLabel(register_frame, text="Register Screen")
register_label.pack(pady=12, padx=10)

register_button = customtkinter.CTkButton(register_frame, text="Go to Login", command=lambda: show_frame(login_frame))
register_button.pack(pady=12, padx=10)

username_field = customtkinter.CTkEntry(register_frame, placeholder_text="Username")
username_field.pack(pady=12, padx=10)

password_field = customtkinter.CTkEntry(register_frame, placeholder_text="Password", show="*")
password_field.pack(pady=12, padx=10)

register_confirm_button = customtkinter.CTkButton(register_frame, text="Register", command=lambda: choiceHandle("REGISTER"))
register_confirm_button.pack(pady=12, padx=10)

root.mainloop()
