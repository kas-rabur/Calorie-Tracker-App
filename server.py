import sqlite3
import hashlib
import socket
import threading

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
                        break
                
                else:
                    print("Invalid choice. Connection closing.")

            except Exception as e:
                print(f"An error occurred: {str(e)}")

    def handle_chat():
        pass



server1 = Server()

while True:
    client, address = server1.server.accept()
    threading.Thread(target=server1.handle_login, args=(client,)).start()
