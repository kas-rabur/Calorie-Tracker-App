from Crypto.Util import number
import customtkinter as ctk
import asyncio
import ssl

class LogInClient(ctk.CTk):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.client = None  # Initialize the client socket
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.connect())
        self.clients = {}
        self.total_calories = 2000
        self.calories_consumed = 0
        self.calories_left = self.total_calories - self.calories_consumed

    async def connect(self):
        # Create SSL context
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.load_verify_locations('server.crt')  # Load the server's certificate

        reader, writer = await asyncio.open_connection(self.host, self.port, ssl=ssl_context)
        self.client = (reader, writer)

        self.prime = int((await reader.readline()).decode('utf-8').strip())
        self.base = int((await reader.readline()).decode('utf-8').strip())
        self.server_public_key = int((await reader.readline()).decode('utf-8').strip())

        self.client_private_key = number.getRandomRange(1, self.prime - 1)
        self.client_public_key = pow(self.base, self.client_private_key, self.prime)

        writer.write(f"{self.client_public_key}\n".encode('utf-8'))
        await writer.drain()

        # Shared secret key
        self.shared_key = pow(self.server_public_key, self.client_private_key, self.prime)
        print(f"Shared key: {self.shared_key}")

    async def login(self, choice):
        reader, writer = self.client
        username = widgets.username_field_login.get()
        password = widgets.password_field_login.get()

        if username == "" or password == "":
            widgets.login_chat_box.configure(state='normal')
            widgets.login_chat_box.delete("1.0", "end")
            widgets.login_chat_box.insert("1.0", "No username or password provided")
            widgets.login_chat_box.configure(state='disabled')
            print("No username or password provided")
            return
        else:
            writer.write(f"{choice}\n".encode('utf-8'))
            await writer.drain()
            message = (await reader.readline()).decode('utf-8').strip()

            print(message)

            writer.write(f"{username}\n".encode('utf-8'))
            await writer.drain()
            writer.write(f"{password}\n".encode('utf-8'))
            await writer.drain()

            message = (await reader.readline()).decode('utf-8').strip()
            print(message)

            widgets.login_chat_box.configure(state='normal')
            widgets.login_chat_box.delete("1.0", "end")
            widgets.login_chat_box.insert("1.0", message)
            widgets.login_chat_box.configure(state='disabled')

            if message.startswith("Admin"):
                widgets.show_frame(widgets.admin_frame)
                
            elif message == "Login Successful!":
                self.clients[(reader, writer)] = username
                widgets.show_frame(widgets.tracker_frame)

    async def register(self, choice):
        reader, writer = self.client
        username = widgets.username_field_register.get()
        password = widgets.password_field_register.get()

        if username == "" or password == "":
            widgets.register_chat_box.configure(state='normal')
            widgets.register_chat_box.delete("1.0", "end")
            widgets.register_chat_box.insert("1.0", "No username or password provided")
            widgets.register_chat_box.configure(state='disabled')
            print("No username or password provided")
            return
        else:
            writer.write(f"{choice}\n".encode('utf-8'))
            await writer.drain()
            message = (await reader.readline()).decode('utf-8').strip()

            print(message)

            writer.write(f"{username}\n".encode('utf-8'))
            await writer.drain()
            writer.write(f"{password}\n".encode('utf-8'))
            await writer.drain()

            message = (await reader.readline()).decode('utf-8').strip()
            print(message)

            widgets.register_chat_box.configure(state='normal')
            widgets.register_chat_box.delete("1.0", "end")
            widgets.register_chat_box.insert("1.0", message)
            widgets.register_chat_box.configure(state='disabled')

    async def fetch_food_data(self, choice):
        reader, writer = self.client
        username = self.clients[(reader, writer)]
        print(f"username: {username}")
        calories_now = 0

        writer.write(f"{choice}\n".encode('utf-8'))
        await writer.drain()
        message = (await reader.readline()).decode('utf-8').strip()
        print(message)

        writer.write(f"{username}\n".encode('utf-8'))
        await writer.drain()

        data = (await reader.readline()).decode('utf-8').strip()
        print(data)

        data_new = data[1:-1].split("), (")
        new_data = ""
        for entry in data_new:
            entry = entry.replace("(", "").replace(")", "").replace("'", "").split(", ")
            date, name, calories = entry
            new_data += (f"{name}: {calories}\n")
            calories_now += int(calories)

        self.calories_consumed = calories_now

        widgets.view_box.configure(state='normal') 
        widgets.view_box.delete("1.0", "end") 
        widgets.view_box.insert("1.0", new_data) 
        widgets.view_box.configure(state='disabled')

        widgets.totals_consumed.configure(text=f"Total Consumed: {self.calories_consumed}")
        widgets.calories_left_label.configure(text=f"Calories left: {self.total_calories - self.calories_consumed}")

    async def fetch_client_data(self, choice):
        reader, writer = self.client
        writer.write(f"{choice}\n".encode('utf-8'))
        await writer.drain()

        message = (await reader.readline()).decode('utf-8').strip()
        print(message)  

        client_data = (await reader.readline()).decode('utf-8').strip()
        print(client_data)

        widgets.admin_view_box.configure(state='normal') 
        widgets.admin_view_box.delete("1.0", "end") 
        widgets.admin_view_box.insert("1.0", client_data) 
        widgets.admin_view_box.configure(state='disabled')

    async def add_food_item(self, choice):
        reader, writer = self.client
        food_item = widgets.food_item_name.get()
        calories = widgets.calories_in_food.get()
        username = self.clients[(reader, writer)]

        writer.write(f"{choice}\n".encode('utf-8'))
        await writer.drain()
        message = (await reader.readline()).decode('utf-8').strip()

        print(message)

        writer.write(f"{food_item}\n".encode('utf-8'))
        writer.write(f"{calories}\n".encode('utf-8'))
        writer.write(f"{username}\n".encode('utf-8'))

        await writer.drain()

        message = (await reader.readline()).decode('utf-8').strip()
        print(message)
        widgets.show_frame(widgets.tracker_frame)

