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
    self.status = 'CLOSED'
    self.__ip_address = ip_address
    self.__source_port = source_port
    self.__destination_port = destination_port
    self.__dict_seq_index = {}
    self.new_msg_event = threading.Event()
    self.data_received_event = threading.Event()
    self.__start_sending()
    self.__start_receiving()    
    self.ack_array = []

  # unknown behavior
  def __exit__(self, exc_type, exc_value, traceback):
    # self.package_obj.cleanup()
    pass

  def send(self, format, data):
    """
    C style format: %s, %d and %b supported
    data should be iterable
    """
    self.new_msg_event.set()
    if self.status == 'CLOSED':
      self.__opening_procedure()
    self.__sending_thread.add(format, data)

  def receive(self):
    return self.__receiving_thread.read()

  def close(self):
    self.__closing_procedure() 
    self.__exit__(None, None, None)

  def get_status(self):
    return self.status

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
    while (self.status != 'CONNECTED'):
      time.sleep(0.1)                               # CAREFUL
    # print("Connection is now CONNECTED") # DEBUG

  def __closing_procedure(self):
    self.set_status('CLOSING')
    self.__send_FIN()
    while (self.status != 'CLOSED'):
      time.sleep(0.1)
    # print("Connection is now CLOSED") # DEBUG

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

  def link(self, seq, indice):
    self.__dict_seq_index[seq]= indice
    
  def add_ack(self, seq, type, ack):
    self.__sending_thread.add_ack(seq, type, ack)
    
  def __look_for_msg(self, ack):
    try:
      indice = self.__dict_seq_index[ack]
    except:
      indice = -1
    return indice
    
  def handle_incoming(self, header, received_msg):
    flag = header.get_flag()
    seq = header.get_sequence_number()
    if flag > 10:
      self.__handle_msgACK(header)
    elif flag > 0:
      self.__handle_msg(header, received_msg)
    else:
      self.__handle_ACK(header)
    indice = self.__look_for_msg(seq)
    if indice >= 0:
      self.ack_array[indice] = True
    return seq
    
  def set_status(self, status):
    # print('new Status:', status) # DEBUG
    self.status = status
    
  def set_ip_address(self, ip):
    # print('new IP: ', ip) # DEBUG
    self.__ip_address = ip

  def __handle_msgACK(self, header):
    flag = header.get_flag()
    if flag == CanalPlusHeader.FLAGS['dataACK'] and self.status == 'CONNECTED':
      # HERE RESTART TIMEOUT TIMER
      pass
    elif flag == CanalPlusHeader.FLAGS['SYNACK'] and self.status == 'CONNECTING':
      self.set_status('CONNECTED')
    elif flag == CanalPlusHeader.FLAGS['FINACK'] and self.status == 'CLOSING':
      self.set_status('CLOSED')
    
  def __handle_msg(self, header, received_msg):
    flag = header.get_flag()
    if flag == CanalPlusHeader.FLAGS['data'] and self.status == 'CONNECTED':
      seq = header.get_sequence_number()
      self.__receiving_thread.add_message_to_dict(seq, received_msg[128:])
    elif flag == CanalPlusHeader.FLAGS['SYN'] and self.status == 'CLOSED':
      self.set_status('CONNECTING')
    elif flag == CanalPlusHeader.FLAGS['FIN'] and self.status == 'CONNECTED':
      self.set_status('CLOSING')

  def __handle_ACK(self, header):
    flag = header.get_flag()
    if flag == CanalPlusHeader.FLAGS['ACK'] and self.status == 'CONNECTING':
      self.set_status('CONNECTED')