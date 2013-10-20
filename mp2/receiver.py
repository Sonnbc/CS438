import sys
from socket import *

def make_receiving_socket(port):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('', port))
    return sock
    
def receive(sock):
    while True:
        message, sender_address = sock.recvfrom(2048)
        print message,
    
def main(port, loss_pattern):
    sock = make_receiving_socket(port)
    receive(sock)
        
if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2])
