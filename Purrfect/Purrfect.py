# encoding utf-8

import sys
import socket
import time


# cat in 1337 speak is c47, c47 to decimal is 3147
PORT=3147

class Purrfect(object):
  def __init__(self):
    super(Purrfect, self).__init__()
    self.protocol = ""
    self.ip_address = ""
    self.pingperiod = 0
    self.timeout = 0
    self.socket = None
    self.direction = ""

  def  __is_valid_ipv4_address(self, address):
    try:
      socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
      try:
        socket.inet_aton(address)
      except socket.error:
        return False
      return address.count('.') == 3
    except socket.error:  # not a valid address
      return False

    return True

  def parse_args(self):
    if len(sys.argv) != 6:
      print("Purrfect usage : python purrfect.py direction protocol IP pingperiod timeout\n")
      sys.exit(-1)

    self.direction = str(sys.argv[1]).upper()
    if self.direction != "UP" and "DOWN" != self.direction:
      print("Direction must be up or down")
      sys.exit(-1)


    self.protocol = (str(sys.argv[2])).upper()
    if self.protocol != "TCP" and "C+" != self.protocol:
      print("Protocol must be TCP or C+\n")
      sys.exit(-1)

    self.ip_address = str(sys.argv[3])
    if not self.__is_valid_ipv4_address(self.ip_address):
      print("IP " + str(sys.argv[3]) + " is not valid\n")
      sys.exit(-1)

    try:
      self.pingperiod = int(sys.argv[4])
      self.timeout = int(sys.argv[5])
    except ValueError:
      print("Pingperiod / timeout must be unsigned integers")
      sys.exit(-1)
    if self.pingperiod <= 0 or self.timeout <= 0:
      print("Pingperiod / timeout must be unsigned integers")
      sys.exit(-1)

  def detect(self):
    if self.protocol == "TCP":
      self.detect_TCP()
    elif self.protocol == "C+":
      if self.direction == "UP":
        self.detect_CPlus_send()
      elif self.direction == "DOWN":
        self.detect_CPlus_recv()
    else:
      raise ValueError("Protocol should be TCP or C+")

  def detect_TCP(self):
    self.establish_connection()
    #self.create_purrfect_detector_thread()
    #self.run_purrfect_dector_thread()
    while True:
      time.sleep(1)

  def establish_connection(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      self.socket.connect((self.ip_address, PORT))
    except:
      print("Could not establish connection to " + str(self.ip_address) + ":" + str(PORT))
      raise


  def purrfect_detection(self):
    self.socket.send("ping")


  def detect_CPlus_send(self):
    # no work :(
    sys.path.append('../CanalPlus')
    import Connection
    connection = Connection.Connection(self.ip_address, 5005, 5006)
    while True:
      connection.send("%s", "ping")
      time.sleep(self.pingperiod / 1000)

  def detect_CPlus_recv(self):
    # Does not work
    sys.path.append('../CanalPlus')
    import Connection
    connection = Connection.Connection(self.ip_address, 5006, 5005)
    counter = 0
    while True:
      msg = connection.receive()
      if msg != "ping":
        counter += 1
      else:
        counter = 0
      if counter >= self.timeout:
        print("Distant machine is faulty! Exiting")
        sys.exit(-1000)
      time.sleep(self.pingperiod / 1000)







cat = Purrfect()
cat.parse_args()
cat.detect()