class Widgets(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.setup_ui()
 

    def setup_ui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.geometry("800x600")
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.login_frame = ctk.CTkFrame(self.container)
        self.register_frame = ctk.CTkFrame(self.container)
        self.tracker_frame = ctk.CTkFrame(self.container)
        self.food_frame = ctk.CTkFrame(self.container)
        self.admin_frame = ctk.CTkFrame(self.container)


        for frame in (self.login_frame, self.register_frame, self.tracker_frame, self.food_frame, self.admin_frame):
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_widgets()


    def show_frame(self, frame):
        frame.tkraise()


    def create_widgets(self):

        # Login frame
        login_label_frame = ctk.CTkFrame(self.login_frame, width=700, height=40)
        login_label_frame.pack(fill='x')  
        login_label = ctk.CTkLabel(login_label_frame, text="Login")
        login_label.pack(pady=12, padx=10)
        self.username_field_login = ctk.CTkEntry(self.login_frame, placeholder_text="Username")
        self.username_field_login.pack(pady=12, padx=10)
        self.password_field_login = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_field_login.pack(pady=12, padx=10)
        login_confirm_button = ctk.CTkButton(self.login_frame, text="Login", command=lambda: app.loop.run_until_complete(app.login("LOGIN")))
        login_confirm_button.pack(pady=12, padx=10)
        login_button = ctk.CTkButton(self.login_frame, text="Go to Register", command=lambda: self.show_frame(self.register_frame))
        login_button.pack(pady=12, padx=10)
        self.login_chat_box = ctk.CTkTextbox(self.login_frame, width=150, height=50)
        self.login_chat_box.pack(pady=12, padx=10)
        self.login_chat_box.configure(state='disabled')

        # Register frame
        register_label_frame = ctk.CTkFrame(self.register_frame, width=700, height=40)
        register_label_frame.pack(fill='x')  
        register_label = ctk.CTkLabel(register_label_frame, text="Register")
        register_label.pack(pady=12, padx=10)
        self.username_field_register = ctk.CTkEntry(self.register_frame, placeholder_text="Username")
        self.username_field_register.pack(pady=12, padx=10)
        self.password_field_register = ctk.CTkEntry(self.register_frame, placeholder_text="Password", show="*")
        self.password_field_register.pack(pady=12, padx=10)
        register_confirm_button = ctk.CTkButton(self.register_frame, text="Register", command=lambda: app.loop.run_until_complete(app.register("REGISTER")))
        register_confirm_button.pack(pady=12, padx=10)
        register_button = ctk.CTkButton(self.register_frame, text="Go to Login", command=lambda: self.show_frame(self.login_frame))
        register_button.pack(pady=12, padx=10)
        self.register_chat_box = ctk.CTkTextbox(self.register_frame, width=150, height=50)
        self.register_chat_box.pack(pady=12, padx=10)
        self.register_chat_box.configure(state='disabled')

        # Tracker frame
        tracker_label_frame = ctk.CTkFrame(self.tracker_frame, width=700, height=40)
        tracker_label_frame.pack(fill='x')  
        tracker_label = ctk.CTkLabel(tracker_label_frame, text="Calorie Tracker", font=("Helvetica", 16, "bold"))
        tracker_label.pack(pady=12, padx=10)
        self.calories_left_label = ctk.CTkLabel(self.tracker_frame, text="Calories left: 2000")
        self.calories_left_label.pack(anchor='w', padx=10)
        self.totals_consumed = ctk.CTkLabel(self.tracker_frame, text="Total Consumed: ")
        self.totals_consumed.pack(anchor='w', padx=10)
        self.view_box = ctk.CTkTextbox(self.tracker_frame, width=700, height=200)
        self.view_box.pack(pady=12, padx=10)
        self.view_box.configure(state='disabled')
        add_button = ctk.CTkButton(self.tracker_frame, text="Add Food Item", font=("Helvetica", 12, "bold"), command=lambda: self.show_frame(self.food_frame))
        add_button.pack(pady=12, padx=10)
        view_button = ctk.CTkButton(self.tracker_frame, text="Update", font=("Helvetica", 12, "bold"), command=lambda: app.loop.run_until_complete(app.fetch_food_data("FETCH_FOOD_DATA")))
        view_button.pack(pady=12, padx=10)
        entry_field = ctk.CTkEntry(self.tracker_frame, placeholder_text="Message here")
        entry_field.pack(pady=12, padx=10)

        #add food frame
        food_label_frame = ctk.CTkFrame(self.food_frame, width=700, height=40)
        food_label_frame.pack(fill='x')  
        food_label = ctk.CTkLabel(self.food_frame, text="Add Food Item", font=("Helvetica", 16, "bold"))
        food_label.pack(pady=12, padx=10)        

        self.food_item_name = ctk.CTkEntry(self.food_frame, placeholder_text="Food Item")
        self.food_item_name.pack(pady=12, padx=10)
        self.calories_in_food = ctk.CTkEntry(self.food_frame, placeholder_text="Calories")
        self.calories_in_food.pack(pady=12, padx=10)

        add_food_button = ctk.CTkButton(self.food_frame, text="Add Item", command=lambda: app.loop.run_until_complete(app.add_food_item("ADD")))
        add_food_button.pack(pady=12, padx=10)
        return_button = ctk.CTkButton(self.food_frame, text="Return", command=lambda: self.show_frame(self.tracker_frame))
        return_button.pack(pady=12, padx=10)

        # Admin tracker frame
        admin_tracker_label_frame = ctk.CTkFrame(self.admin_frame, width=700, height=40)
        admin_tracker_label_frame.pack(fill='x')  
        admin_tracker_label = ctk.CTkLabel(admin_tracker_label_frame, text="Admin Interface", font=("Helvetica", 16, "bold"))
        admin_tracker_label.pack(pady=12, padx=10)

        self.admin_view_box = ctk.CTkTextbox(self.admin_frame, width=700, height=200)
        self.admin_view_box.pack(pady=12, padx=10)
        self.admin_view_box.configure(state='disabled')

        admin_view_button = ctk.CTkButton(self.admin_frame, text="View client list", font=("Helvetica", 12, "bold"), command=lambda: app.loop.run_until_complete(app.fetch_client_data("FETCH_CLIENT_DATA")))
        admin_view_button.pack(pady=12, padx=10)

        admin_add_client = ctk.CTkButton(self.admin_frame, text="View client list", font=("Helvetica", 12, "bold"))
        admin_add_client.pack(pady=12, padx=10)

        self.login_frame.tkraise()


if __name__ == "__main__":
    app = LogInClient("127.0.0.1", 55555)
    widgets = Widgets()
    widgets.mainloop()
