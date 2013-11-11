import sys

def generate(size):
  x = 1
  sum = 0
  while 1:
    print x
    sum += len(str(x)) + 1
    if sum >= size:
      return sum
    x += 1

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print >> sys.stderr, 'Usage: python test.py size-in-bytes'
    sys.exit(1)
  size = int(sys.argv[1])
  sum = generate(size)
  print >> sys.stderr, sum , 'bytes generated'
  sys.exit(0)
