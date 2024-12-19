import socket
import threading
import hashlib
import sqlite3
from Crypto.Util import number

class Server:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 55555
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.prime = number.getPrime(256)
        self.base = 2

    def handle_client(self, client):
   
        server_private_key = number.getRandomRange(1, self.prime-1)
        server_public_key = pow(self.base, server_private_key, self.prime)

        client.send(str(self.prime).encode())
        client.send(str(self.base).encode())
        client.send(str(server_public_key).encode())

        client_public_key = int(client.recv(1024).decode())
        shared_key = pow(client_public_key, server_private_key, self.prime)
        print(f"Shared key: {shared_key}")

        self.handle_login(client)

    def handle_login(self, c):
        while True:
            try:
                choice = c.recv(1024).decode()
                print(f"Received Choice: {choice}")
                c.send("Received Choice".encode())
            
                if choice == "LOGIN":
                    username = c.recv(1024).decode()
                    password = c.recv(1024).decode()
                    password = hashlib.sha256(password.encode()).hexdigest()
                    print(f"Login Attempt From: {username}")

                    conn = sqlite3.connect("userdata.db")
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

                    if cur.fetchone():
                        c.send("Login Successful!".encode())
                        print("Login Successful!")
                        conn.close()
                        break
        
                    else:
                        c.send("Login Failed!".encode())
                        print("Login Failed!")

                elif choice == "REGISTER":
                    username = c.recv(1024).decode()
                    password = c.recv(1024).decode()
                    password = hashlib.sha256(password.encode()).hexdigest()
                    print(f"Register Attempt From: {username}")

                    conn = sqlite3.connect("userdata.db")
                    cur = conn.cursor()

                    cur.execute("SELECT username FROM userdata WHERE username = ?", (username,))
                    if cur.fetchone():
                        c.send("Account already registered!".encode())
                        print("Account already registered!")
                    else:
                        cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, password))
                        conn.commit()
                        c.send("Register successful!".encode())
                        print("Register successful!")
                        conn.close()
                else:
                    print("Invalid choice. Connection closing.")

            except Exception as e:
                print(f"An error occurred: {str(e)}")

    def fetch_food_data(self, username):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()
        cur.execute("SELECT date, food_item, calories FROM calorie_data")
        data = cur.fetchall()
        conn.close()
        print(data)
        return data

    def start(self):
        while True:
            client, addr = self.server.accept()
            threading.Thread(target=self.handle_client, args=(client,)).start()

server = Server()
server.start()
