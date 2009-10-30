#!/usr/bin/env python

import queue

if __name__ == "__main__":
    q = queue.Queue()
    q.connect_to_server("localhost",50000)

    for i in range(10):
        q.enqueue("hejsan" + str(i))

    try:
        q.mainloop()
    except KeyboardInterrupt:
        q.running = False
        q.close()
        print "Aborting"

