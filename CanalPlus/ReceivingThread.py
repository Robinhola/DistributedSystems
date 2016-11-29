import threading
import Message
from CanalPlusHeader import *
from queue import *
import socket


class ReceivingThread(threading.Thread):
  def __init__(self, connection ,buffer_size = 35):
    super(ReceivingThread, self).__init__()
    self.connection = connection
    self.receiving_buffer = bytearray(b'------------')
    self.data_waiting_dict = {}
    self.data = []
    self.sock = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM) # UDP
        
  def run(self): # WIP
    while True:
      self.receive()
      for message in self.receiving_buffer:
        header = CanalPlusHeader()
        header.turn_bytes_to_header(message)
        seq = connection.validate_ack(header)
        if seq > -1: 
          if header.message_needs_ack():
            self.send_acks(header)
            if header.message_contains_data():
              self.add_message_to_dict(seq, message[128:])
          else:
            data = self.pop_message_from_dict(seq)
            self.treat_data(data)

  def read(self):
    data = bytes()
    if len(self.data) > 0:
      data = self.data.pop()
    return data

  def send_signal_buffer_full(self):
    pass

  def receive(self):
    self.sock.recvmsg_into([self.receiving_buffer])

  def send_ack(self, header):
    seq, ack = self.gather_seqack(header)
    flag = header.get_flag()
    type = CanalPlusHeader.TYPES[flag]
    self.connection.__sending_thread.add_ack(seq, type, ack)

  def gather_seqack(self, header):
    seq = header.get_sequence_number()
    ack = header.get_ack_number()
    return seq, ack

  def add_message_to_dict(self, seq, message):
    self.data_waiting_dict[seq: message]

  def pop_message_from_dict(self, seq):
    data = bytes()
    data = self.data_waiting_dict[seq]
    del self.data_waiting_dict[seq]
    return data

  def treat_data(self, data):
    self.data.append(data)