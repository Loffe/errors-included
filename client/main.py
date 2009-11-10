#!/usr/bin/env python
# coding: utf-8
from shared.util import log as log
log.debug("main imported log")
import clientgui

# den här borde skapa nya vyer av mission och kartan
if __name__ == "__main__":
    log.debug("__main__")
    app = clientgui.ClientGui()
    app.run()
