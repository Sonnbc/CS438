
import sys

def checksum(words, w):
    ssum = words[0]
    mask = 2 ** w - 1
    for word in words[1:]:
        ssum += word
        #print ssum
        if ssum > mask:
            ssum = (ssum & mask) + 1
            # print ">>", ssum
    csum = ssum ^ mask
    return csum

def read_words(n, base, fin):
    done = 0
    words = []
    while done < n:
        text = fin.readline()[:-1]
        tokens = text.split(' ')
        for token in tokens:
            try:
                words.append(int(token, base))
                done += 1
            except: # can not parse
                continue
    return words

if __name__ == '__main__':
    nwords = 8
    wordsize = 16
    base = 10
    words = read_words(nwords, base, sys.stdin)
    print checksum(words, wordsize)

