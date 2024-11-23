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


#implement login logic here 
def login():
    username = username_field.get()
    password = password_field.get()

    client.send(username.encode())
    client.send(password.encode())
    
    message = client.recv(1024).decode()
    print(message)

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=2, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Login System")
label.pack(pady=12, padx=10)

username_field = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
username_field.pack(pady=12, padx=10)

password_field = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
password_field.pack(pady=12, padx=10)

confirm_button = customtkinter.CTkButton(master=frame, text="Login", command=login)
confirm_button.pack(pady=12, padx=10)

#----------------------------------------------------------------

# print(client.recv(1024).decode())

root.mainloop()