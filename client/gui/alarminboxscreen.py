# coding: utf-8

import gtk
import map.mapdata
import shared.data
import gui
import pango

class AlarmInboxScreen(gtk.ScrolledWindow, gui.Screen):
    '''
    The screen wich shows your messages
    '''

    def __init__(self, db):
        '''
        Constructor.
        '''
        gtk.ScrolledWindow.__init__(self)

        # set automatic horizontal and vertical scrolling
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        meddelande = gtk.Label("Du har inget larm atm!")
        self.add_with_viewport(meddelande)

 
