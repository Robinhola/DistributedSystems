import time
import threading
import Message
from CanalPlusHeader import *
import socket


class ReceivingThread(threading.Thread):
  def __init__(self, connection ,buffer_size = 35):
    super(ReceivingThread, self).__init__()
    self.connection = connection
    self.receiving_buffer = []
    self.data_waiting_dict = {}
    self.data = []
    self.sock = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM)     # UDP
    try:
      self.sock.bind((connection.get_ip_address(),
                    connection.get_source_port()))
    except:
      pass
      
  def run(self): # WIP
    while self.connection.get_status() != 'FINISHED':
      self.receive()
      while len(self.receiving_buffer) > 0:
        message = self.receiving_buffer.pop(0)
        header = CanalPlusHeader()
        header.turn_bytes_to_header(message)
        seq = self.connection.handle_incoming(header, message)
        if seq > 0: 
          if header.message_needs_ack():
            self.connection.new_msg_event.set()
            self.send_ack(header)
            if header.message_contains_data():
              self.add_message_to_dict(seq, message[128:])    # CAREFUL SEQS:
          else:
            data = self.pop_message_from_dict(seq)
            self.treat_data(data)

  def read(self):
    data = bytes()
    if(len(self.data) == 0):
      self.connection.data_received_event.wait()
    data = self.data.pop(0)
    self.connection.data_received_event.clear()
    return data

  def send_signal_buffer_full(self):
    pass

  def receive(self):
    data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
    if (self.connection.get_ip_address() == '0.0.0.0'):
      self.connection.set_ip_address(addr[0])
    header = CanalPlusHeader()
    header.turn_bytes_to_header(data)
    # print("header flag:", header.get_flag()) # DEBUG
    self.receiving_buffer.append(data)

  def send_ack(self, header):
    seq, ack = self.gather_seqack(header)
    flag = header.get_flag()
    type = CanalPlusHeader.TYPES[flag]
    self.connection.add_ack(seq, type, ack)

  def gather_seqack(self, header):
    seq = header.get_sequence_number()
    ack = header.get_ack_number()
    return seq, ack

  def add_message_to_dict(self, seq, message):
    self.data_waiting_dict[seq] = message

  def pop_message_from_dict(self, seq):
    data = bytes()
    try:
      data = self.data_waiting_dict[seq]
      del self.data_waiting_dict[seq]
    except:
      pass
    return data

  def treat_data(self, data):
    if len(data) > 0:
      self.data.append(data)
      self.connection.data_received_event.set()