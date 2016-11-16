# encoding: utf-8
import threading
import time

class SendingThread(threading.Thread):
    def __init__(self, connection, ip_address):
        super(SendingThread, self).__init__()
        self.target_ip_address = ip_address
        self.connection = connection
        self.ack_queue = Queue() 
        self.send_queue = 
        self.ack_receiving_thread = ReceivingAckThread(self.ack_queue)
        
    def run(self):
        # init
        self.ack_receiving_thread.start()
        establish_connection(self)
        # loop
        while self.connection.status == "established":
            if has_message_to_process() and target_buffer_not_full():
                send_next_message()
            else:
                # wait
        # closing

    def add():
        return


class ReceivingThread(threading.Thread):
    def run(self):
        return


def closing_procedure():
    return


class ReceivingAckThread(threading.Thread):
    def __init__(self, ack_queue):
        super(ReceivingAckThread, self).__init__()
        self.queue = ack_queue