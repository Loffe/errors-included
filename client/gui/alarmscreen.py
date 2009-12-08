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
        hbox.pack_start(right_box)

        # create entries
        self.event_entry = self.new_entry("Händelse:", left_box, right_box)
        
        self.location_entry = self.new_entry("Skadeplats ort:", left_box, right_box)
        
        self.coordx_entry = self.new_coordlabel("Skadeplats lon-Gps:", left_box, right_box)
        
        self.coordy_entry = self.new_coordlabel("Skadeplats lat-Gps:", left_box, right_box)

        self.wounded_entry = self.new_entry("Antal skadade:", left_box, right_box)

        self.new_section("Kontaktperson:", left_box, right_box)
        
        self.contact_person_entry = self.new_entry("Namn:", left_box, right_box)     

        self.contact_number_entry = self.new_entry("Nummer:", left_box, right_box)

        self.other_entry = self.new_entry("Övrigt:", left_box, right_box)

        self.show_all()

    def ok_button_function(self, event):
        lon = float(self.coordx_entry.get_text())
        lat = float(self.coordy_entry.get_text())
        poi_data = shared.data.POIData(
                lon,lat,
                unicode(self.event_entry.get_text()),
                datetime.datetime.now(),
                shared.data.POIType.flag)
        self.db.add(poi_data)

        alarm = shared.data.Alarm(
                unicode(self.event_entry.get_text()),
                unicode(self.location_entry.get_text()),
                poi_data,
                unicode(self.contact_person_entry.get_text()),
                unicode(self.contact_number_entry.get_text()),
                self.wounded_entry.get_text(),
                unicode(self.other_entry.get_text()))
        self.db.add(alarm)

        # clear all entries
        for entry in self.entries:
            entry.set_text("")

        self.emit("okbutton-alarm-clicked")
        
gobject.type_register(AlarmScreen)
gobject.signal_new("okbutton-alarm-clicked", AlarmScreen, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
