import gtk
import pygtk
pygtk.require('2.0')
class Main:
    
    def enter_callback(self, widget, handelse):
        handelse_text = handelse.get_text()
        print "Entry contents: %s\n" % handelse_text
  
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Skapa uppdrag")
        window.set_default_size(500,400)
        window.connect("destroy", gtk.main_quit)
 
        
        vbox = gtk.VBox()
        window.add(vbox)
        handelse = gtk.GtkEntry(50)
        handelse.connect("activate", self.enter_callback, handelse)
        handelse.set_text("hello")
        handelse.select_region(0, len(handelse.get_text()))
        vbox.pack_start(handelse, gtk.TRUE, gtk.TRUE, 0)
        handelse.show()

        self.button = gtk.Button("Skapa Uppdrag")
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