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

class InboxScreen(gtk.ScrolledWindow, gui.Screen):
    '''
    The screen in which you create a new alarm.
    '''
    # the entries
    event_entry = None
    location_entry = None
    location_entry2 = None
    location_entry3 = None
    hurted_entry = None
    name_entry = None
    number_entry = None
    random_entry = None
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
        self.combo_box.append_text("Välj Meddelande...")
        vbox.pack_start(self.combo_box, True,True, 0)

        label, self.subject_entry = new_entry("Ämne",vbox)

        msg_label = gtk.Label("Meddelande")
        
        msg_label.set_alignment(0, 0.5)
        textbox = gtk.TextView()
        textbox.set_editable(False)
        self.subject_entry.set_editable(False)
        textbox.set_size_request(250,250)
        textbox.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        self.buffer = textbox.get_buffer()
        self.buffer.set_text("")
        msgbox = gtk.HBox(True,0)
        msgbox.pack_start(msg_label)
        msgbox.pack_start(textbox)
        vbox.add(msgbox)  
        
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
        messages = self.db.textmessages()
        for message in messages:
            senderandsubject = "från: " + str(message.sender) + "    Ämne: " + str(message.subject)
            if senderandsubject == self.selected_m:
                self.subject_entry.set_text(message.subject)
                self.buffer.set_text(message.message_content)

                

    