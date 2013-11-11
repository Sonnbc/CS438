import sys
from socket import *
from common import *
import errno
from math import ceil

class TCPSender:
    
    def __init__(self, receiver_domain, receiver_port):
        self.connection = self.make_connection(receiver_domain, receiver_port) 
        self.time_origin = current_time()
        
        self.rwnd = RWND_INIT
        self.send_base = INIT_SEQ_NUM
        self.next_seq_num = INIT_SEQ_NUM 
        self.segments = []
        
        #TODO: initialize timer and timeout???
        self.timeout = 100 #ms
        self.estimatedRTT = 100 #ms
        self.devRTT = 0
        
        self.duplicate_acks = 0
        
        self.RTT_calculation_phase = "Ready"
        
        self.cwnd = MSS
        self.ssthresh = 1000
        self.congestion_phase = SLOW_START

        self.time_origin = current_time() # when we started
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
        #print "timeout: ", self.timeout
        
#------------------------------------------------------------------------------
    def handle_ack(self, segment):
        
        ack = get_ack(segment)
        if ack < self.send_base:
            return
        
        if ack == self.send_base:
            self.duplicate_acks += 1
            if self.congestion_phase == FAST_RECOVERY:
                self.cwnd += MSS
            if self.duplicate_acks >= 3:
                self.congestion_phase = FAST_RECOVERY
                self.ssthresh = self.cwnd / 2
                self.cwnd = self.ssthresh + 3*MSS
                print "%f, %d" % (current_time() - self.time_origin, self.cwnd)
                
                self.duplicate_acks = 0
                self.RTT_calculation_phase = "Ready"
                self.retransmit(byte_to_id(self.send_base))

            return        
        
        #new ack
        if self.congestion_phase == SLOW_START:
            self.cwnd += MSS
            if self.cwnd >= self.ssthresh:
                self.congestion_phase = CONGESTION_AVOIDANCE
        elif self.congestion_phase == CONGESTION_AVOIDANCE:
            self.cwnd += MSS*MSS/self.cwnd
        elif self.congestion_phase == FAST_RECOVERY:
            self.cwnd = self.ssthresh
            self.congestion_phase = CONGESTION_AVOIDANCE
        
        print "%f, %d" % (current_time() - self.time_origin, self.cwnd)
        
        if (self.RTT_calculation_phase == ack):
            sampleRTT = current_time() - self.RTT_start
            self.update_timeout(sampleRTT)
            self.RTT_calculation_phase = "Ready"

        self.duplicate_acks = 0
        self.send_base = ack
        self.rwnd = get_rwnd(segment)
     
#------------------------------------------------------------------------------
    def handle_timeout(self):
        self.congestion_phase = SLOW_START
        self.ssthresh = self.cwnd / 2
        self.cwnd = MSS
        self.duplicate_acks = 0
        
        print "%f, %d" % (current_time() - self.time_origin, self.cwnd)
        first_id_unacked = byte_to_id(self.send_base)
        
        #double timeout var then retransmit in case of a timeout event
        self.timeout *= 2
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
    def available_to_send(self):
        return min(self.rwnd, ceil(float(self.cwnd)/MSS)*MSS)               
#------------------------------------------------------------------------------
    def run(self, data):
        self.data = data 
        self.count = len(data)
        self.segments = [''] * self.count 
        self.timer = [inf()] * self.count
        
        end_at = sum([len(x) for x in data]) + INIT_SEQ_NUM
        idx = 0
        
        # print initial congestion window size
        print "%f, %d" % (current_time() - self.time_origin, self.cwnd)

        while self.send_base < end_at:
            segment, _ = self.udp_receive(self.connection[0])
            timer = self.timer[byte_to_id(self.send_base)]
            sofar = self.next_seq_num - self.send_base
            if segment and is_ack(segment):
                self.handle_ack(segment)
            elif current_time() >= timer:
                self.handle_timeout()
            elif ( idx < self.count 
            and sofar+len(self.data[idx]) <= self.available_to_send() ):
                self.send_segment(idx, idx == self.count - 1)
                idx += 1
#------------------------------------------------------------------------------
def main(filename, receiver_domain, receiver_port):
    with open(filename) as my_file:
        data = list(iter(lambda: my_file.read(MSS), ''))
    sender = TCPSender(receiver_domain, receiver_port)
    sender.run(data)
#------------------------------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
