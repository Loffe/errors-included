import gtk

class Main:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Hello world!")
        window.set_default_size(1000,400)
        window.connect("destroy", gtk.main_quit, "WM destroy")
        vbox = gtk.VBox()
        window.add(vbox)
        self.button = gtk.Button("Start")
        self.button.connect("clicked", self.print_hi)
        vbox.pack_start(self.button, False)
        window.show_all()
        
    def print_hi(self, w):
        print "hello world"

Main()
gtk.main()