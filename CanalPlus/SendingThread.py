# encoding: utf-8
import threading
from Message import *
from CanalPlusHeader import *
from random import randint 
import socket

RANGE = 4294967295


class SendingThread(threading.Thread):

  def __init__(self, connection, ip_address):
    super(SendingThread, self).__init__()
    self.target_ip_address = ip_address
    self.connection = connection
    self.target_buffer_full = False
    self.ack_sending_tuples = [] # list of ack tuples (seq, ack) 
    self.sending_list = []
    self.ack_sending_list = []
    self.ack_array_next_free_cell = []
    self.sock = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM) # UDP

  random_number = 0

  def run(self):
    self.connection.connected()
    while self.connection.get_status() == "established":
      if not self.target_buffer_full:
        while self.has_ack_to_process():
          self.send_next_ack()
        if self.has_message_to_process():
          self.send_next_message()
      else:
        time.sleep(.300)

  def add(self, format, data, type = 'data'):
    message = self.create_message(format, data, type)
    self.append_to_sending_list(message)
    self.add_to_ack_array(message)

  def add_ack(self, type, seq = 0, ack = 0):
    ack_msg = self.create_ack(type, seq, ack)
    self.append_to_ack_list(ack_msg)

  def send_next_message(self):
    message = self.pop_next_message();
    received = message.get_ack_status()
    if not received:
      if message.time_since_last_try_not_short():
        print("sending message")
        self.try_to_send(message)
      elif len(self.sending_list) == 0:
        time.sleep(TIME_BEFORE_SENDING_AGAIN_ms/1000)
      self.append_to_sending_list(message)
    else:
      self.remove_message(message)

  def send_next_ack(self):
    print("sending ack")
    ack_msg = self.pop_next_ack()
    self.try_to_send(ack_msg)

  def add_to_ack_array(self, message):
    try:
      indice = self.ack_array_next_free_cell.pop()
      self.connection.ack_array[indice] = False
    except Exception:
      self.connection.ack_array.append(False)
      indice = len(self.connection.ack_array) - 1
    message.set_ack_number(indice)
    seq = message.get_header().get_sequence_number()
    self.connection.link(seq, indice)

  def create_message(self, format, data, type = 'data'):
    random_number = randint(1, RANGE)
    message = Message(format, data, type, random_number)
    message.set_id(random_number)
    return message

  def pop_next_message(self):
    message = self.sending_list.pop()
    ack = message.get_ack_number()
    if self.connection.ack_array[ack]:
      message.has_been_read()
    return message

  def append_to_sending_list(self, message):
    self.sending_list.append(message)

  def remove_message(self, message):
    ack = message.get_ack_number()
    id_num = message.get_id()
    self.connection.ack_array[ack] = False
    self.ack_array_next_free_cell.append(ack)
    message.delete()

  def create_ack(self, seq, type = 'dataACK', ack = 0):
    ack_msg = Message('', '', type)
    ack_msg.get_header().decide_seq_and_ack(type, seq, ack)
    return ack_msg

  def pop_next_ack(self):
    ack_msg = self.ack_sending_list.pop()
    return ack_msg

  def append_to_ack_list(self, ack_msg):
    self.ack_sending_list.append(ack_msg)

  def try_to_send(self, message):
    content = bytes()
    UDP_IP = self.connection.get_ip_address()
    UDP_PORT = self.connection.get_destination_port()
    content += message.content[0] + message.content[1]
    message.time_since_last_try = int(round(time.time() * 1000))
    self.sock.sendto(content, (UDP_IP, UDP_PORT))

  def has_message_to_process(self):
    return len(self.sending_list) > 0

  def has_ack_to_process(self):
    self.connection.connected()
    return len(self.ack_sending_list) > 0
