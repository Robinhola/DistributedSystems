# encoding: utf-8
#import Connection
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



val = [0,155,2,3,4,5,65,7,8,9]
print(val)

results = [val[1].to_bytes(16,'big')]
# ,
#           val[1].to_bytes(16,'big'),
#           val[5].to_bytes(32,'big'),
#           val[2].to_bytes(32,'big'),
#           val[3].to_bytes(16,'big'),
#           val[4].to_bytes(16,'big')]
s = ''
for res in results:
  s = s + str(res)
# s = s.replace('b','').replace("'", '')

#    self.connection.__dict_seq_ack[message.get_header().get_sequence_number()] = message.get_header().get_ack_number()


print('TEST')

from CanalPlusHeader import *
header = CanalPlusHeader()
print(header.ports[0])
print(header.specifications[1])
byt = header.turn_into_bytes()
print(byt)
header.turn_bytes_to_header(byt)
print(header.ports[0])
print(header.specifications[1])

print(bytes('lol', 'utf-8'))

a = 4294967295
print(pow(2,32))
print(a)
print(a.bit_length())


import time
millis = int(round(time.time() * 1000))
time.sleep(0.3)
millis = int(round(time.time() * 1000)) - millis
print (millis)