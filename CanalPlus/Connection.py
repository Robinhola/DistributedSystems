# encoding: utf-8
from SendingThread import *
from ReceivingThread import *
from random import randint
import time


class Connection(object):
  """
    Object can be instanced in receiving or sending mode depending on the
    presence of an argument on creation.
  """
  def __init__(self, ip_address = "127.0.0.1", destination_port = 5005, source_port = 5005):
    super(Connection, self).__init__()
    self.__status = "closed"
    self.__source_port = source_port
    self.__destination_port = destination_port
    self.__dict_seq_index = {}
    self.ack_array = []
    self.__ip_address = ip_address
    self.__start_sending()
    self.__start_receiving()
      
  # unknown behavior
  def __exit__(self, exc_type, exc_value, traceback):
    self.package_obj.cleanup()

  def send(self, format, data):
    """
    C style format: %s, %d and %b supported
    data should be iterable
    """
    try:
      self.__sending_thread.add(format, data)
    except AttributeError:
      self.__start_sending()
      self.__sending_thread.add(format, data)

  def receive(self):
    try:
      return self.__receiving_thread.read()
    except AttributeError:
      self.__start_receiving()
      return self.__receiving_thread.read()    

  def close(self):
    self.__closing_procedure() 
    self.__exit__(self, None, None, None)

  def connected(self):
    self.__status = "established"

  def get_status(self):
    return self.__status

  def get_destination_port(self):
    return self.__destination_port

  def get_source_port(self):
    return self.__source_port

  def get_ip_address(self):
    return self.__ip_address
    
  def __start_sending(self):
    self.__sending_thread = SendingThread(self, self.__ip_address)
    self.__sending_thread.start()

  def __start_receiving(self):
    self.__receiving_thread = ReceivingThread(self, )
    self.__receiving_thread.start()

  def __opening_procedure(self):
    self.__status = 'OPENING'
    self.__send_SYN()
    while (self.__status != 'OPEN'):
      time.sleep(0.1)
    print("Connection is now OPEN")

  def __closing_procedure(self):
    self.__status = 'CLOSING'
    self.__send_FIN()
    while (self.__status != 'CLOSED'):
      time.sleep(0.1)
    print("Connection is now CLOSED")

  def __send_SYN(self):
    self.__sending_thread.add(self, '', '', 'SYN')

  def __send_FIN(self):
    self.__sending_thread.add(self, '', '', 'FIN')

  def __send_ACK(self, seq, ack):
    self.__sending_thread.add_ack(seq, 'ACK', ack)

  def __send_dataACK(self, seq):
    self.__sending_thread.add_ack(seq, 'dataACK')

  def __send_SYNACK(self, seq):
    self.__sending_thread.add_ack(seq, 'SYNACK')

  def __send_FINACK(self):
    self.__sending_thread.add_ack(seq, 'FINACK')

  def validate_ack(self, header):
    self.connected()
    ack = header.get_ack_number()
    print("hey this is a ack", ack)
    return ack
    
  def link(self, seq, indice):
    self.__dict_seq_index[seq]= indice
    
  def add_ack(self, seq, type, ack):
    self.__sending_thread.add_ack(seq, type, ack)