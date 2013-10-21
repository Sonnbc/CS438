import time 
import math

MSS = 100    
RWND_INIT = 2500
INIT_SEQ_NUM = 1
MAX_SEGMENT_SIZE = 200

current_time = lambda: time.time() * 1000

# header format
# [sequence number, ack number, rwnd, msg_type] data
# [10,4,50,0]this is a data
# msg_type: 
#    0 for normal data, 
#    1 for connection termination (sent from sender to receiver)
#    2 for ack 


def build_segment(seqnum, ack, rwnd, msg_type, data = ''):
    return str([seqnum, ack, rwnd, msg_type]) + data

def get_header(segment):
    return eval( segment[:segment.find(']')+1] ) 

def get_data(segment):
    return segment[segment.find(']')+1:]    
    
def get_seqnum(segment):
    return get_header(segment)[0]

def get_ack(segment):
    return get_header(segment)[1]
    
def get_rwnd(segment):
    return get_header(segment)[2]
    
def is_ack(segment):      
    return get_header(segment)[3] is 2
    
def is_termination(segment):
    return get_header(segment)[3] is 1    
    
def byte_to_id(byte):
    return int(math.ceil(float(byte + INIT_SEQ_NUM - 1)/MSS)) - 1
    
def id_to_last_byte(id):
    return (id + 1)* MSS + INIT_SEQ_NUM - 1 
    
def inf():
    return float('Inf')    
    

  
        

        
        
