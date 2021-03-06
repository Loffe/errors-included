# -*- coding: utf-8 -*-
import gtk
import gobject
import shared.data
import gui
import datetime
import pango
from selectunit import SelectUnitButton
from selectunit import SelectUnitDialog

class MissionScreen(gtk.ScrolledWindow, gui.Screen):
    
    selected_alarm = None
    db = None
    
    def __init__(self, db):
        gtk.ScrolledWindow.__init__(self)
        self.db = db

        # set automatic horizontal and vertical scrolling
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        # all entries
        self.entries = []
        
        # create layout boxes
        vbox = gtk.VBox(False,0)
        hbox = gtk.HBox(False,0)
        self.add_with_viewport(vbox)
        left_box = gtk.VBox(True,0)
        right_box = gtk.VBox(True,0)
        hbox.pack_start(left_box,False,False,0)
        hbox.add(right_box)
        vbox.pack_start(hbox)
        
        # create type label
        type_label = gtk.Label("Inkomna larm:")
        type_label.modify_font(pango.FontDescription("sans 12"))
        type_label.set_alignment(0, 0.5)
        left_box.pack_start(type_label, True, True, 0)
        
        # create and pack combobox
        self.combo_box = gtk.combo_box_new_text()
        self.combo_box.set_size_request(300,50)
        self.combo_box.append_text("Välj larm...")
        right_box.pack_start(self.combo_box, True,False, 0)
        
        self.new_section("Nytt uppdrag", left_box, right_box)
        self.event_entry = self.new_entry("     Händelse:", left_box, right_box)
        self.wounded_entry = self.new_entry("     Antal skadade:", left_box, right_box)
        self.other_entry = self.new_entry("     Information:", left_box, right_box)
        self.new_section("Position", left_box, right_box)
        self.coordx_entry = self.new_label("     Longitud:", left_box, right_box)
        self.coordy_entry = self.new_label("     Latitud:", left_box, right_box)        
        self.new_section("Kontaktperson", left_box, right_box)
        self.name_entry = self.new_entry("     Namn:", left_box, right_box)
        self.number_entry = self.new_entry("     Nummer:", left_box, right_box)

        self.select_unit_button = SelectUnitButton(self.db)
        vbox.add(self.select_unit_button)

        # add event handler
        self.combo_box.connect('changed', self.select_alarm)

        # set the first item added as active
        self.combo_box.set_active(0)

        # show 'em all! (:
        vbox.show_all()

    '''Handle events
    '''

    def select_alarm(self, combobox):
        '''
        Call when combobox changes to switch obstacle type.
        @param combobox: the changed combobox
        '''
        # set the selected type
        self.selected_alarm = self.combo_box.get_active_text()
        alarms = self.db.get_all_alarms()
        for alarm in alarms:
            if alarm.event == self.selected_alarm:
                self.event_entry.set_text(alarm.event)
                self.coordx_entry.set_text(str(alarm.poi.coordx))
                self.coordy_entry.set_text(str(alarm.poi.coordy))                
                self.name_entry.set_text(alarm.contact_person)
                self.wounded_entry.set_text(str(alarm.number_of_wounded))
                self.number_entry.set_text(alarm.contact_number)
                self.other_entry.set_text(alarm.other)
                
    def ok_button_function(self, event):
        alarm = None
        for a in self.db.get_all_alarms():
            if a.event == self.selected_alarm:
                alarm = a
        lon = float(self.coordx_entry.get_text())
        lat = float(self.coordy_entry.get_text())
        selected = self.select_unit_button.select_dialog.selected_units
        units = self.db.get_units(selected)
        poi_data = None
        if alarm == None:
            # @todo CHANGE POI-TYPE, SHOULDNT BE HARDCODED!
            poi_data = shared.data.POIData(lon,lat,
                                           unicode(self.event_entry.get_text()),
                                           datetime.datetime.now(),
                                           shared.data.POIType.event,
                                           shared.data.POISubType.other)
            print "POI:", poi_data
            self.db.add(poi_data)
        else:
            poi_data = alarm.poi
        mission_data = shared.data.MissionData(unicode(self.event_entry.get_text()), 
                                               poi_data, 
                                               self.wounded_entry.get_text(), 
                                               unicode(self.name_entry.get_text()), 
                                               unicode(self.number_entry.get_text()), 
                                               unicode(self.other_entry.get_text()), 
                                               units, shared.data.MissionStatus.active)

        self.select_unit_button.clear_selected()
        self.select_unit_button.unit_label.set_text("Inga valda enheter...")
        self.db.add(mission_data)
        self.emit("okbutton-mission-clicked")
        
gobject.type_register(MissionScreen)
gobject.signal_new("okbutton-mission-clicked", MissionScreen, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
