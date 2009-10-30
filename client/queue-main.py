#!/usr/bin/env python

import queue

if __name__ == "__main__":
    q = queue.Queue()
    q.connect_to_server("localhost",50000)

    try:
        q.mainloop()
    except KeyboardInterrupt:
        q.running = False
        q.close()
        print "Aborting"

