import hashlib
import sqlite3
from Crypto.Util import number
import asyncio
from datetime import datetime

class Server:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 55555
        self.prime = number.getPrime(256)
        self.base = 2
        self.connected_clients = []

    async def start(self):
        print("Server started")
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        try:
            self.connected_clients.append(writer)
            server_private_key = number.getRandomRange(1, self.prime - 1)
            server_public_key = pow(self.base, server_private_key, self.prime)

            writer.write(str(self.prime).encode() + b'\n')
            writer.write(str(self.base).encode() + b'\n')
            writer.write(str(server_public_key).encode() + b'\n')
            await writer.drain()

            data = await reader.readline()
            client_public_key = int(data.decode().strip())

            shared_key = pow(client_public_key, server_private_key, self.prime)
            print(f"Shared key: {shared_key}")

            await self.handle_main(reader, writer)
        except:
            print(f"Client {writer.get_extra_info('peername')} disconnected")
        finally:
            self.connected_clients.remove(writer)
            writer.close()
            try: 
                await writer.wait_closed() 
            except ConnectionResetError: 
                print("Client forcibly closed the connection")

    async def handle_main(self, reader, writer):
        try:
            while True:
                choice = await reader.readline()
                choice = choice.decode().strip()

                writer.write("Received Choice\n".encode())
                await writer.drain()

                if choice == "LOGIN":
                    await self.login(reader, writer)
                elif choice == "REGISTER":
                    await self.register(reader, writer)
                elif choice == "FETCH_FOOD_DATA":
                    await self.fetch_food_data(reader, writer)
                elif choice == "FETCH_CLIENT_DATA":
                    await self.fetch_client_data(reader, writer)
                elif choice == "ADD":
                    await self.add_food_item(reader, writer)
                elif choice == "HEARTBEAT":
                    print("in heartbeat choice")
                    await self.handle_heartbeat(reader, writer)
                else:
                    print("Invalid choice. Connection closing.")
                    break
        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            addr = writer.get_extra_info('peername')
            print(f"Disconnected: {addr}")
            writer.close()
            await writer.wait_closed()

    async def handle_heartbeat(self, reader, writer):
        try:
            heartbeat = (await reader.readline()).decode().strip()
            print(f"Heartbeat from {writer.get_extra_info('peername')}")
        except:
            pass
    async def login(self, reader, writer):
        try:
            username = await reader.readline()
            password = await reader.readline()
            username = username.decode().strip()
            password = password.decode().strip()

            password = hashlib.sha256(password.encode()).hexdigest()
            print(f"Login Attempt From: {username}")

            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM userdata WHERE username_client = ? AND password = ?", (username, password))

            if cur.fetchone():
                if username == "admin":
                    writer.write("Admin Login Successful!\n".encode())
                    print("Admin Login Successful!")
                else:
                    writer.write("Login Successful!\n".encode())
                    print("Login Successful!")
            else:
                writer.write("Login Failed!\n".encode())
                print("Login Failed!")
            conn.close()
        except Exception as e:
            print(f"An error occurred during login: {e}")

    async def register(self, reader, writer):
        try:
            username = await reader.readline()
            password = await reader.readline()
            username = username.decode().strip()
            password = password.decode().strip()

            password = hashlib.sha256(password.encode()).hexdigest()
            print(f"Register Attempt From: {username}")

            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("SELECT username_client FROM userdata WHERE username_client = ?", (username,))
            if cur.fetchone():
                writer.write("Account already registered!\n".encode())
                print("Account already registered!")
            else:
                cur.execute("INSERT INTO userdata (username_client, password) VALUES (?, ?)", (username, password))
                conn.commit()
                writer.write("Register successful!\n".encode())
                print("Register successful!")
            conn.close()
        except Exception as e:
            print(f"An error occurred during registration: {e}")

    async def fetch_food_data(self, reader, writer):
        try:
            username = (await reader.readline()).decode().strip()

            now = datetime.now() 
            current_date = now.strftime("%d-%m-%Y")

            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("SELECT date, food_item, calories FROM calorie_data WHERE username = ? AND date = ?", (username, current_date))
            data = cur.fetchall()
            conn.close()
            print(data)
            writer.write(f"{data}\n".encode())
            await writer.drain()
        except Exception as e:
            print(f"An error occurred while fetching food data: {e}")

    async def add_food_item(self, reader, writer):
        try:
            food = (await reader.readline()).decode().strip()
            calories = (await reader.readline()).decode().strip()
            username = (await reader.readline()).decode().strip()

            print(f"Food: {food}, Calories: {calories}, Username: {username}")
            now = datetime.now() 
            current_date = now.strftime("%d-%m-%Y")
            print(f"{current_date}")
            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO calorie_data (username, date, food_item, calories) VALUES (?, ?, ?, ?)", (username, current_date, food, calories))
            conn.commit()
            conn.close()
            writer.write("Food item added!\n".encode())
            await writer.drain()
        except Exception as e:
            print(f"An error occurred while adding food item: {e}")

    async def fetch_client_data(self, reader, writer):
        try:
            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("SELECT username_client FROM userdata")

            username_data = cur.fetchall()
            conn.close()
            print(username_data)

            writer.write(f"{username_data}\n".encode())
            await writer.drain()
        except Exception as e:
            print(f"An error occurred while fetching client data: {e}")

server = Server()
asyncio.run(server.start())
