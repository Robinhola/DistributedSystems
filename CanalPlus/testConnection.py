import Connection

UDP_IP = "127.0.0.1"

connect = Connection.Connection(UDP_IP)
connect.send("%d", "Bonjour")