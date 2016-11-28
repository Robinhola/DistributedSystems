import Connection

UDP_IP = "127.0.0.1"

t = ("lol", "jambe")
t1 = ("lol1", "jambe1")

l = [t, t1]

for k,j in l:
  print k
  print j

def tuplee():
  ack = 4
  seq = 18
  return ack, seq
  
a,c = tuplee()
print a
print c
#conn = Connection.Connection(UDP_IP)
#conn.send("%d", 3)


#    self.connection.__dict_seq_ack[message.get_header().get_sequence_number()] = message.get_header().get_ack_number()
