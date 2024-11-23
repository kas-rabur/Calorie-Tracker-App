import sqlite3
import hashlib
import socket
import threading

host = "127.0.0.1"
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()


def handle(c):
    c.send("Username: ".encode())
    username = c.recv(1024).decode()

    c.send("Password: ".encode())
    password = c.recv(1024)
    password = hashlib.sha256(password).hexdigest()

    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

    if cur.fetchall():
        c.send("Login Successful!".encode())
    else:
        c.send("Login failed!".encode())

while True:
    client, address = server.accept()
    threading.Thread(target=handle, args=(client,)).start()