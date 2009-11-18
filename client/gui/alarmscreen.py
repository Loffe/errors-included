# -*- coding: utf-8 -*-

import gtk
import gobject
import map.mapdata
import shared.data
import datetime
import gui
import pango

class AlarmScreen(gtk.ScrolledWindow, gui.Screen):
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
        Constructor. Create the alarmscreen and its entries.
        '''
        gtk.ScrolledWindow.__init__(self)
        self.db = db

        # set automatic horizontal and vertical scrolling
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        # all entries
        self.entries = []
        
        # method used internally to create new entries
        def new_entry(labeltext):
            label = gtk.Label(labeltext)
            label.set_alignment(0, 0.5)
            entry = gtk.Entry()
            entry.set_max_length(300)
            entry.set_text("")
            entry.select_region(0, len(entry.get_text()))
            self.entries.append(entry)
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
        
        label, self.location_entry = new_entry("Skadeplats ort:")
        
        left_box.add(label)
        right_box.add(self.location_entry)
        
        label, self.location_entry2 = new_entry("Skadeplats lon-Gps:")

        left_box.add(label)
        right_box.add(self.location_entry2)
        
        label, self.location_entry3 = new_entry("Skadeplats lat-Gps:")

        left_box.add(label)
        right_box.add(self.location_entry3)

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

    def ok_button_function(self, event):
        lon = float(self.location_entry2.get_text())
        lat = float(self.location_entry3.get_text())

        if lon != None and lat != None:
            poi_data = shared.data.POIData(lon,lat, self.event_entry.get_text(), datetime.datetime.now(), shared.data.POIType.pasta_wagon)
            alarm = shared.data.Alarm(self.event_entry.get_text(), self.location_entry.get_text(), poi_data, self.name_entry.get_text(), self.number_entry.get_text(), self.hurted_entry.get_text(), self.random_entry.get_text())
            self.db.add(alarm)
        else:
            print "No alarm created due to no lon- or lat-coordinate."

        # clear all entries
        for entry in self.entries:
            entry.set_text("")
        
        self.emit("okbutton-clicked2")
        
gobject.type_register(AlarmScreen)
gobject.signal_new("okbutton-clicked2", AlarmScreen, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
