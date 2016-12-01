import Connection

UDP_IP = "127.0.0.1"
LOCALIP = "192.168.1.23"
IP = '151.80.40.119'

connect = Connection.Connection(UDP_IP, destination_port = 5006, source_port = 5005)
connect.send("%d", "Bonjour")
connect.send("%d", "Grégoire")
print(connect.receive())
connect.close()