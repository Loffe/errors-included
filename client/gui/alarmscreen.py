# -*- coding: utf-8 -*-

import gtk
import gobject
import map.mapdata
import shared.data
import datetime
import gui


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

        hbox = gtk.HBox(False,0)
        self.add_with_viewport(hbox)
        left_box = gtk.VBox(True,0)
        right_box = gtk.VBox(True,0)
        hbox.pack_start(left_box,False,False,0)
        hbox.add(right_box)

        # create entries
        self.event_entry = self.new_entry("Händelse:", left_box, right_box)
        
        self.location_entry = self.new_entry("Skadeplats ort:", left_box, right_box)
        
        self.location_entry2 = self.new_coordlabel("Skadeplats lon-Gps:", left_box, right_box)
        
        self.location_entry3 = self.new_coordlabel("Skadeplats lat-Gps:", left_box, right_box)

        self.hurted_entry = self.new_entry("Antal skadade:", left_box, right_box)

        contact = self.new_section("Kontaktperson:", left_box, right_box)
#        contact.set_alignment(0, 0.5)
#        invisible_label = gtk.Label("")
#        right_box.add(invisible_label)
        
        self.name_entry = self.new_entry("Namn:", left_box, right_box)     

        self.number_entry = self.new_entry("Nummer:", left_box, right_box)

        self.random_entry = self.new_entry("Övrigt:", left_box, right_box)

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
        
        self.emit("okbutton-alarm-clicked")
        
gobject.type_register(AlarmScreen)
gobject.signal_new("okbutton-alarm-clicked", AlarmScreen, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
