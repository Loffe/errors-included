import gtk

class Main:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Hello world!")
        window.set_default_size(500,400)
        window.connect("destroy", gtk.main_quit)
        vbox = gtk.VBox()
        window.add(vbox)
        self.button = gtk.Button("Hello")
        self.button.connect("clicked", self.print_hi)
        vbox.pack_start(self.button, False)
        self.button2 = gtk.Button("Quit")
        self.button2.connect("clicked", gtk.main_quit)
        vbox.pack_start(self.button2, False)
        window.show_all()
        
    def print_hi(self, w):
        print "hello world"

Main()
gtk.main()