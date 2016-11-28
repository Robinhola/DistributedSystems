class ReceivingThread(threading.Thread):
def __init__(self, connection ,buffer_size = 35):
        super(ReceivingThread, self).__init__()
        self.connection = connection
        self.receiving_buffer = queue()
        self.messages_to_ack = {}
        
    def run(self):
      while True:
        self.receive()
        for message in self.receiving_buffer:
          if self.message_needs_ack(message):
            self.send_ack(message)
            if self.contains_data(message):
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

    def send_ack(self, message, ack_type = ""):
      seq, ack = self.gather_seqack(message)
      ack_message = Message("", "", 
                            ack_type + "ACK", 
                            ack, 
                            seq + 1, 
                            self.connection)
      UDP_IP = self.connection.get_ip_address()
      UDP_PORT = self.connection.get_destination_port()
      self.sock.sendto(str(message.content), (UDP_IP, UDP_PORT)) # BYTES ??

    def gather_seqack(self, message):
      seq = 0
      ack = 0
      return seq, ack

    def add_message_to_set(self, message):
      pass

    def validate_ack(self, message):
      pass

    def pop_message_from_set(self, seq):
      data = ''
      return data

    def treat_data(self, data):
      pass

