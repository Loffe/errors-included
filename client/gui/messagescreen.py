# coding: utf-8

import gtk
import map.mapdata
import shared.data
import gui
import pango

class MessageScreen(gtk.ScrolledWindow, gui.Screen):
    '''
    The screen in which you create a new alarm
    '''
    # the entries
    event_entry = None
    location_entry = None
    hurted_entry = None
    name_entry = None
    number_entry = None
    random_entry = None

    def __init__(self):
        '''
        Constructor. Create the missionscreen and its entries.
        '''
        gtk.ScrolledWindow.__init__(self)

        # set automatic horizontal and vertical scrolling
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        # method used internally to create new entries
        def new_entry(labeltext):
            label = gtk.Label(labeltext)
            label.set_alignment(0, 0.5)
            entry = gtk.Entry()
            entry.set_max_length(300)
            entry.set_text("")
            entry.select_region(0, len(entry.get_text()))
            return (label, entry)

        hbox = gtk.HBox(False,0)
        self.add_with_viewport(hbox)
        left_box = gtk.VBox(True,0)
        right_box = gtk.VBox(True,0)
        hbox.pack_start(left_box,False,False,0)
        hbox.add(right_box)

        # create entries
        label, self.event_entry = new_entry("Händelse:")
        left_box.add(label)
        right_box.add(self.event_entry)
        
        label, self.location_entry = new_entry("Skadeplats:")
        left_box.add(label)
        right_box.add(self.location_entry)

        label, self.hurted_entry = new_entry("Antal skadade:")
        left_box.add(label)
        right_box.add(self.hurted_entry)

        contact = gtk.Label("Kontaktperson:")
        contact.set_alignment(0, 0.5)
        invisible_label = gtk.Label("")
        left_box.add(contact)
        right_box.add(invisible_label)
        
        label, self.name_entry = new_entry("Namn:")
        label.set_alignment(0.5, 0.5)
        label.modify_font(pango.FontDescription("sans 12"))
        left_box.add(label)
        right_box.add(self.name_entry)
        
        label, self.number_entry = new_entry("Nummer:")
        label.set_alignment(0.5, 0.5)
        label.modify_font(pango.FontDescription("sans 12"))
        left_box.add(label)
        right_box.add(self.number_entry)

        label, self.random_entry = new_entry("Övrigt:")
        left_box.add(label)
        right_box.add(self.random_entry)

        
        self.show_all()
        
    ''' Handle Events
    '''
    def show_messages(self, event):
        '''
        Call when OK-button is pressed. Create the alarm using information from entries.
        '''
        pass
 
