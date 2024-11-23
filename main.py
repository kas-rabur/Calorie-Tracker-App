import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry("500x300")

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# Main container
container = ctk.CTkFrame(root)
container.pack(fill="both", expand=True)

# Configure grid for the container
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Frames
login_frame = ctk.CTkFrame(container)
register_frame = ctk.CTkFrame(container)

for frame in (login_frame, register_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# Login Frame
login_label = ctk.CTkLabel(login_frame, text="Login Screen")
login_label.pack(pady=12, padx=10)

login_button = ctk.CTkButton(login_frame, text="Go to Register", command=lambda: show_frame(register_frame))
login_button.pack(pady=12, padx=10)

username_field = ctk.CTkEntry(login_frame, placeholder_text="Username")
username_field.pack(pady=12, padx=10)

password_field = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*")
password_field.pack(pady=12, padx=10)

login_confirm_button = ctk.CTkButton(login_frame, text="Login")
login_confirm_button.pack(pady=12, padx=10)

# Register Frame
register_label = ctk.CTkLabel(register_frame, text="Register Screen")
register_label.pack(pady=12, padx=10)

register_button = ctk.CTkButton(register_frame, text="Go to Login", command=lambda: show_frame(login_frame))
register_button.pack(pady=12, padx=10)

register_username_field = ctk.CTkEntry(register_frame, placeholder_text="Username")
register_username_field.pack(pady=12, padx=10)

register_password_field = ctk.CTkEntry(register_frame, placeholder_text="Password", show="*")
register_password_field.pack(pady=12, padx=10)

register_confirm_button = ctk.CTkButton(register_frame, text="Register")
register_confirm_button.pack(pady=12, padx=10)

# Show the login frame first
show_frame(login_frame)

root.mainloop()
