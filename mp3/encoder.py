import sys
from random import randrange
from timeit import Timer
from math import pow

def encode(g, k, d, r=3):
    R = 0
    d = d<<r
    for i in xrange(k+r, 0 , -1):
        R = (R<<1) + (d>>(i-1) &1)
        if R < g:
            continue
        R = R^g
        
    return R
             
def encode_loop(g, k, inputs):
    for d in inputs:
        encode(g, k, d)
        
def lookup_loop(crc_table, inputs):        
    for d in inputs:
        crc_table[d]
                  
if __name__ == "__main__":
    if len(sys.argv) is 4:
        g, k, d = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
        R = encode(g, k, d)
        print format(R, '03b')
        
    elif len(sys.argv) is 2:
        g = int(sys.argv[1])
        N = 100000
        kr = 8 + 3
        crc_table = [encode(g, kr, dR, 0) for dR in xrange(0, 1<<kr)]
        received = [randrange(1, 1<<kr) for _ in xrange(N)]
        
        for p in [0.1, 0.2, 0.3]:
            p_detected, p_error, cnt_correct = 0, 0, 0
            for dR in received:
                num_error = bin(dR).count('1')    
                p_this = pow(p, num_error) * pow(1-p, kr-num_error)
                
                p_error += p_this
                if crc_table[dR] != 0:
                    p_detected += p_this
            
            print 'p=', p, 'prob. of detection in case of error=', p_detected / p_error
    else:
        g = int('1001', 2)
        N = 100000
        k = 16
        
        crc_table = [encode(g, k, d) for d in xrange(0, 1<<k)]
        inputs = [randrange(1<<k) for _ in xrange(N)]
        
        t1 = Timer(lambda: encode_loop(g, k, inputs))
        print 'average encoding:', t1.timeit(number=1) / N
        
        t2 = Timer(lambda: lookup_loop(crc_table, inputs))
        print 'average lookup:', t2.timeit(number=1) / N

