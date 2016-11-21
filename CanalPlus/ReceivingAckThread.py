class ReceivingAckThread(threading.Thread):
    def __init__(self, ack_queue):
        super(ReceivingAckThread, self).__init__()
        self.queue = ack_queue