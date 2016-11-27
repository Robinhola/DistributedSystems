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
    if len(sys.argv) != 5:
      print("Purrfect usage : python purrfect.py protocol IP pingperiod timeout\n")
      sys.exit(-1)

    self.protocol = (str(sys.argv[1])).upper()
    if self.protocol != "TCP" and "C+" != self.protocol:
      print("Protocol must be TCP or C+\n")
      sys.exit(-1)

    self.ip_address = str(sys.argv[2])
    if not self.__is_valid_ipv4_address(self.ip_address):
      print("IP " + str(sys.argv[2]) + " is not valid\n")
      sys.exit(-1)

    try:
      self.pingperiod = int(sys.argv[3])
      self.timeout = int(sys.argv[4])
    except ValueError:
      print "Pingperiod / timeout must be unsigned integers"
      sys.exit(-1)
    if self.pingperiod <= 0 or self.timeout <= 0:
      print "Pingperiod / timeout must be unsigned integers"
      sys.exit(-1)

  def detect(self):
    if self.protocol == "TCP":
      self.detect_TCP()
    elif self.protocol == "C+":
      self.detect_CPlus()
    else:
      raise ValueError("Protocol should be TCP or C+")

  def detect_TCP(self):
    self.establish_connection()
    self.create_purrfect_detector_thread()
    self.run_purrfect_dector_thread()
    while True:
      time.sleep(1)


  def detect_CPlus(self):
    raise NotImplementedError("Purrfect over CanalPlus is not quite ready")







cat = Purrfect()
cat.parse_args()
cat.detect()
