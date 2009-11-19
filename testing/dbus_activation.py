import select
import sys

running = True
while running:
    inputready, writeready, errorready = select.select([sys.stdin],[],[])
    print "got input"
    for s in inputready:
        if s == sys.stdin:
            print "from stdin"
            print s.readline()


print "Hello"
