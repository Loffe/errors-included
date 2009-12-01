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

        self.name = None
        gtk.ScrolledWindow.__init__(self)
        # set automatic horizontal and vertical scrolling
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        self.db = db
#        self.units = self.db.get_all_units()
        self.vbox = gtk.VBox(False,0)
        self.buttons = []
        self.add_with_viewport(self.vbox)
        
    def select_contacts(self, event):
        for button in self.buttons:
            if button != event:
                button.set_active(False)
            else:
                self.name = button.get_label()
