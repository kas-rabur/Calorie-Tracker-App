import socket
import hashlib
import sqlite3
from Crypto.Util import number
import asyncio

class Server:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 55555
        self.prime = number.getPrime(256)
        self.base = 2

    async def start(self):
        print("Server started")
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        try:
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

            await self.handle_login(reader, writer)
        except:
            print("Client disconnected...")
        finally:
            writer.close()
            await writer.wait_closed()

    async def handle_login(self, reader, writer):
        while True:
            try:
                choice = await reader.readline()
                choice = choice.decode().strip()

                writer.write("Received Choice\n".encode())
                await writer.drain()

                if choice == "LOGIN":
                    username = await reader.readline()
                    password = await reader.readline()
                    username = username.decode().strip()
                    password = password.decode().strip()

                    password = hashlib.sha256(password.encode()).hexdigest()
                    print(f"Login Attempt From: {username}")

                    conn = sqlite3.connect("userdata.db")
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

                    if cur.fetchone():
                        writer.write("Login Successful!\n".encode())
                        print("Login Successful!")
                        conn.close()
                        break
                    else:
                        writer.write("Login Failed!\n".encode())
                        print("Login Failed!")
                elif choice == "REGISTER":
                    username = await reader.readline()
                    password = await reader.readline()
                    username = username.decode().strip()
                    password = password.decode().strip()

                    password = hashlib.sha256(password.encode()).hexdigest()
                    print(f"Register Attempt From: {username}")

                    conn = sqlite3.connect("userdata.db")
                    cur = conn.cursor()
                    cur.execute("SELECT username FROM userdata WHERE username = ?", (username,))
                    if cur.fetchone():
                        writer.write("Account already registered!\n".encode())
                        print("Account already registered!")
                    else:
                        cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, password))
                        conn.commit()
                        writer.write("Register successful!\n".encode())
                        print("Register successful!")
                        conn.close()
                else:
                    print("Invalid choice. Connection closing.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            finally:
                addr = writer.get_extra_info('peername')
                print(f"Disconnected: {addr}")
                writer.close() 
                await writer.wait_closed()

    def fetch_food_data(self, username):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()
        cur.execute("SELECT date, food_item, calories FROM calorie_data WHERE username = ?", (username,))
        data = cur.fetchall()
        conn.close()
        print(data)
        return data

server = Server()
asyncio.run(server.start())
