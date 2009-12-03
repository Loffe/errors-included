# -*- coding: utf-8 -*-

import gtk
import gobject
import map.mapdata
import shared.data
import datetime
import gui
import pango



class Activities(gtk.ScrolledWindow, gtk.VBox):
    
    
    

    def __init__(self, db):
        '''
        Constructor. Create the statusscreen and its entries.
        '''
        gtk.ScrolledWindow.__init__(self)
        self.db = db 

        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        vbox = gtk.VBox(False,0)
        self.add_with_viewport(vbox)
        
        
        
        choose_units_button = gtk.Button("Svar")
        choose_units_button2 = gtk.Button("upptagen")
        #choose_units_button.connect("clicked", self.select_units)
        #choose_units_button2.connect("clicked"), self.select_units)
        vbox.add(choose_units_button)
        vbox.add(choose_units_button2)