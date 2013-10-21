import sys
from socket import *
from common import *
import time

class TCPReceiver:

    acked = INIT_SEQ_NUM
    
    def __init__(self, port, pattern):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(('', port))
        
        self.pattern = pattern
    
    def send_ack(self, ack):
        #print "send_ack", ack
        segment = build_segment(0, self.acked, 2500, 2)
        self.sock.sendto(segment, self.sender_address)
        
    def run(self):
        count = 0
        idx = 0
        
        result = []
        received = {}
        while True:
            segment, self.sender_address = self.sock.recvfrom(MAX_SEGMENT_SIZE)
            idx += 1
            
            #Packet should be dropped
            if self.pattern(idx):
                continue
             
            #print idx, is_termination(segment), get_seqnum(segment), self.acked
            print segment
            count += len(get_data(segment))
            data = get_data(segment)
            
            seqnum = get_seqnum(segment)
            
            if seqnum == self.acked:
                self.acked = seqnum + len(data)
                self.send_ack(self.acked)
                
                result.append(data)
                
                if is_termination(segment):
                    break 
            elif seqnum > self.acked:
                self.send_ack(self.acked)
                
        #print ''.join(result)    
            

def main(port, loss_file):
    with open(loss_file) as f:
        content = [int(x) for x in f.read().split()]
        if content[0] is 1:
            pattern = lambda x: x % content[1] is 0
        elif content[0] is 2:
            pattern = lambda x: x in content[1:]
        else:
            pattern = lambda x: False
            
    receiver = TCPReceiver(port, pattern)
    receiver.run()
            
if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2])
