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
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        self.db = db
        units = self.db.get_all_units()
        vbox = gtk.VBox(False,0)
        for u in units:
            unit_button = gtk.ToggleButton("%s (%d)" % (u.name, u.id))
            unit_button.show()
            self.vbox.pack_start(unit_button)
            self.buttons[u.id] = unit_button

        # set automatic horizontal and vertical scrolling
        

 
