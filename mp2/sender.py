import sys
from socket import *
from common import *
import errno

class TCPSender:

    self.last_byte_sent = 0
    self.last_byte_acked = 0

    self.send_base = INIT_SEQ_NUM
    self.next_seq_num = INIT_SEQ_NUM

#TODO: initialize timer and timeout
    
    def __init__(receiver_domain, receiver_port):
        self.connection = self.make_connection(receiver_domain, receiver_port)    
   
#------------------------------------------------------------------------------
    def udp_send(self, segment):
        sock, domain, port = connection
        sock.sendto(data, (domain, port))
#------------------------------------------------------------------------------
    def udp_receive(self):
        sock, _, _ = connection
        try:
            return sock.recvfrom(MSS)
        except:
            return None
#------------------------------------------------------------------------------
    def make_connection(self, target_domain, target_port):
        my_socket = socket(AF_INET, SOCK_DGRAM)
        my_socket.setblocking(0)
        return my_socket, target_domain, target_port
#------------------------------------------------------------------------------    
    def handle_ack(self, segment):
        
        ack = segment.get_ack()
        if ack <= self.send_base:
            return
        
        acked_id = byte_to_id(ack - 1)
        
        self.send_base = ack
        self.last_byte_acked = ack - 1
        
        if last_byte_sent > last_byte_acked:
            timer = sent_time[acked_id + 1] + timeout
#------------------------------------------------------------------------------
    def handle_timeout(self):
        first_byte_unacked = last_byte_acked + 1
        first_id_unacked = byte_to_id(first_byte_unacked)
        transmit(first_id_unacked)

#------------------------------------------------------------------------------
    def transmit_segment(self, idx):
        segment = self.build_segment(idx) #header + data[idx]
        self.udp_send(segment)
        
        last_byte_sent = id_to_max_byte(idx)
        
               
#------------------------------------------------------------------------------    
    def run(self, data):
        self.data = data
        while True:
            ack = udp_receive(connection)
            if ack:
                handle_ack(ack)
            elif current_time() >= timer:
                handle_timeout()
            elif has_data()
                send()  
#------------------------------------------------------------------------------    
def main(filename, receiver_domain, receiver_port):
    sender = TCPSender(receiver_domain, receiver_port)

    with open(filename) as my_file:
        data = list(iter(lambda: my_file.read(MSS), ''))
    sender.run(data)
#------------------------------------------------------------------------------    
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
