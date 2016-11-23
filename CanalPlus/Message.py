# encoding: utf-8
import time
from CanalPlusHeader import *

TIME_BEFORE_SENDING_AGAIN_ms = 150 #ms

class Message(object):
  """docstring for Message"""
  def __init__(self, format, data, type = 'data'):
    super(Message, self).__init__()
    self.type = type
    self.id = '1234' + 'time'
    self.ack_number = -1
    self.ack_status = False
    self.time_since_last_try = 0
    self.content = [CanalPlusHeader(), self.format_data(format, data)]
    self.wrapping()

  def wrapping(self):
    print ("Not implemented yet")
    pass

  def format_data(format, data):
    return PyBytes_FromFormat(format, data)

  def time_since_last_try_not_short(self):
    diff = time.gmtime() - self.time_since_last_try
    diff = diff * 1000
    return diff > TIME_BEFORE_SENDING_AGAIN_ms 

  def has_been_received(self):
    self.ack_status = True

  def try_to_send(self):
    self.time_since_last_try = time.gmtime()
    print ("Not implemented yet")

  def set_ack_number(self, ack_number):
    self.ack_number = ack_number

  def get_id(self):
    return self.id

  def get_ack_number(self):
    return self ack_number

  def get_ack_status(self):
    return self.ack_status