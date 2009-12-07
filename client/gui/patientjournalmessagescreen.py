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


class PatientJournalMessageScreen(gtk.ScrolledWindow, gui.Screen):
    '''
    The screen in which you create a new alarm.
    '''
    # the entries
    db = None

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
        
        label, self.why_Entry = new_entry("Varför",vbox)
        label, self.social_security_Number = new_entry("Personnummer",vbox)
        
#        # add event handler
        self.combo_box.connect('changed', self.select_m)
#
#        # set the first item added as active
        self.combo_box.set_active(0)

        # show 'em all! (:
        self.show_all()

    '''Handle events
    '''

    def select_m(self, combobox):
        
        '''
        Call when combobox changes to switch obstacle type.
        @param combobox: the changed combobox
        '''
        # set the selected type
        self.selected_m = self.combo_box.get_active_text()
        messages = self.db.patientjournalmessage()
        for message in messages:
            patientjournalMessage = "varför: " + str(message.why_entry) + "    personumer: " + str(message.social_security_number)
            if patientjournalMessage == self.selected_m:
                self.why_Entry.set_text(message.why_entry)
                self.social_security_Number.set_text(message.social_security_number)
                
    def add_request(self, request_dict):
        why = request_dict["why"]
        ssn = request_dict["ssn"]
        print "Add request to list plx", why, snn
                
    def ok_button_function(self, event):
        pass
    
    def no_button_function(self, event):
        pass
    