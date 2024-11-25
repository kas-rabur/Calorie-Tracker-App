import sqlite3
import hashlib
import socket
import threading

# host = "127.0.0.1"
# port = 55555

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((host, port))
# server.listen()

# def handle(c):
#     try:
#         choice = c.recv(1024).decode()
#         print(f"Received Choice: {choice}")
#         c.send("Received Choice".encode())
#         print(choice)

#         if choice == "LOGIN":
#             username = c.recv(1024).decode()
#             password = c.recv(1024).decode()
#             password = hashlib.sha256(password.encode()).hexdigest()
#             print(f"Login Attempt: {username}, {password}")

#             conn = sqlite3.connect("userdata.db")
#             cur = conn.cursor()

#             cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

#             if cur.fetchone():
#                 c.send("Login Successful!".encode())
#                 print("Login Successful!")
#             else:
#                 c.send("Login Failed!".encode())
#                 print("Login Failed!")

#             conn.close()

#         elif choice == "REGISTER":
#             username = c.recv(1024).decode()
#             password = c.recv(1024).decode()
#             password = hashlib.sha256(password.encode()).hexdigest()
#             print(f"Register Attempt: {username}, {password}")

#             conn = sqlite3.connect("userdata.db")
#             cur = conn.cursor()

#             cur.execute("SELECT username FROM userdata WHERE username = ?", (username,))
#             if cur.fetchone():
#                 c.send("Account already registered!".encode())
#                 print("Account already registered!")
#             else:
#                 cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, password))
#                 conn.commit()
#                 c.send("Register successful!".encode())
#                 print("Register successful!")

#         else:
#             print("NO IF STATEMENT")

#             conn.close()
#     except Exception as e:
#         c.send(f"An error occurred: {str(e)}".encode())
#         print(f"An error occurred: {str(e)}")
#     finally:
#         c.close()


class Server:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 55555
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
    
    def handle(self, c):
        try:
            choice = c.recv(1024).decode()
            print(f"Received Choice: {choice}")
            c.send("Received Choice".encode())
            print(choice)

            if choice == "LOGIN":
                username = c.recv(1024).decode()
                password = c.recv(1024).decode()
                password = hashlib.sha256(password.encode()).hexdigest()
                print(f"Login Attempt: {username}, {password}")

                conn = sqlite3.connect("userdata.db")
                cur = conn.cursor()

                cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

                if cur.fetchone():
                    c.send("Login Successful!".encode())
                    print("Login Successful!")
                else:
                    c.send("Login Failed!".encode())
                    print("Login Failed!")

                conn.close()

            elif choice == "REGISTER":
                username = c.recv(1024).decode()
                password = c.recv(1024).decode()
                password = hashlib.sha256(password.encode()).hexdigest()
                print(f"Register Attempt: {username}, {password}")

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

            else:
                print("NO IF STATEMENT")

                conn.close()
        except Exception as e:
            c.send(f"An error occurred: {str(e)}".encode())
            print(f"An error occurred: {str(e)}")
        finally:
            c.close()


server1 = Server()


while True:
    client, address = server1.server.accept()
    threading.Thread(target=server1.handle, args=(client,)).start()
