import sys
from socket import *
from common import *
import errno
#------------------------------------------------------------------------------
last_byte_sent = 0
last_byte_acked = 0

send_base = INIT_SEQ_NUM
next_seq_num = INIT_SEQ_NUM

#------------------------------------------------------------------------------
def udp_send(data, connection):
    sock, domain, port = connection
    sock.sendto(data, (domain, port))
#------------------------------------------------------------------------------
def udp_receive(connection):
    sock, _, _ = connection
    try:
        return sock.recvfrom(MSS)
    except:
        return None
#------------------------------------------------------------------------------
def make_connection(target_domain, target_port):
    my_socket = socket(AF_INET, SOCK_DGRAM)
    my_socket.setblocking(0)
    return my_socket, target_domain, target_port
#------------------------------------------------------------------------------    
def handle_ack(message):
    global send_base
    
    ack = message.get_ack()
    if ack <= send_base:
        return
    
    acked_id = ack_to_id(ack)
    
    send_base = ack
    last_byte_acked = ack - 1
    
    if last_byte_sent > last_byte_acked:
        timer = sent_time[acked_id + 1] + timeout
           
#------------------------------------------------------------------------------    
def process(data, connection):
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
    connection = make_connection(receiver_domain, receiver_port)
    udp_receive(connection)
    with open(filename) as my_file:
        data = list(iter(lambda: my_file.read(MSS), ''))
    process(data, connection)
#------------------------------------------------------------------------------    
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
