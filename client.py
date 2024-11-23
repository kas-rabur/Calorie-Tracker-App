import socket

host = "127.0.0.1"
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

message = client.recv(1024).decode()
client.send(input(message).encode())

message = client.recv(1024).decode()
client.send(input(message).encode())

print(client.recv(1024).decode())