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
    
    def make_ack(self, segment):
        return get_seqnum(segment) + len(get_data(segment))
        
    def run(self):
        count = 0
        packet_number = 0
        
        result = []
        received = {}
        while True:
            segment, self.sender_address = self.sock.recvfrom(MAX_SEGMENT_SIZE)
            #print "**", segment, "&&", len(segment), ">>"
            packet_number += 1
            
            #Packet should be dropped
            if self.pattern(packet_number):
                continue
             
            count += len(get_data(segment))
            seqnum = get_seqnum(segment)
            idx = byte_to_id(seqnum)
            received[idx] = segment
            
            #print idx, get_header(segment)
            
            if seqnum == self.acked:
                while idx in received:
                    result.append(get_data(received[idx]))
                    idx += 1
                
                last_segment = received[idx - 1]
                self.acked = self.make_ack(last_segment)    
                self.send_ack(self.acked)    
                
                if is_termination(last_segment):
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
