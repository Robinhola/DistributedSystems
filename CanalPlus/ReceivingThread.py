class ReceivingThread(threading.Thread):
def __init__(self, connection ,buffer_size = 35):
        super(ReceivingThread, self).__init__()
        self.receiving_buffer = queue()

    def run(self):
      while True:
        self.receive()
        for message in self.receiving_buffer:
          if (self.has_ack_number(message) and self.demands_ack(message)):
            self.send_corresponding_ack(message)
          else:
            self.send_new_ack(message)

    def send_signal_buffer_full(self):
      pass

    def receive(self):
      socket.recvfrom_into(self.receiving_buffer)

    def has_ack_number(self, message):
      pass

    def demands_ack(self, message):
      pass

    def send_corresponding_ack(self, message):
      pass

    def send_new_ack(self, message):
      pass

