# encoding: utf-8
from SendingThread import *
from ReceivingThread import *
from random import randint
import time

STATUS = ['CONNECTING',
          'CONNECTED',
          'CLOSING',
          'CLOSED',
          'FINISHED']

class Connection(object):
  """
    Object can be instanced in receiving or sending mode depending on the
    presence of an argument on creation.
  """
  def __init__(self, ip_address = "0.0.0.0", destination_port = 5005, source_port = 5005):
    super(Connection, self).__init__()
    self.set_status('CLOSED')
    self.__ip_address = ip_address
    self.__source_port = source_port
    self.__destination_port = destination_port
    self.__dict_seq_index = {}
    self.__start_sending()
    self.__start_receiving()    
    self.ack_array = []
      
  # unknown behavior
  def __exit__(self, exc_type, exc_value, traceback):
    self.package_obj.cleanup()

  def send(self, format, data):
    """
    C style format: %s, %d and %b supported
    data should be iterable
    """
    if self.__status == 'CLOSED':
      self.__opening_procedure()
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
    self.__receiving_thread = ReceivingThread(self)
    self.__receiving_thread.start()

  def __opening_procedure(self):
    self.set_status('CONNECTING')
    self.__send_SYN()
    while (self.__status != 'CONNECTED'):
      print('sleeping')
      time.sleep(0.1)                               # CAREFUL
    print("Connection is now CONNECTED")

  def __closing_procedure(self):
    self.set_status('CLOSING')
    self.__send_FIN()
    while (self.__status != 'CLOSED'):
      time.sleep(0.1)
    print("Connection is now CLOSED")

  def __send_SYN(self):
    self.__sending_thread.add('', '', 'SYN')

  def __send_FIN(self):
    self.__sending_thread.add('', '', 'FIN')

  def __send_ACK(self, seq, ack):
    self.__sending_thread.add_ack(seq, 'ACK', ack)

  def __send_dataACK(self, seq):
    self.__sending_thread.add_ack(seq, 'dataACK')

  def __send_SYNACK(self, seq):
    self.__sending_thread.add_ack(seq, 'SYNACK')

  def __send_FINACK(self):
    self.__sending_thread.add_ack(seq, 'FINACK')

  def validate_ack(self, header): ###### WIP
    flag = header.get_flag()
    ack = header.get_ack_number()
    indice = self.look_for_msg(ack)
    if indice >= 0:
      self.ack_array[indice] = True
      if self.__status == 'OPENING' and CanalPlusHeader.FLAG['SYNACK'] == flag:
        self.set_status('OPEN')
      if self.__status == 'CLOSING' and CanalPlusHeader.FLAG['FINACK'] == flag:
        self.set_status('CLOSED')
    return ack
    
  def link(self, seq, indice):
    self.__dict_seq_index[seq]= indice
    
  def add_ack(self, seq, type, ack):
    self.__sending_thread.add_ack(seq, type, ack)
    
  def look_for_msg(self, ack):
    try:
      indice = self.__dict_seq_index[ack - 1]
    except:
      indice = -1
    return indice
    
  def handle_incoming(self, header, received_msg):
    flag = header.get_flag()
    status = self.__status
    if flag == CanalPlusHeader.FLAGS['ACK'] and status == 'CONNECTING':
      status = 'CONNECTED'
    elif flag == CanalPlusHeader.FLAGS['data'] and status == 'CONNECTED':
      self.__receiving_thread.add_message_to_dict(seq, message[128:])
    elif flag == CanalPlusHeader.FLAGS['SYN'] and status == 'CLOSED':
      ### TO DO HERE SET LISTENNING IP
      status = 'CONNECTING'
    elif flag == CanalPlusHeader.FLAGS['FIN'] and status == 'CONNECTED':
      ### TO DO HERE SET LISTENNING IP
      status = 'CLOSING'
    elif flag == CanalPlusHeader.FLAGS['dataACK'] and status == 'CONNECTED':
      pass
    elif flag == CanalPlusHeader.FLAGS['SYNACK'] and status == 'CONNECTING':
      status = 'CONNECTED'
    elif flag == CanalPlusHeader.FLAGS['FINACK']:
      pass
    else:
      return 3
    self.set_status(status)
    ack = header.get_ack_number()
    seq = header.get_sequence_number()
    indice = self.look_for_msg(ack)
    if indice >= 0:
      self.ack_array[indice] = True
    return seq
    
  def set_status(self, status):
    print(status)
    self.__status = status
    
  def set_ip_address(self, ip):
    print('new IP: ', ip)
    self.__ip_address = ip