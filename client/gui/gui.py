import gtk

class Screen(gtk.Widget):
    name = "Screen"
    def __init__(self, name):
        self.name = name