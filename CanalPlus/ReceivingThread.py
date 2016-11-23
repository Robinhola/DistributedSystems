class ReceivingThread(threading.Thread):
def __init__(self, int buffer_size):
        super(ReceivingThread, self).__init__()
        self.messages_to_ack = []
        self.receiving_buffer = queue()
        self.buffer_size = buffer_size

    def run(self):
      while True:
        if self.buffer_is_full():
          self.send_signal_buffer_full()
        if self.new_message_received():
          self.handle_new_message()
        message = self.pop_next_message();
        if not message.get_ack_status():
        if message.time_since_last_try_not_short():
                message.try_to_send()
            self.append_to_messages_to_ack_list(message)
        else:
            self.remove_message(message)

    def send_signal_buffer_full(self):
      pass

    def new_message_received(self):
      return len(receiving_buffer) > 0

    def handle_new_message(self):
      Message message = self.receiving_buffer.pop()
      self.append_to_messages_to_ack_list(message) 
      pass

    def pop_next_message(self):
      return messages_to_ack.pop()

    def append_to_messages_to_ack_list(self, message):
      self.messages_to_ack.append(message)

    def remove_message(self, message):
      message.delete()