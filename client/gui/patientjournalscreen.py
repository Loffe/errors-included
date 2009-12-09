# -*- coding: utf-8 -*-

import gtk
import map.mapdata
import shared.data
import gui
import pango
import datetime
import gobject
from selectunit import SelectUnitButton
from selectunit import SelectUnitDialog
from shared.data import JournalRequest
import config

class PatientJournalScreen(gtk.ScrolledWindow, gui.Screen):
    '''
    The screen in which you create a new 
    '''
   # the entries
    to_entry = None
    subject_entry = None
    message_entry = None
    db = None


    def __init__(self, db, queue):
        '''
        Constructor. Create the alarmscreen and its entries.
        '''
        gtk.ScrolledWindow.__init__(self)
        self.db = db
        self.queue = queue

        # set automatic horizontal and vertical scrolling
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        
        # method used internally to create new entries
        def new_entry(labeltext, parent):
            hbox = gtk.HBox(True,0)
            label = gtk.Label(labeltext)
            label.set_alignment(0, 0.5)
            entry = gtk.Entry()
            entry.set_max_length(300)
            entry.set_text("")
            entry.select_region(0, len(entry.get_text()))
            hbox.add(label)
            hbox.add(entry)
            parent.add(hbox)
            return (label, entry)

        vbox = gtk.VBox(False,0)
        self.add_with_viewport(vbox)
        label, self.why_entry = new_entry("Varför",vbox)
        label, self.ssn_entry = new_entry("Personnummer",vbox)

        self.show_all()
       
    def ok_button_function(self, event):
        data = JournalRequest(self.why_entry.get_text(),
                              self.ssn_entry.get_text(), config.client.name)
        self.db.add(data)
#        text = shared.data.PatientJournalMessage(why_entry=unicode(self.why_entry2.get_text()), 
#                                       social_security_number=unicode(self.social_security_number2.get_text()),
#                                       timestamp=datetime.datetime.now(),
#                                       units=units, 
#                                       sender=config.client.name
#                                       ) 
        self.emit("okbutton_clicked_PatientJournalScreen")
        
gobject.type_register(PatientJournalScreen)
gobject.signal_new("okbutton_clicked_PatientJournalScreen", PatientJournalScreen, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
