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
        self.combo_box = gtk.combo_box_new_text()
        #combo_box.set_size_request(300,50)
        main_box.pack_start(self.combo_box, False, False, 0)
        self.textview = gtk.TextView()
        self.textview.set_editable(False)
        self.textview.set_size_request(400,-1)
        self.textview.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        main_box.pack_start(self.textview)
        # add event handler
        self.combo_box.connect('changed', self.selected)
        
        self.combo_box.append_text("Välj journal...")
        self.combo_box.append_text("Diabetes")
        # set the first item added as active
        self.combo_box.set_active(0)

        # show 'em all! (:
        self.show_all()

    def selected(self, combobox):
        pass
       
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
