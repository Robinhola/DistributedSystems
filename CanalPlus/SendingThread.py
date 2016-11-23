# encoding: utf-8
import threading
from Message import *
import time

class SendingThread(threading.Thread):
  def __init__(self, connection, ip_address):
    super(SendingThread, self).__init__()
    self.target_ip_address = ip_address
    self.connection = connection
    self.target_buffer_full = False
    self.sending_list = []
    self.ack_array = []
    self.ack_array_next_free_cell = []

  def run(self):
    self.start_receiving_acks(self)
    self.establish_connection(self)
    while self.connection.status == "established":
      if self.has_message_to_process() and self.target_buffer_not_full():
        self.send_next_message()
      else:
        continue
    self.handle_connection_ending()

  def add_data(self, format, data): ######## WIP
    header = self.create_header(self)
    formated_data = Message.format_data(format, data)
    message.add_content(header, formated_data)
    message.wrapping()
    self.append_to_sending_list(message)
    self.add_to_ack_array(message)
  
  def send_next_message(self):
    message = self.pop_next_message();
    if not message.has_been_read():
      if message.time_since_last_try_not_short():
        message.try_to_send()
      self.append_to_sending_list(message)
    else:
      self.remove_message(message)

  def start_receiving_acks(self):
    self.ack_receiving_thread = ReceivingAckThread(self.ack_queue)
    self.ack_receiving_thread.start()

  def establish_connection(self):
    print ("Not implemented yet")
    pass

  def has_message_to_process(self):
    return len(sending_list) > 0

  def target_buffer_not_full(self):
    return not self.target_buffer_full

  def handle_connection_ending(self):
    print ("Not implemented yet")
    pass
    
  def add_to_ack_array(self, Message message):
    indice = self.ack_array_next_free_cell.pop()
    self.ack_array[indice] = False
    message.set_ack_number(indice)

  def pop_next_message(self):
    Message message = self.sending_list.pop()
    int ack = message.get_ack_number()
    if self.ack_array[ack]:
      message.has_been_read()
    return message

  def append_to_sending_list(self, Message message):
    self.sending_list.append(message)

  def remove_message(self, message):
    ack = message.get_ack_number()
    id_num = message.get_id()
    self.ack_array[ack] = False
    self.ack_array_next_free_cell.append(ack)
    message.delete()

  def __create_header(self): 