import gtk
import pango
from gui import Screen 

class NotificationScreen(gtk.HBox, Screen):
    
    def __init__(self):
        gtk.HBox.__init__(self, False, 0)
        self.left_label = gtk.Label("Team Med Fel")
        self.left_label.set_alignment(0,0)
        self.left_label.modify_font(pango.FontDescription("sans 14"))
        self.left_label.show()
        self.pack_start(self.left_label,True)
        self.right_label = gtk.Label("Offline")
        self.right_label.set_alignment(1,0)
        self.right_label.modify_font(pango.FontDescription("sans 14"))
        self.right_label.show()
        self.pack_start(self.right_label, False)
        
    def set_label(self, text):
        self.left_label.set_label(text)
    
    def set_right_label(self, text):
        self.right_label.set_label(text)
    
    def update_label(self, service_level):
        if service_level == "mega-low" or service_level == "ad-hoc":
            text = "Offline" 
        else:
            text = "Online"
        self.right_label.set_label(text)