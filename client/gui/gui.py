import gtk

class Screen(gtk.Widget):
    name = "Screen"
    def __init__(self, name):
        self.name = name

    def ok_button_function(self, event):
        
        print "Default ok buttton pressed"
