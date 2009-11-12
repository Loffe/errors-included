from shared.data import *
from shared.util import getLogger
log = getLogger("server.log")

class MessageHandler:
    server = None
    def __init__(self, server):
        self.server = server

    def handle(self, msg):
        if msg.type == MessageType.login:
            log.info("%s is logging in" % msg.sender)
            if msg.unpacked_data["password"] == "prydlig frisyr":
                self.login_allow(msg.sender)
            else:
                self.login_deny(msg.sender)
        else:
            log.info("Got unhandled message type")

    def login_allow(self, sender):
        pass

    def login_deny(self, sender):
        pass
