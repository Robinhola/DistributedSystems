# encoding: utf-8
import Connection
import itertools

UDP_IP = "127.0.0.1"

a = bytes(UDP_IP, 'utf-8') + bytes([3])
print(a)
#conn = Connection.Connection(UDP_IP)
#conn.send("%d", 3)

sequence_number = 1  
ack_number = 1     
source_port = 5005      
destination_port = 5005 
nb_of_fields = 5        
flag = 0            
window_size = 32
ports = [source_port, destination_port]
numbers = [sequence_number, ack_number]
specifications = [nb_of_fields, flag, window_size]
values = itertools.chain(ports, numbers, specifications)
results = ''
print(values)
listage = []
for val in values:
  print (val)
  listage.append(val.to_bytes(2,'little'))
print(listage)
for li in listage:
  results += str(li)
print(results)



val = [0,1,2,3,4,5,65,7,8,9]
print(val)

results = [val[0].to_bytes(16,'big'),
          val[1].to_bytes(16,'big'),
          val[5].to_bytes(32,'big'),
          val[2].to_bytes(32,'big'),
          val[3].to_bytes(16,'big'),
          val[4].to_bytes(16,'big')]
s = ''
for res in results:
  s = s + str(res)
s = s.replace('b','').replace("'", '')
print(s)
#    self.connection.__dict_seq_ack[message.get_header().get_sequence_number()] = message.get_header().get_ack_number()
