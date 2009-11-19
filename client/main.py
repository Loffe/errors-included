#!/usr/bin/env python
# coding: utf-8

from shared.util import getLogger
log = getLogger("client.log")
log.debug("main imported log")
import clientgui

# Start up the client!
if __name__ == "__main__":
    log.debug("__main__")

    # Create and run GUI
    gui = clientgui.ClientGui()
    gui.run()
