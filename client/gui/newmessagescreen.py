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


    def __init__(self):
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

#        label, self.message_entry = new_entry("Meddelande",vbox)
#        self.message_entry.set_size_request(200,200)
        msg_label = gtk.Label("Meddelande")
        msg_label.set_alignment(0, 0.5)
        textbox = gtk.TextView()
        textbox.set_editable(True)
        textbox.set_size_request(200,200)
        #print textbox.get_style()["border"]
        buffer = textbox.get_buffer()
        buffer.set_text("Skriv ditt meddelande här")
        #textbox.set_size_allocate(200,200)
        msgbox = gtk.HBox(True,0)
        msgbox.pack_start(msg_label)
        msgbox.pack_start(textbox)
#        text = "Hejsan"
#        tag=gtk.TextTag("default")
#
#
#        self.buffer.set_text(text) #text is a string  
#        start, end=self.buffer.get_bounds()
#        self.buffer.apply_tag_by_name("default",start,end)
        
#        msgbox.pack_start()
#        msgbox.pack_start(msg_label)
        vbox.add(msgbox)
        

        
        self.show_all()
