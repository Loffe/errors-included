# coding: utf-8

#InboxScreen

import gtk
import gobject
import map.mapdata
import shared.data
import datetime
import gui
import pango
import config
from shared.data import JournalResponse


class PatientJournalMessageScreen(gtk.ScrolledWindow, gui.Screen):
    '''
    The screen in which you allow a client access to a journal
    '''
    # the entries
    db = None
    
    journals = [
            u'Kalle kamel är en häst',
            u'Freddie har en hjärnskada och behöver behandlas med lakrits och extra kaffe',
            u'DT är från Småland och därför snål.'
            ]

    def __init__(self, db):
        '''
        Constructor. Create the infoscreen and its entries.
        '''
        gtk.ScrolledWindow.__init__(self)
        self.db = db 

        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
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

        self.combo_box = gtk.combo_box_new_text()
        self.combo_box.set_size_request(300,50)
        self.combo_box.append_text("Välj patientjournalförfrågan")
        vbox.pack_start(self.combo_box, True,True, 0)
        
        label, self.why_entry = new_entry("Varför",vbox)
        label, self.ssn_entry = new_entry("Personnummer",vbox)
        
        # add event handler
        self.combo_box.connect('changed', self.select_journal)

        # set the first item added as active
        self.combo_box.set_active(0)

        # show 'em all! (:
        self.show_all()

    '''Handle events
    '''

    def select_journal(self, combobox):
        
        '''
        Call when combobox changes to switch obstacle type.
        @param combobox: the changed combobox
        '''
        # set the selected type
        selected_m = self.combo_box.get_active_text()
        for request in self.db.get_journal_requests():
            text = "varför: " + str(request.why) + "    personumer: " + str(request.ssn)
            if text == selected_m:
                self.selected_request = request
                self.why_entry.set_text(request.why)
                self.ssn_entry.set_text(request.ssn)
                break
                
    def add_request(self, event):
        print "new request added, start blinkin'!"
                
    def ok_button_function(self, event):
        req = self.selected_request
        response = JournalResponse(req.id, True, u"Därför",
                                   req.ssn, self.journals[req.id%len(self.journals)])
        self.db.add(response)
        print "OK"
    
    def no_button_function(self, event):
        req = self.selected_request
        response = JournalResponse(req.id, False, u"Därför",
                                   req.ssn, u"")
        self.db.add(response)
        print "NO"

