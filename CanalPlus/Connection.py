# encoding: utf-8
import sys
import threading
import time
from random import randint

class Connection(object):
    """ 
        Object can be instanced in receiving or sending mode depending on the
        presence of an argument on creation.
    """
    def __init__(self, arg = ""):
        super(Connection, self).__init__()
        self.status = "closed"
        if arg == "":
            self.start_receiving()
        else:
            self.IP_address = arg
            self.start_sending()
            
    # unknown behavior
    def __exit__(self, exc_type, exc_value, traceback):
        self.package_obj.cleanup()

    def closing_procedure():
        return

    def close():
        self.closing_procedure() 
        __exit__(self, exc_type, exc_value, traceback)

    def start_sending():
        self.sending_thread = ReceivingThread()
        self.sending_thread.start()

    def send(message):
        try:
            self.sending_thread.add(message)
        except AttributeError:
            self.start_sending()
            self.sending_thread.add(message)

    def start_receiving():
        self.receiving_thread = ReceivingThread()
        self.receiving_thread.start()

    def receive():
        message = ""
        try:
            self.receiving_thread.read(message)
        except AttributeError:
            self.start_receiving()
            self.receiving_thread.read(message)
        return message