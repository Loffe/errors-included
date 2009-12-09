# -*- coding: utf-8 -*-

import gtk
import gobject
import map.mapdata
import shared.data
import datetime
import gui
import pango
from selectunit import SelectUnitButton
from selectunit import SelectUnitDialog

class MissionInfoScreen(gtk.ScrolledWindow, gui.Screen):
    '''
    The screen in which you create a new alarm.
    '''

    def __init__(self, db, many_missions = True):
        '''
        Constructor. Create the infoscreen and its entries.
        '''
        gtk.ScrolledWindow.__init__(self)
        # the database to save changes to
        self.db = db
        # the mission to change (MUST be set upon showing this screen)
        self.mission = None
        # set automatic horizontal and vertical scrolling
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        # create layout boxes
        vbox = gtk.VBox(False,0)
        hbox = gtk.HBox(False,0)
        self.add_with_viewport(vbox)
        left_box = gtk.VBox(True,0)
        right_box = gtk.VBox(True,0)
        hbox.pack_start(left_box,False,False,0)
        hbox.pack_start(right_box)
        vbox.pack_start(hbox)

        self.mission_combo_box = gtk.combo_box_new_text()
        if many_missions:
            # create my missions label
            type_label = gtk.Label("Mina uppdrag:")
            type_label.modify_font(pango.FontDescription("sans 12"))
            type_label.set_alignment(0, 0.5)
            left_box.pack_start(type_label, True, True, 0)
            # create and pack combobox
            self.mission_combo_box.set_size_request(300,50)
            self.mission_combo_box.append_text("Välj uppdrag...")
            self.mission_combo_box.connect('changed', self.select_mission)
            right_box.pack_start(self.mission_combo_box)
        
        # list of all entries
        self.entries = []
        
        # mission entries
        self.new_section("Uppdrag", left_box, right_box)
        self.event_entry = self.new_entry("     Händelse:", left_box, right_box)
        self.wounded_entry = self.new_entry("     Antal skadade:", left_box, right_box)
        self.other_entry = self.new_entry("     Information:", left_box, right_box)
        
        # create status label
        type_label = gtk.Label("Status:")
        type_label.modify_font(pango.FontDescription("sans 12"))
        type_label.set_alignment(0, 0.5)
        left_box.pack_start(type_label, True, True, 0)
        # create and pack combobox
        self.status_combo_box = gtk.combo_box_new_text()
        self.status_combo_box.set_size_request(300,50)
        self.selected_status = None
        self.status_combo_box.connect('changed', self.select_status)
        right_box.pack_start(self.status_combo_box)

        # position entries
        self.new_section("Position", left_box, right_box)
        self.coordx_entry = self.new_entry("     Longitud", left_box, right_box)
        self.coordy_entry = self.new_entry("     Latitude", left_box, right_box)        
        
        # contact person entries
        self.new_section("Kontaktperson", left_box, right_box)
        self.contact_person_entry = self.new_entry("     Namn:", left_box, right_box)
        self.contact_number_entry = self.new_entry("     Nummer:", left_box, right_box)

        # select units button
        self.select_unit_button = SelectUnitButton(self.db)
        vbox.add(self.select_unit_button)

        # show 'em all! (:
        vbox.show_all()

    '''Handle events
    '''
    def set_missions(self, missions):
        self.mission_combo_box.get_model().clear()
        self.mission_combo_box.append_text("Välj uppdrag...")
        for m in missions:
            self.mission_combo_box.append_text(m.event_type)
        self.mission_combo_box.set_active(0)
    
    def set_entries(self, mission):
        self.mission = mission
        self.event_entry.set_text(mission.event_type)
        self.coordx_entry.set_text(str(mission.poi.coordx))
        self.coordy_entry.set_text(str(mission.poi.coordy))        
        self.wounded_entry.set_text(str(mission.number_of_wounded))
        self.contact_person_entry.set_text(mission.contact_person)
        self.contact_number_entry.set_text(mission.contact_number)
        self.other_entry.set_text(mission.other)

        self.status_combo_box.get_model().clear()
        self.status_combo_box.append_text(mission.status)
        statuslist = [u"active", u"done", u"aborted"]
        for status in statuslist:
            if status != mission.status:
                self.status_combo_box.append_text(status)
        self.status_combo_box.set_active(0)
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
        if self.mission.__class__ != shared.data.MissionData:
            return
        self.db.delete(self.mission)

    def change_button_function(self, event):
        if self.mission.__class__ != shared.data.MissionData:
            return
        poi_data = shared.data.POIData(
                coordx=float(self.coordx_entry.get_text()),
                coordy=float(self.coordy_entry.get_text()),
                name=unicode(self.mission.poi.name),
                timestamp=datetime.datetime.now(),
                type=self.mission.poi.type,
                subtype=self.mission.poi.subtype,
                id=self.mission.poi.id)
        self.db.change(poi_data)

        mission_data = shared.data.MissionData(
                unicode(self.event_entry.get_text()),
                poi_data,
                unicode(self.wounded_entry.get_text()),
                unicode(self.contact_person_entry.get_text()),
                unicode(self.contact_number_entry.get_text()),
                unicode(self.other_entry.get_text()),
                self.db.get_units(self.select_unit_button.select_dialog.selected_units),
                status=unicode(self.selected_status),
                timestamp=datetime.datetime.now(),
                id=self.mission.id)
        self.db.change(mission_data)

    def select_mission(self, combobox):
        '''
        Call when combobox changes to switch selected mission.
        @param combobox: the changed combobox
        '''
        # set the selected type
        self.selected_mission = combobox.get_active_text()
        for mission in self.db.get_all_missions():
            if mission.event_type == self.selected_mission:
                self.set_entries(mission)
                
    def select_status(self, combobox):
        '''
        Call when combobox changes to switch selected status.
        @param combobox: the changed combobox
        '''
        # set the selected type
        self.selected_status = combobox.get_active_text()
