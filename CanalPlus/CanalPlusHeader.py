from random import randint 
import hashlib
import itertools

RANGE = 99999

class CanalPlusHeader(object):
  """docstring for CanalPlusHeader"""
  def __init__(self,                     \
                sequence_number = -1,    \
                ack_number = -1,         \
                source_port = 5005,      \
                destination_port = 5005, \
                nb_of_fields = 5,        \
                flag = 0,                \
                window_size = 32):
    super(CanalPlusHeader, self).__init__()
    self.ports = [source_port, destination_port]
    self.numbers = [sequence_number, ack_number]
    self.specifications = [nb_of_fields, flag, window_size]
    self.checksum = b''
  
  random_number = 0

  def turn_into_bytes(self):
    values = itertools.chain(self.ports, self.numbers, self.specifications)
    results = bytes([])
    for val in values:
      results = results +(bytes(values))
    results = results + bytes(self.checksum)
    print (results)
    return results

  def decide_seq_and_ack(self, type, previous_seq = 0, previous_ack = 0):
    if type == 'data' or type == 'SYN' or type == 'FIN':
      random_number = randint(1, RANGE)
      self.set_sequence_number(random_number)
    elif type == 'dataACK' or type =='SYNACK' or type == 'FINACK':
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

  def compute_checksum(self, data):
    m = hashlib.md5()
    m.update(self.turn_into_bytes())
    m.update(data)
    self.checksum = m.digest()
    print (m.digest())
    
  def set_source_port(self, value):
    self.port[0] = value
  
  def set_destination_port(self, value):
    self.port[1] = value
  
  def set_sequence_number(self, value):
    self.numbers[0] = value
  
  def set_ack_number(self, value):
    self.numbers[1] = value
  
  def set_flag(self, value):
    self.specifications[1] = value
  
  def set_window_size(self, value):
    self.specifications[2] = value
    
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
    
  def get_nb_of_fields(self):
    return self.specifications[0]
    
  def get_flag(self):
    return self.specifications[1]
    
  def get_window_size(self):
    return self.specifications[2]
    
  def get_checksum(self):
    return self.checksum