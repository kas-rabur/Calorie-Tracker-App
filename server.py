import hashlib
import sqlite3
import logging
from Crypto.Util import number
import asyncio
from datetime import datetime
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
import base64
import ssl

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Server:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 55555
        self.prime = number.getPrime(256)
        self.base = 2
        self.connected_clients = []
        self.login_attempts = 0

    async def start(self):
        logging.info("Server started")

        # Load SSL context
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

        server = await asyncio.start_server(self.handle_client, self.host, self.port, ssl=ssl_context)
        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        logging.info(f"New client connected: {addr}")
        try:
            self.connected_clients.append(writer)
            server_private_key = number.getRandomRange(1, self.prime - 1)
            server_public_key = pow(self.base, server_private_key, self.prime)

            writer.write(str(self.prime).encode('utf-8') + b'\n')
            writer.write(str(self.base).encode('utf-8') + b'\n')
            writer.write(str(server_public_key).encode('utf-8') + b'\n')
            await writer.drain() 

            data = await reader.readline()
            client_public_key = int(data.decode('utf-8').strip())

            shared_key = pow(client_public_key, server_private_key, self.prime)
            logging.info(f"Shared key established with {addr}: {shared_key}")

            await self.handle_main(reader, writer) # Handle the main client communication
        except Exception as e:
            logging.error(f"Client disconnected with error: {e}")
        finally:
            if writer in self.connected_clients:
                self.connected_clients.remove(writer)
            writer.close()
            try:
                await writer.wait_closed()
            except ConnectionResetError:
                logging.error("Client forcibly closed the connection")

    async def handle_main(self, reader, writer):
        addr = writer.get_extra_info('peername')
        try:
            while True:
                choice = await reader.readline()
                choice = choice.decode('utf-8').strip()

                logging.info(f"Received choice from {addr}: {choice}")

                writer.write("Received Choice\n".encode('utf-8'))
                await writer.drain() # Flush the write buffer, ensuring the client receives the data

                if choice == "LOGIN":
                    await self.login(reader, writer) #ensures functions run asynchronously using await keyword
                elif choice == "REGISTER":
                    await self.register(reader, writer)
                elif choice == "FETCH_FOOD_DATA":
                    await self.fetch_food_data(reader, writer)
                elif choice == "FETCH_CLIENT_DATA":
                    await self.fetch_client_data(reader, writer)
                elif choice == "ADD":
                    await self.add_food_item(reader, writer)#
                elif choice == "FETCH_LOGGING_INFO":
                    await self.fetch_logs(reader, writer)
                elif choice == "HEARTBEAT":
                    logging.info("Heartbeat received")
                    await self.handle_heartbeat(reader, writer)
                else:
                    logging.warning(f"Invalid choice received from {addr}: {choice}")
                    break
        except asyncio.CancelledError:
            raise
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            logging.info(f"Disconnected: {addr}")
            writer.close()
            await writer.wait_closed()

    async def handle_heartbeat(self, reader, writer):
        try:
            heartbeat = (await reader.readline()).decode('utf-8').strip()
            logging.info(f"Heartbeat from {writer.get_extra_info('peername')}")
        except Exception as e:
            logging.error(f"Heartbeat error: {e}")

    async def login(self, reader, writer):
    
        try:
            username = await reader.readline()
            password = await reader.readline()
            username = username.decode('utf-8').strip()
            password = password.decode('utf-8').strip()
            print(self.login_attempts)
            logging.info(f"Login attempt for username: {username}")

            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("SELECT password, salt, admin FROM userdata WHERE username_client = ?", (username,))
            result = cur.fetchone()

            if result:
                stored_hashed_password = base64.b64decode(result[0])
                salt = base64.b64decode(result[1])
                hashed_password = scrypt(password.encode('utf-8'), salt, 32, N=2**14, r=8, p=1)
                admin_status = result[2]

                if stored_hashed_password == hashed_password and self.login_attempts <= 3:
                    if admin_status == 1:
                        writer.write("Admin Login Successful!\n".encode('utf-8'))
                        logging.info(f"Admin Login Successful for username: {username}")
                    else:
                        writer.write("Login Successful!\n".encode('utf-8'))
                        logging.info(f"Login Successful for username: {username}")
                elif self.login_attempts > 3:
                    writer.write("Login Attempts Exceeded!Account locked out!Contact admin!\n".encode('utf-8'))
                    logging.warning(f"Login Attempts Exceeded for username: {username}")
                    cur.execute("UPDATE userdata SET can_login = 0 WHERE username_client = ?", (username,))
                    logging.warning(f"user login blocked for: {username}")

                else:
                    self.login_attempts += 1
                    writer.write("Login Failed!\n".encode('utf-8'))
                    logging.warning(f"Login Failed for username: {username}")
            else:
                writer.write("Login Failed!\n".encode('utf-8'))
                logging.warning(f"Login Failed for username: {username}")
            conn.close()
        except sqlite3.Error as db_error:
            logging.error(f"Database error during login: {db_error}")
        except Exception as e:
            logging.error(f"An error occurred during login: {e}")

    async def register(self, reader, writer):
        try:
            username = await reader.readline()
            password = await reader.readline()
            username = username.decode('utf-8').strip()
            password = password.decode('utf-8').strip()

            logging.info(f"Register attempt for username: {username}")

            salt = get_random_bytes(16)
            hashed_password = scrypt(password.encode('utf-8'), salt, 32, N=2**14, r=8, p=1)

            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("SELECT username_client FROM userdata WHERE username_client = ?", (username,))
            if cur.fetchone():
                writer.write("Account already registered!\n".encode('utf-8'))
                logging.warning(f"Account already registered for username: {username}")
            else:
                cur.execute("INSERT INTO userdata (username_client, password, salt) VALUES (?, ?, ?)", 
                            (username, base64.b64encode(hashed_password).decode('utf-8'), base64.b64encode(salt).decode('utf-8')))
                conn.commit()
                writer.write("Register successful!\n".encode('utf-8'))
                logging.info(f"Register successful for username: {username}")
            conn.close()
        except sqlite3.Error as db_error:
            logging.error(f"Database error during registration: {db_error}")
        except Exception as e:
            logging.error(f"An error occurred during registration: {e}")

    async def fetch_food_data(self, reader, writer):
        try:
            username = (await reader.readline()).decode('utf-8').strip()
            logging.info(f"Fetching food data for username: {username}")

            now = datetime.now()
            current_date = now.strftime("%d-%m-%Y")

            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("SELECT date, food_item, calories FROM calorie_data WHERE username = ? AND date = ?", (username, current_date))
            data = cur.fetchall()
            conn.close()
            logging.info(f"Food data fetched for username {username}: {data}")
            writer.write(f"{data}\n".encode('utf-8'))
            await writer.drain()
        except sqlite3.Error as db_error:
            logging.error(f"Database error while fetching food data: {db_error}")
        except Exception as e:
            logging.error(f"An error occurred while fetching food data: {e}")

    async def add_food_item(self, reader, writer):
        try:
            food = (await reader.readline()).decode('utf-8').strip()
            calories = (await reader.readline()).decode('utf-8').strip()
            username = (await reader.readline()).decode('utf-8').strip()

            logging.info(f"Adding food item for username {username}: {food}, {calories}")

            now = datetime.now()
            current_date = now.strftime("%d-%m-%Y")

            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO calorie_data (username, date, food_item, calories) VALUES (?, ?, ?, ?)", (username, current_date, food, calories))
            conn.commit()
            conn.close()
            writer.write("Food item added!\n".encode('utf-8'))
            await writer.drain()
        except sqlite3.Error as db_error:
            logging.error(f"Database error while adding food item: {db_error}")
        except Exception as e:
            logging.error(f"An error occurred while adding food item: {e}")

    async def fetch_client_data(self, reader, writer):
        try:
            logging.info("Fetching client data")

            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("SELECT username_client FROM userdata")

            username_data = cur.fetchall()
            conn.close()
            logging.info(f"Client data fetched: {username_data}")
            writer.write(f"{username_data}\n".encode('utf-8'))
            await writer.drain()
        except sqlite3.Error as db_error:
            logging.error(f"Database error while fetching client data: {db_error}")
        except Exception as e:
            logging.error(f"An error occurred while fetching client data: {e}")

    async def fetch_logs(self, reader, writer):
        try:
            logging.info("Fetching recent logs")

            with open('server.log', 'r') as f:
                logs = f.readlines()[-10:]
            logs = ''.join(logs)

            logging.info("Recent logs fetched")
            writer.write(logs.encode('utf-8'))
            await writer.drain()
        except Exception as e:
            logging.error(f"An error occurred while fetching logs: {e}")

server = Server()
asyncio.run(server.start())
