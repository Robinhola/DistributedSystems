# encoding: utf-8
import time
from CanalPlusHeader import *

TIME_BEFORE_SENDING_AGAIN_ms = 1500 #ms

class Message(object):
  """docstring for Message"""
  def __init__(self, format, data, type = 'data', seq = -1, ack = -1, connection = None):
    super(Message, self).__init__()
    self.type = type
    self.__id = 0
    self.__ack_number = -1
    self.__ack_status = False
    self.time_since_last_try = 0
    self.header = CanalPlusHeader()
    self.content = ['', self.format_data(format, data)]
    print (self.content)
    self.wrapping(connection, type, seq, ack)

  def wrapping(self, type, seq, ack, connection):
    if (connection != None):
      self.header.set_source_port(connection.get_source_port())
      self.header.set_destination_port(connection.get_destination_port())
    self.header.decide_seq_and_ack(type, seq, ack)
    self.header.compute_checksum(self.content[1])
    self.content[0] = self.header.turn_into_bytes()

  def create_from_bytes

  def format_data(self, format, data):
    b = bytes()
    if(not hasattr(data, '__iter__')):
        data = [data]
    if(format == '%s'):
      for d in data:
        b = bytes(data, 'utf-8')
    elif(format == '%d'):
        for d in data:
          b += d.to_bytes(64, 'big')
    elif(format == '%b')
        for d in data:
          b += d
    else:
      print('ERROR wrong format')
    return b
    
  def time_since_last_try_not_short(self):
    diff = time.time() - self.time_since_last_try
    diff = diff * 1000
    return diff > TIME_BEFORE_SENDING_AGAIN_ms 

  def set_id(self, id):
    self.__id = id

  def set_ack_number(self, ack_number):
    self.__ack_number = ack_number

  def has_been_received(self):
    self.__ack_status = True

  def get_id(self):
    return self.__id

  def get_ack_number(self):
    return self.__ack_number

  def get_ack_status(self):
    return self.__ack_status
    
  def get_header(self):
    return self.header