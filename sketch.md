Object CanalPlus ([IP who])

    Parameters:
      Connection connection ([IP who])
    
    Methods:
      send
      receive
      
Object Connection ([IP who])
    
    Parameters:
      int status

    Methods:
      check
      terminate
      
    Private methods:
      create

Object Message (type = 'data')

    Parameters:
        self.type = type
        self.id = '1234' + 'time'
        self.ack_number = -1
        self.ack_status = False
        self.time_since_last_try = 0
        self.content = []               == CanalPlusHeader.to_bytes() + Data 
    Methods:
        def add_content(self, content):
        def get_id(self):
        def set_ack_number(self, ack_number):
        def get_ack_number(self):
        def wrapping(self)
        def get_ack_status(self):
        def has_been_received(self):
        def time_since_last_try_not_short(self):
        def try_to_send(self):
    Private methods:
    
Object CanalPlusHeader (int source_port,
                            destination_port, 
                            sequence_number, 
                            ack_number, 
                            nb_of_data, 
                            flag, 
                            window_size
                    [, int* options])

    Parameters:
        int* port = [source_port, destination_port]
        int sequence_number
        int ack_number =    # if ack flag is present, this the expected next sequence_number
        int* specifications = [nb_of_data, flag, window_size]
        int checksum
        int* options = ** if nb_of_data > 5
    Methods:
        bytes object to_bytes(self):
            if self.nb_of_data == 5:
                return PyBytes_FromFormat(%d, self.paramaters - self.options)
            else if self.nb_of_data > 5:
                return PyBytes_FromFormat(%d, self.paramaters)
            else:
                return null
                
