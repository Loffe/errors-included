# coding: utf-8

import gtk
import map.mapdata
import shared.data
import gui
import pango

class ContactScreen(gtk.ScrolledWindow, gui.Screen):
    '''
    The screen wich shows your messages
    '''

    def __init__(self,db):
        '''
        Constructor.
        '''
        self.ip = None
        self.name = None
        gtk.ScrolledWindow.__init__(self)
        # set automatic horizontal and vertical scrolling
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        self.db = db
        self.units = self.db.get_all_units()
        self.vbox = gtk.VBox(False,0)
        self.buttons = []
        for u in self.units:
            button = gtk.ToggleButton("%s" % u.name)
            button.show()
            self.vbox.pack_start(button)
            button.connect("pressed", self.select_contacts)
            self.buttons.append(button)
        self.add_with_viewport(self.vbox)
        
    def select_contacts(self, event):
        for button in self.buttons:
            if button != event:
                button.set_active(False)
            else:
                self.name = button.get_label()
                ip = self.get_ip(self.name)
                if ip != None:
                    self.ip = ip
                
    def get_ip(self, name):
        for unit in self.units:
            if unit.name == name:
                print "Kontaktens ip: ", unit.ip
                return unit.ip
        return None

        

 
