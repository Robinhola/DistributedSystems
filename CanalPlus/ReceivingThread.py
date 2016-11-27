class ReceivingThread(threading.Thread):
def __init__(self, connection ,buffer_size = 35):
        super(ReceivingThread, self).__init__()
        self.receiving_buffer = queue()

    def run(self):
      while True:
        self.receive()
        for message in self.receiving_buffer:
          if self.message_needs_ack(message):
            self.send_ack(message)
            self.add_message_to_set(message)
          else:
            seq = self.validate_ack(message)
            data = self.pop_message_from_set(seq)
            self.treat_data(data)

    def send_signal_buffer_full(self):
      pass

    def receive(self):
      socket.recvfrom_into(self.receiving_buffer)

    def message_needs_ack(self, message):
      pass
      
    def send_ack(self, message):
      pass
      
    def add_message_to_set(self, message):
      pass

    def validate_ack(self, message):
      pass

    def pop_message_from_set(self, seq):
      data = ''
      return data
      
    def treat_data(self, data):
      pass

