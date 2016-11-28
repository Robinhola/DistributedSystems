from random import randint 
import itertools

RANGE = 4294967295

class CanalPlusHeader(object):
  
  FLAGS = {'ACK':     0, 
          'SYN':      1, 
          'data':     2,
          'FIN':      3,
          'SYNACK':  11,
          'dataACK': 12,
          'FINACK':  13}

  def __init__(self,
              flag = 'ACK',
              sequence_number = 0,
              ack_number = 0,
              source_port = 5005,
              destination_port = 5005,
              window_size = 32):
    super(CanalPlusHeader, self).__init__()
    self.ports = [source_port, destination_port]
    self.numbers = [sequence_number, ack_number]
    self.specifications = [CanalPlusHeader.FLAGS[flag], window_size]
  
  random_number = 0

  def turn_into_bytes(self):
    b = bytes()
    results = [self.get_source_port().to_bytes(16,'big'),
              self.get_destination_port().to_bytes(16,'big'),
              self.get_sequence_number().to_bytes(32,'big'),
              self.get_ack_number().to_bytes(32,'big'),
              self.get_flag().to_bytes(16, 'big'),
              self.get_window_size().to_bytes(16,'big')]
    for res in results:
      b += res
    return b

  def turn_bytes_to_header(self, bheader):
    if(len(bheader) > 128):
      print("ERROR header too big")
      return
    self.ports = [int.from_bytes(bheader[0:16],'big'),
                  int.from_bytes(bheader[16:32],'big')]
    self.numbers = [int.from_bytes(bheader[32:64],'big'),
                    int.from_bytes(bheader[64:96],'big')]
    self.specifications = [int.from_bytes(bheader[96:112],'big'),
                          int.from_bytes(bheader[112:128],'big')]

  def decide_seq_and_ack(self, type, previous_seq = 0, previous_ack = 0):
    if type == 'dataACK' or type =='SYNACK' or type == 'FINACK':
      random_number = randint(RANGE)
      self.set_sequence_number(random_number)
      self.set_ack_number(previous_seq + 1)
    elif type == 'ACK':
      self.set_sequence_number(previous_ack)
      self.set_ack_number(previous_seq + 1)
    else:
      print ("not a valid type")
      return 0
    return 1

  def set_source_port(self, value):
    self.port[0] = value
  
  def set_destination_port(self, value):
    self.port[1] = value
  
  def set_sequence_number(self, value):
    self.numbers[0] = value
  
  def set_ack_number(self, value):
    self.numbers[1] = value
  
  def set_window_size(self, value):
    self.specifications[1] = value
    
  def set_checksum(self, value):
    self.checksum = value
  
  def get_source_port(self):
    return self.ports[0]

  def get_destination_port(self):
    return self.ports[1]
  
  def get_sequence_number(self):
    return self.numbers[0]
  
  def get_ack_number(self):
    return self.numbers[1]
    
  def get_flag(self):
    return self.specifications[0]
    
  def get_window_size(self):
    return self.specifications[1]
    
  def get_checksum(self):
    return self.checksum