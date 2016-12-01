import Connection


connect = Connection.Connection("0.0.0.0", destination_port = 5005, source_port = 5006)
data1 = connect.receive() 
data2 = connect.receive() 
print(data1, data2)
print(connect.get_status())
connect.send("%d", "Bonjour, Robin")