#!/usr/bin/env python
# coding: utf-8
from shared.util import getLogger
log = getLogger("client.log")
log.debug("main imported log")
import clientgui
import controller
import qosmanager
import threading

# den här borde skapa nya vyer av mission och kartan
if __name__ == "__main__":
    log.debug("__main__")
    app = clientgui.ClientGui()
    threading.Thread(target=app.run()).start()
    
    qos = qosmanager.QoSManager()
    threading.Thread(target=qos.start()).start()
    
    controller = controller.ClientController()
    threading.Thread(target=controller.run()).start()