import gtk
import time
from threading import Thread
import gobject

class Main:
    counter = 0
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

        self.button3 = gtk.Button("Nothing")
        vbox.pack_start(self.button3, False)

        window.show_all()
        
    def print_hi(self, w):
        print "hello world", self.counter
        Thread(target=self.run).start()

    def run(self):
        time.sleep(2)
        self.counter += 1
        gobject.idle_add(self.button.set_label,  "Yess: " + str(self.counter))
        print "Hello thread", self.counter

Main()
gtk.main()
