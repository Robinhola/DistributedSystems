import Connection

UDP_IP = "127.0.0.1"

connect = Connection.Connection()
while True:
  data = connect.receive()
  if len(data) > 0:
    print(data)