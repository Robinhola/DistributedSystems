import Connection


connect = Connection.Connection("0.0.0.0", destination_port = 5006, source_port = 5005)
data1 = connect.receive() 
data2 = connect.receive() 
print(data1, data2)
connect.send("%d", "Bonjour, Robin")