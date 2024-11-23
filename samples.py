import sqlite3
import hashlib

connection = sqlite3.connect("userdata.db")
cur = connection.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
        id INTEGER PRIMARY KEY,
        username VARCHAR(255),
        password VARCHAR(255)    
    )
""")

username1, password1 = "kas", hashlib.sha256("kaspass".encode()).hexdigest()
username2, password2 = "george", hashlib.sha256("georgiscool".encode()).hexdigest()
username3, password3 = "filip", hashlib.sha256("flipflop".encode()).hexdigest()
username4, password4 = "breaker", hashlib.sha256("breakingthings".encode()).hexdigest()

cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username1, password1))
cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username2, password2))
cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username3, password3))
cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username4, password4))

connection.commit()
