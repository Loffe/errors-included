# -*- coding: utf-8 -*-

import gtk
import map.mapdata
import shared.data
import gui
import pango

class NewMessageScreen(gtk.ScrolledWindow, gui.Screen):
    '''
    The screen in which you create a new alarm.
    '''
    # the entries
    to_entry = None
    subject_entry = None
    message_entry = None


    def __init__(self, db):
        '''
        Constructor. Create the alarmscreen and its entries.
        '''
        gtk.ScrolledWindow.__init__(self)

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

        # create entries
        label, self.to_entry = new_entry("Till",vbox)

        label, self.subject_entry = new_entry("Ämne",vbox)

        msg_label = gtk.Label("Meddelande")
        msg_label.set_alignment(0, 0.5)
        textbox = gtk.TextView()
        textbox.set_editable(True)
        textbox.set_size_request(200,200)
        buffer = textbox.get_buffer()
        buffer.set_text("Skriv ditt meddelande här")
        msgbox = gtk.HBox(True,0)
        msgbox.pack_start(msg_label)
        msgbox.pack_start(textbox)
        vbox.add(msgbox)

        self.show_all()
