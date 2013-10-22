import sys
from socket import *
from common import *
import errno

class TCPSender:
    
    rwnd = RWND_INIT
    send_base = INIT_SEQ_NUM
    next_seq_num = INIT_SEQ_NUM 
    segments = []
    
    timeout = 100 #ms
    estimatedRTT = 100 #ms
    devRTT = 0
    
    duplicate_acks = 0
    
    RTT_calculation_phase = "Ready"
    
#TODO: initialize timer and timeout
    
    def __init__(self, receiver_domain, receiver_port):
        self.connection = self.make_connection(receiver_domain, receiver_port) 
   
#------------------------------------------------------------------------------
    def udp_send(self, segment):
    
        if len(segment) is 0:
            raise Exception
        sock, domain, port = self.connection
        sock.sendto(segment, (domain, port))
        
#------------------------------------------------------------------------------
    def udp_receive(self, sock):
        try:
            return sock.recvfrom(MAX_SEGMENT_SIZE)
        except:
            return None, None        
#------------------------------------------------------------------------------
    def make_connection(self, target_domain, target_port):
        my_socket = socket(AF_INET, SOCK_DGRAM)
        my_socket.setblocking(0)
        return my_socket, target_domain, target_port
            #------------------------------------------------------------------------------    
    def update_timeout(self, sampleRTT):
        self.estimatedRTT = 0.875*self.estimatedRTT + 0.125*sampleRTT
        self.devRTT = 0.75*self.devRTT + 0.25*abs(sampleRTT - self.estimatedRTT)
        self.timeout = self.estimatedRTT + 4*self.devRTT
        print "timeout: ", self.timeout
        
#------------------------------------------------------------------------------
    def handle_ack(self, segment):
        
        ack = get_ack(segment)
        if ack < self.send_base:
            return
        
        if ack == self.send_base:
            self.duplicate_acks += 1
            if self.duplicate_acks >= 3:
                self.retransmit(byte_to_id(self.send_base))
                self.duplicate_acks = 0
                
                self.RTT_calculation_phase = "Ready"
            return        
        
        if (self.RTT_calculation_phase == ack):
            sampleRTT = current_time() - self.RTT_start
            self.update_timeout(sampleRTT)
            self.RTT_calculation_phase = "Ready"

        self.duplicate_acks = 0
        self.send_base = ack
        self.rwnd = get_rwnd(segment)
     
#------------------------------------------------------------------------------
    def handle_timeout(self):
        first_id_unacked = byte_to_id(self.send_base)

        self.retransmit(first_id_unacked)

#------------------------------------------------------------------------------
    def send_segment(self, idx, is_termination):
        msg_type = 1 if is_termination else 0
        segment = build_segment(self.next_seq_num, 0, 
            RWND_INIT, msg_type, self.data[idx])
        self.segments[idx] = segment
        
        self.udp_send(segment)
        self.next_seq_num += len(self.data[idx])
        
        current = current_time()
        self.timer[idx] = current + self.timeout
        
        if self.RTT_calculation_phase == "Ready":
            self.RTT_start = current
            self.RTT_calculation_phase = self.next_seq_num
        
#------------------------------------------------------------------------------
    def retransmit(self, idx):
        self.udp_send(self.segments[idx])
        
        timer = current_time() + self.timeout
        end = byte_to_id(self.next_seq_num)
        self.timer[idx:end] = [timer] * (end - idx)
               
#------------------------------------------------------------------------------
    def run(self, data):
        self.data = data 
        self.count = len(data)
        self.segments = [''] * self.count 
        self.timer = [inf()] * self.count
        
        end_at = sum([len(x) for x in data]) + INIT_SEQ_NUM
        idx = 0

        print end_at, self.send_base
        while self.send_base < end_at:
            segment, _ = self.udp_receive(self.connection[0])
            timer = self.timer[byte_to_id(self.send_base)]
            sofar = self.next_seq_num - self.send_base 

            if segment and is_ack(segment):
                self.handle_ack(segment)
            elif current_time() >= timer:
                self.handle_timeout()
            elif idx < self.count and sofar + len(self.data[idx]) <= self.rwnd:
                self.send_segment(idx, idx == self.count - 1)
                idx += 1
#------------------------------------------------------------------------------
def main(filename, receiver_domain, receiver_port):
    sender = TCPSender(receiver_domain, receiver_port)

    with open(filename) as my_file:
        data = list(iter(lambda: my_file.read(MSS), ''))
    sender.run(data)
#------------------------------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
