#!/usr/bin/env python

import shared.clientnetworkhandler
import config
import sys

if __name__ == "__main__":
    if "stop" in sys.argv:
        import dbus
        bus = dbus.SessionBus()
        remote_object = bus.get_object("included.errors.Client", "/Queue")
        remote_object.dbus_close()
        sys.exit(0)

    q = shared.clientnetworkhandler.ClientNetworkHandler(config.server.ip,config.server.port)

    try:
        q.mainloop()
    except KeyboardInterrupt:
        q.running = False
        del q
        print "Aborting"
