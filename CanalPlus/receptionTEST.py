import Connection


connect = Connection.Connection("0.0.0.0", destination_port = 5006, source_port = 5005)
while True:
  data = connect.receive()
  if len(data) > 0:
    print(data)