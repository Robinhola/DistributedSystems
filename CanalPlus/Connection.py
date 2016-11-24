# encoding: utf-8
import sys
from SendingThread import *
import time
from random import randint


class Connection(object):
  """
    Object can be instanced in receiving or sending mode depending on the
    presence of an argument on creation.
  """
  def __init__(self, ip_address = "", destination_port = 5005, source_port = 5005):
    super(Connection, self).__init__()
    self.__status = "closed"
    self.__source_port = source_port
    self.__destination_port = destination_port
    if ip_address == "":
      self.__start_receiving()
    else:
      self.__ip_address = ip_address
      self.__start_sending()
      
  # unknown behavior
  def __exit__(self, exc_type, exc_value, traceback):
    self.package_obj.cleanup()

  def send(self, format, data):
    try:
      self.__sending_thread.add(format, data)
    except AttributeError:
      self.__start_sending()
      self.__sending_thread.add(message)

  def receive(self):
    try:
      return self.__receiving_thread.read()
    except AttributeError:
      self.__start_receiving()
      return self.__receiving_thread.read()    

  def close(self):
    self.__closing_procedure() 
    self.__exit__(self, None, None, None)

  def get_destination_port(self):
    return self.__destination_port

  def get_source_port(self):
    return self.__source_port

  def get_ip_address(self):
    try:
      return self.__ip_address
    except AttributeError:
      print ("no ip address")
      return ""

  def get_status(self):
    return self.__status

  def __start_sending(self):
    self.__sending_thread = SendingThread(self, self.__ip_address)
    self.__sending_thread.start()

  def __start_receiving(self):
    self.__receiving_thread = ReceivingThread()
    self.__receiving_thread.start()

  def __closing_procedure(self):
    pass
