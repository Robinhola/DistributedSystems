import Connection

UDP_IP = "127.0.0.1"

conn = Connection.Connection(UDP_IP)
conn.send("%d", 3)
