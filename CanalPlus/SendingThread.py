# encoding: utf-8
import threading
from Message import *
from CanalPlusHeader import *
import time
from random import randint 
import socket

RANGE = 99999


class SendingThread(threading.Thread):

  def __init__(self, connection, ip_address):
    super(SendingThread, self).__init__()
    self.target_ip_address = ip_address
    self.connection = connection
    self.target_buffer_full = False
    self.sending_list = []
    self.ack_array = []
    self.ack_array_next_free_cell = []

  random_number = 0

  def run(self):
    #self.start_receiving_acks()
    self.establish_connection()
    while self.connection.get_status() == "established":
      if self.has_message_to_process() and self.target_buffer_not_full():
        self.send_next_message()
      else:
        continue
    self.handle_connection_ending()

  def add(self, format, data):
    message = self.create_message(format, data)
    self.append_to_sending_list(message)
    self.add_to_ack_array(message)
            
  def send_next_message(self): ######## WIP
    print("sending message")
    message = self.pop_next_message();
    received = message.get_ack_status()
    if not received:
      if message.time_since_last_try_not_short():
        self.try_to_send(message)
      self.append_to_sending_list(message)
    else:
      self.remove_message(message)

  def start_receiving_acks(self):
    self.ack_receiving_thread = ReceivingAckThread(self.ack_queue)
    self.ack_receiving_thread.start()

  def establish_connection(self):
    self.connection.is_connected()
    print ("establish_connection Not really implemented yet")
    pass

  def has_message_to_process(self):
    return len(self.sending_list) > 0

  def target_buffer_not_full(self):
    return not self.target_buffer_full

  def handle_connection_ending(self):
    print ("handle_connection_ending Not implemented yet")
    pass

  def add_to_ack_array(self, message):
    indice = self.ack_array_next_free_cell.pop()
    self.ack_array[indice] = False
    message.set_ack_number(indice)

  def pop_next_message(self):
    message = self.sending_list.pop()
    ack = message.get_ack_number()
    if self.ack_array[ack]:
      message.has_been_read()
    return message

  def append_to_sending_list(self, message):
    self.sending_list.append(message)

  def remove_message(self, message):
    ack = message.get_ack_number()
    id_num = message.get_id()
    self.ack_array[ack] = False
    self.ack_array_next_free_cell.append(ack)
    message.delete()

  def create_message(self, format, data):
    message = Message(format, data)
    self.id_message(message)
    return message 

  def id_message(self, message):
    random_number = randint(1, RANGE)
    message.set_id(random_number)

  def create_header(self):
    return CanalPlusHeader()

  def try_to_send(self, message):
    message.time_since_last_try = time.gmtime()
    sock = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM) # UDP
    UDP_IP = self.connection.get_ip_address()
    UDP_PORT = self.connection.get_destination_port()
    print (message.content)
    sock.sendto(message.content, (UDP_IP, UDP_PORT))
