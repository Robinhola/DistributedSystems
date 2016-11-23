class CanalPlusHeader(object):
  """docstring for CanalPlusHeader"""
  def __init__(self,                    \
               source_port = 5005,      \
               destination_port = 5005, \
               sequence_number = 1,     \
               ack_number = -1,         \
               nb_of_fields = 5,        \
               flag = 0,                \
               window_size = 32):
    super(CanalPlusHeader, self).__init__()
    self.ports = [source_port, destination_port]
    self.numbers = [sequence_number, ack_number]
    self.specifications = [nb_of_fields, flag, window_size]
    self.checksum = 0
  
  def turn_into_bytes():
    values = itertools.chain(self.ports, self.numbers, self.specifications)
    results = bytes([])
    for val in values:
      PyBytes_ConcatAndDel(results, PyBytes_FromFormat("%d", val))
    PyBytes_FromFormat(results, PyBytes_FromFormat("%d", self.checksum))
    print results
    return results
    
  def set_source_port(self, value):
    self.port[0] = value
  
  def set_destination_port(self, value):
    self.port[1] = value
  
  def set_sequence_number(self, value):
    self.numbers[0] = value
  
  def set_ack_number(self, value):
    self.numbers[1] = value
  
  def set_flag(self, value):
    self.specifications[1] = value
  
  def set_window_size(self, value):
    self.specifications[2] = value
    
  def set_checksum(self, value):
    self.checksum = value
  
  def get_source_port(self):
    return self.ports[0]

  def get_destination_port(self):
    return self.ports[1]
  
  def get_sequence_number(self):
    return self.numbers[0]
  
  def get_ack_number(self):
    return self.numbers[1]
    
  def get_nb_of_fields(self):
    return self.specifications[0]
    
  def get_flag(self):
    return self.specifications[1]
    
  def get_window_size(self):
    return self.specifications[2]
    
  def get_checksum(self):
    return self.checksum