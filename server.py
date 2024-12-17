import sqlite3
import hashlib
import socket
import threading
import jwt
import datetime

class Server:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 55555
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
    
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
                        
                        # token_gen = Tokens()
                        # token_gen.gen_token(username)
                        # token = token_gen.current_token
                        
                        # conn = sqlite3.connect("userdata.db")
                        # cur = conn.cursor()
                        # cur.execute("UPDATE userdata SET token = ? where username = ?", (token, username))
                        # conn.commit()
                        # c.send(f"Login Successful! Token = {token}".encode())
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

    def handle_calorie_tracker(self, c, username):
        while True:
            try:
                choice = c.recv(1024).decode()

            except:
                pass

    def view_data(self, c, username):
        pass

    def add_food_item(self, c, username):
        pass


class Tokens:
    def __init__(self) -> None:
        self.temp_secret_key = "tempkey"
        self.current_token = ""


    def gen_token(self, username):
        token_store = {
            "username" : username,
            "expiry" : datetime.datetime.utcnow() + datetime.timedelta(hours=5)
        }
        token = jwt.encode(token, self.temp_secret_key, algorithm=["HS256"])
        self.current_token = token
        return token
    

    def verify_token(self, token):
        try:
            key = jwt.decode(token, self.temp_secret_key, algorithms=["HS256"])
            return True, key
        except jwt.ExpiredSignatureError:
            return False, "Token has expired"
        except jwt.InvalidTokenError:
            return False, "Invalid Token"



server1 = Server()

while True:
    client, address = server1.server.accept()
    threading.Thread(target=server1.handle_login, args=(client,)).start()
