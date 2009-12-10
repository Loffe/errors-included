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
from shared.data import JournalResponse, JournalRequest


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
        
        def new_label(labeltext, parent):
            hbox = gtk.HBox(True,0)
            label = gtk.Label(labeltext)
            label.set_alignment(0, 0.5)
            entry = gtk.Label()
            entry.set_text("")
            hbox.add(label)
            hbox.add(entry)
            parent.add(hbox)
            return (label, entry)

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

        # create and pack combobox
        self.liststore = gtk.ListStore(str, str, str, int)
        self.combo_box = gtk.ComboBox(self.liststore)
        cell = gtk.CellRendererText()
        cell2 = gtk.CellRendererText()
        cell3 = gtk.CellRendererText()
        self.combo_box.pack_start(cell, True)
        self.combo_box.pack_start(cell2, True)
        self.combo_box.pack_start(cell3, True)
        self.combo_box.add_attribute(cell, 'text', 0)
        self.combo_box.add_attribute(cell2, 'text', 1)
        self.combo_box.add_attribute(cell3, 'text', 2)
        vbox.pack_start(self.combo_box, True, True, 0)
        
        label, self.why_label = new_label("Varför",vbox)
        label, self.ssn_label = new_label("Personnummer",vbox)
        label, self.why_entry = new_entry("Anledning",vbox)
        
        # add event handler
        self.combo_box.connect('changed', self.select_journal)

        # set the first item added as active

        # show 'em all! (:
        self.show_all()

    def update_list(self):
        self.combo_box.get_model().clear()
        self.combo_box.get_model().append(("Välj journal...","","", 0))
        for req in self.db.get_journal_requests():
            self.combo_box.get_model().append((
                "Persnr: " + req.ssn,
                "Från: " + req.sender,
                "Anledning: " + req.why,
                req.id))
        self.combo_box.set_active(0)

    '''Handle events
    '''

    def select_journal(self, combobox):
        
        '''
        Call when combobox changes to switch obstacle type.
        @param combobox: the changed combobox
        '''
        index = self.combo_box.get_active()
        if index < 1:
            return
        selected = self.liststore[index]
        selected_id = selected[3]
        session = self.db._Session()
        request = session.query(JournalRequest).filter_by(id=selected_id).first()

        self.selected_request = request
        self.why_label.set_text(request.why)
        self.ssn_label.set_text(request.ssn)
        session.close()

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
        response = JournalResponse(req.id, False, u"",
                                   req.ssn, unicode(self.why_entry.get_text()))
        self.db.add(response)
        print "NO"

