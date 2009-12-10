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
from shared.data import JournalRequest, JournalResponse
import config

class RequestDialog(gtk.Dialog, gui.Screen):
    def __init__(self):
        gtk.Dialog.__init__(self, "Begär patientjournal",
                None,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                ("Avbryt", 0, "Begär patientjournal", 1))
        self.set_size_request(400, 200)
        self.ssn_entry = self.create_entry("Personnummer",self.vbox)
        self.why_entry = self.create_entry("Anledning",self.vbox)
        self.vbox.show_all()


class PatientJournalScreen(gtk.ScrolledWindow, gui.Screen):
    '''
    The screen in which you create a new PatientJournalRequest
    '''
   # the entries
    to_entry = None
    subject_entry = None
    message_entry = None
    db = None
    dialog = RequestDialog()

    def __init__(self, db, queue):
        '''
        Constructor. Create the request screen and its entries.
        '''
        gtk.ScrolledWindow.__init__(self)
        self.db = db
        self.queue = queue

        # set automatic horizontal and vertical scrolling
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        
        main_box = gtk.VBox(False,0)
        self.add_with_viewport(main_box)

        # create and pack combobox
        self.liststore = gtk.ListStore(str, int)
        self.combo_box = gtk.ComboBox(self.liststore)
        cell = gtk.CellRendererText()
        self.combo_box.pack_start(cell, True)
        self.combo_box.add_attribute(cell, 'text', 0)  

        #combo_box.set_size_request(300,50)
        main_box.pack_start(self.combo_box, False, False, 0)
        self.textview = gtk.TextView()
        self.textview.set_editable(False)
        self.textview.set_size_request(400,-1)
        self.textview.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        main_box.pack_start(self.textview)
        # add event handler
        self.combo_box.connect('changed', self.selected)
        
        self.update_list()
        # set the first item added as active
        self.combo_box.set_active(0)

        # show 'em all! (:
        self.show_all()

    def update_list(self):
        self.combo_box.get_model().clear()
        self.combo_box.get_model().append(("Välj journal...", 0))
        for j in self.db.get_journals():
            self.combo_box.get_model().append((j.ssn, j.id))


    def got_journal_response(self, event):
        print "got new journal"
        self.update_list()

    def selected(self, combobox):
        selected = self.liststore[self.combo_box.get_active()]
        selected_id = selected[1]
        session = self.db._Session()
        journal = session.query(JournalResponse).filter_by(id=selected_id).first()

        buffer = gtk.TextBuffer()
        buffer.set_text(journal.journal)
        self.textview.set_buffer(buffer)
        session.close()
       
    def ok_button_function(self, event):
        self.dialog.show()
        result = self.dialog.run()
        if result == 1:
            ssn = self.dialog.ssn_entry.get_text()
            why = self.dialog.why_entry.get_text()
            print "Requesting journal for %s: %s" % (ssn, why)
            data = JournalRequest(unicode(why),
                                  unicode(ssn),
                                  config.client.name)
            self.db.add(data)

        self.dialog.hide()
        self.emit("okbutton_clicked_PatientJournalScreen")
        
gobject.type_register(PatientJournalScreen)
gobject.signal_new("okbutton_clicked_PatientJournalScreen", PatientJournalScreen, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
