import sys

def generate(size):
  x = 1
  sum = 0
  while 1:
    newbytes = len(str(x)) + 1
    if sum + newbytes <= size:
      print x
      sum += newbytes
      if sum == size:
        return sum
      x += 1
    else:
      break
  print str(x)[:size - sum - 1]
  sum = size
  return sum

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print >> sys.stderr, 'Usage: python generate-test-file.py size-in-bytes'
    sys.exit(1)
  size = int(sys.argv[1])
  sum = generate(size)
  print >> sys.stderr, sum , 'bytes generated'
  sys.exit(0)
