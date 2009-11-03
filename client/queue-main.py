#!/usr/bin/env python

import queue
import config

if __name__ == "__main__":
    q = queue.Queue(config.server.ip,config.server.port)

    for i in range(10):
        q.enqueue("hejsan" + str(i))

    try:
        q.mainloop()
    except KeyboardInterrupt:
        q.running = False
        del q
        print "Aborting"

