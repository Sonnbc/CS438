import sys
from socket import *
from common import *

class TCPReceiver:

    acked = INIT_SEQ_NUM
    
    def __init__(self, port):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(('', port))
    
    def send_ack(self, ack):
        segment = build_segment(0, self.acked, 2500, 1)
        self.sock.sendto(segment, self.sender_address)
        
    def run(self):
        count = 0
        while True:
            segment, self.sender_address = self.sock.recvfrom(MAX_SEGMENT_SIZE)
            
            count += len(get_data(segment))
            my_data =get_data(segment)
            print my_data, '**', count , '**'
            
            seqnum = get_seqnum(segment)
            if seqnum == self.acked:
                self.acked = seqnum + len(get_data(segment))
                #print self.acked
                self.send_ack(self.acked)
            elif seqnum > self.acked:
                self.send_ack(self.acked)    
            

def main(port, loss_pattern):
    receiver = TCPReceiver(port)
    receiver.run()
            
if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2])
