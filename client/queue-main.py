#!/usr/bin/env python

import queue
import config

if __name__ == "__main__":
    q = queue.Queue()
    q.connect_to_server("127.0.0.1",config.server.localport)

    for i in range(10):
        q.enqueue("hejsan" + str(i))

    try:
        q.mainloop()
    except KeyboardInterrupt:
        q.running = False
        q.close()
        print "Aborting"

