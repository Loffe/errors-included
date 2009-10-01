'''
Created on Sep 25, 2009

@author: markr471
'''

import gtk

class Wagh:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("hej")
        window.set_default_size(500,400)


        window.connect("destroy", gtk.main_quit)
        vbox = gtk.VBox()


        window.add(vbox)
        self.button = gtk.Button("Start")
        self.button.connect("clicked", self.hej)
        vbox.pack_start(self.button, False)
        window.show_all()
        
        
    def hej(self, w):
        print "hej"   
        
Wagh()
gtk.main()     
    