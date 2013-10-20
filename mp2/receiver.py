import sys
from socket import *
from common import *

class TCPReceiver:

    def __init__(self, port):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(('', port))
        
    def run(self):
        count = 0
        while True:
            segment, self.sender_address = udp_receive(self.sock)
            count += len(get_data(segment))
            print get_data(segment), '**', count , '**' 



def main(port, loss_pattern):
    receiver = TCPReceiver(port)
    receiver.run()
            
if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2])
