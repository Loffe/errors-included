# -*- coding: utf-8 -*-
import gtk
import gobject
import shared.data
import gui
import datetime
import pango
from selectunit import SelectUnitButton
from selectunit import SelectUnitDialog

class ChangeMissionScreen(gtk.ScrolledWindow, gui.Screen):
    
    def __init__(self, db):
        gtk.ScrolledWindow.__init__(self)
        # the database to save changes to
        self.db = db
        # the mission to change (MUST be set upon showing this screen)
        self.mission = None
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
        
        label = self.new_section("Uppdrag", left_box, right_box)
        
        # create entries
        self.event_entry = self.new_entry("     Händelse:", left_box, right_box)

        self.location_entry2 = self.new_entry("     Skadeplats: lon-Gps", left_box, right_box)
        self.location_entry3 = self.new_entry("     Skadeplats: lat-Gps", left_box, right_box)        
        self.hurted_entry = self.new_entry("     Antal skadade:", left_box, right_box)
        self.new_section("Kontaktperson", left_box, right_box)
        self.name_entry = self.new_entry("     Namn:", left_box, right_box)
        self.number_entry = self.new_entry("     Nummer:", left_box, right_box)
        self.new_section("Övrigt", left_box, right_box)
        self.random_entry = self.new_entry("     Information:", left_box, right_box)

        self.select_unit_button = SelectUnitButton(self.db)
        vbox.add(self.select_unit_button)

        # show 'em all! (:
        vbox.show_all()
        
    def set_entries(self, mission):
        self.mission = mission
        self.event_entry.set_text(mission.event_type)
        self.location_entry2.set_text(str(mission.poi.coordx))
        self.location_entry3.set_text(str(mission.poi.coordy))        
        self.hurted_entry.set_text(str(mission.number_of_wounded))
        self.name_entry.set_text(mission.contact_person)
        self.number_entry.set_text(mission.contact_number)
        self.random_entry.set_text(mission.other)
        ids = []
        for unit in mission.units:
            ids.append(unit.id)
        self.select_unit_button.selected_ids = ids
        selected_units = self.db.get_units(ids)
        names = [u.name for u in selected_units][:3]
        text = ", ".join(names)
        if len(selected_units) > 3:
            text += "..."
        if text == "":
            self.select_unit_button.unit_label.set_text("Inga valda enheter...")
        else:
            self.select_unit_button.unit_label.set_text(text)
        
    def delete_button_function(self, event):
        self.db.delete(self.mission)

    def change_button_function(self, event):
        poi_data = shared.data.POIData(
                coordx=float(self.location_entry2.get_text()),
                coordy=float(self.location_entry3.get_text()),
                name=unicode(self.mission.poi.name),
                timestamp=datetime.datetime.now(),
                type=self.mission.poi.type,
                subtype=self.mission.poi.subtype,
                id=self.mission.poi.id)
        self.db.change(poi_data)
        
        mission_data = shared.data.MissionData(
                unicode(self.event_entry.get_text()),
                poi_data,
                unicode(self.hurted_entry.get_text()),
                unicode(self.name_entry.get_text()),
                unicode(self.number_entry.get_text()),
                unicode(self.random_entry.get_text()),
                self.db.get_units(self.select_unit_button.select_dialog.selected_units),
                timestamp=datetime.datetime.now(),
                id=self.mission.id,
                status="Oklart")
        self.db.change(mission_data)

#        self.emit("okbutton-mission-clicked")
        
#gobject.type_register(MissionScreen)
#gobject.signal_new("okbutton-mission-clicked", MissionScreen, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
