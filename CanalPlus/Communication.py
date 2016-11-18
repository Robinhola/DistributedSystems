# encoding: utf-8
import threading
import time

class SendingThread(threading.Thread):
    def __init__(self, connection, ip_address):
        super(SendingThread, self).__init__()
        self.target_ip_address = ip_address
        self.connection = connection
        self.sending_list = []
        self.ack_array = []
        self.linking_dict = {}

    def run(self):
        self.start_receiving_acks(self)
        self.establish_connection(self)
        while self.connection.status == "established":
            if self.has_message_to_process() and self.target_buffer_not_full():
                self.send_next_message()
            else:
                continue
        self.handle_connection_ending()

    def add(self, message):
        self.add_to_send_list(message)
        self.add_to_ack_array(message)
        self.link_message_to_id(message)
    
    def send_next_message(self):
        message = self.pop_next_message();
        if not message.has_been_sent():
            if message.time_since_last_try_not_short():
                message.try_to_send()
            self.append_to_sending_list(message)
        else:
            self.remove_message(message)
            message.delete()

    def start_receiving_acks(self):
        self.ack_receiving_thread = ReceivingAckThread(self.ack_queue)
        self.ack_receiving_thread.start()

    def establish_connection():
        pass

    def has_message_to_process():
        pass

    def target_buffer_not_full():
        pass

    def handle_connection_ending():
        pass

    def add_to_send_list(message):
        pass
        
    def add_to_ack_array(message):
        pass

    def link_message_to_id(message):
        pass

    def pop_next_message():
        pass

    def append_to_sending_list():
        pass

    def remove_message(message):
        pass


class ReceivingThread(threading.Thread):
    def run(self):
        return


def closing_procedure():
    return


class ReceivingAckThread(threading.Thread):
    def __init__(self, ack_queue):
        super(ReceivingAckThread, self).__init__()
        self.queue = ack_queue