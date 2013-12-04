
import sys

def checksum(n, w, fin):
    ssum = 0
    mask = 2 ** w - 1
    for i in xrange(0, n):
        word = int(fin.readline()[:-1])
        ssum += word
        if ssum > mask:
            ssum = ssum & mask + 1
    csum = ssum ^ mask
    return csum

if __name__ == '__main__':
    print checksum(8, 16, sys.stdin)

