#!/usr/bin/env python

import shared.queue
import config

if __name__ == "__main__":
    q = shared.queue.Queue(config.server.ip,config.server.port)

    for i in range(3):
        q.enqueue("hejsan" + str(i))

    try:
        q.mainloop()
    except KeyboardInterrupt:
        q.running = False
        del q
        print "Aborting"
