import gtk

import gui

class TestScreen(gtk.Label, gui.Screen):

    def __init__(self):
        gtk.Label.__init__(self)
        self.set_label("Test")
