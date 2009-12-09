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
        
        # create type label
        type_label = gtk.Label("Typ:")
        type_label.modify_font(pango.FontDescription("sans 12"))
        type_label.set_alignment(0, 0.5)
        left_box.pack_start(type_label, True, True, 0)
        
        # create combobox used to select event type (poi.subtype)
        self.combo_box = gtk.combo_box_new_text()
        self.selected_type = None
        right_box.pack_start(self.combo_box, True, False, 0)
        # add event handler
        self.combo_box.connect('changed', self.select_type)
        # add selectable types
        types = ["accident", "fire", "other"]
        for type in types:
            self.combo_box.append_text(type)
        self.combo_box.set_active(0)

        # create entries
        self.new_section("Nytt larm", left_box, right_box)
        self.event_entry = self.new_entry("Händelse:", left_box, right_box)
        self.location_entry = self.new_entry("Skadeplats ort:", left_box, right_box)
        self.wounded_entry = self.new_entry("Antal skadade:", left_box, right_box)
        self.other_entry = self.new_entry("Övrigt:", left_box, right_box)
        
        self.new_section("Position", left_box, right_box)
        self.coordx_entry = self.new_label("Longitud:", left_box, right_box)
        self.coordy_entry = self.new_label("Latitud:", left_box, right_box)

        self.new_section("Kontaktperson:", left_box, right_box)
        
        self.contact_person_entry = self.new_entry("Namn:", left_box, right_box)     

        self.contact_number_entry = self.new_entry("Nummer:", left_box, right_box)

        self.show_all()
        
    def select_type(self, combobox):
        '''
        Call when combobox changes to switch obstacle type.
        @param combobox: the changed combobox
        '''
        # set the selected type
        self.selected_type = unicode(combobox.get_active_text())
        
    def ok_button_function(self, event):
        lon = float(self.coordx_entry.get_text())
        lat = float(self.coordy_entry.get_text())
        poi_data = shared.data.POIData(
                lon,lat,
                unicode(self.event_entry.get_text()),
                datetime.datetime.now(),
                shared.data.POIType.event,
                self.selected_type)
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
