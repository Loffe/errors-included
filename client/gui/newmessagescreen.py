# -*- coding: utf-8 -*-

import gtk
import map.mapdata
import shared.data
import gui
import pango
import gobject
from selectunit import SelectUnitButton
from selectunit import SelectUnitDialog

class NewMessageScreen(gtk.ScrolledWindow, gui.Screen):
    '''
    The screen in which you create a new alarm.
    '''
    # the entries
    to_entry = None
    subject_entry = None
    message_entry = None
    db = None


    def __init__(self, db):
        '''
        Constructor. Create the alarmscreen and its entries.
        '''
        gtk.ScrolledWindow.__init__(self)
        self.db = db

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
        #label, self.to_entry = new_entry("Till",vbox)

        label, self.subject_entry = new_entry("Ämne",vbox)

        msg_label = gtk.Label("Meddelande")
        
        msg_label.set_alignment(0, 0.5)
        textbox = gtk.TextView()
        textbox.set_editable(True)
        textbox.set_size_request(200,200)
        self.buffer = textbox.get_buffer()
        self.buffer.set_text("Skriv ditt meddelande här")
        msgbox = gtk.HBox(True,0)
        msgbox.pack_start(msg_label)
        msgbox.pack_start(textbox)
        vbox.add(msgbox)
        
        self.select_unit_button = SelectUnitButton(self.db)
        vbox.add(self.select_unit_button)

        self.show_all()
        
        
    def ok_button_function(self, event):
        print "hejlkk"
    
        #lon = float(self.location_entry2.get_text())
        #lat = float(self.location_entry3.get_text())
        selected = self.select_unit_button.select_dialog.selected_units
        units = self.db.get_units(selected)
    
        #datetime 
        #print self.buffer#.get_text()
        text = shared.data.TextMessage(self.subject_entry.get_text(), "hej", units)
        self.db.add(text)
        self.emit("okbutton_clicked_new_message")
        
gobject.type_register(NewMessageScreen)
gobject.signal_new("okbutton_clicked_new_message", NewMessageScreen, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
        
