import Connection

UDP_IP = "127.0.0.1"

connect = Connection.Connection(UDP_IP, destination_port = 5005, source_port = 5006)
connect.send("%d", "Bonjour")
connect.send("%d", "Grégoire")
print(connect.receive())
connect.close()