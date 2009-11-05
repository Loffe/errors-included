# -*- coding: utf-8 -*-
import gtk
import gobject
import shared.data
import gui
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
        
        def new_entry(labeltext, parent):
            hbox = gtk.HBox(True, 0)
            label = gtk.Label(labeltext)
            label.set_alignment(0, 0.5)
            label.modify_font(pango.FontDescription("sans 12"))

            entry = gtk.Entry()
            entry.set_max_length(300)
            entry.set_text("")
            entry.select_region(0, len(entry.get_text()))
            hbox.add(label)
            hbox.add(entry)
            parent.add(hbox)
            return entry

        def new_section(title, parent):
            label = gtk.Label(title)
            label.set_alignment(0, 0.5)
            parent.add(label)
        
        # create layout boxes
        main_box = gtk.VBox(False,0)
        self.add_with_viewport(main_box)
        hbox = gtk.HBox(False,0)
        main_box.pack_start(hbox,True,True,0)
        
        # create type label
        type_label = gtk.Label("Inkomna larm:")
        type_label.set_alignment(0, 0.5)
        hbox.pack_start(type_label, True, True, 0)
        
        # create and pack combobox
        combo_box = gtk.combo_box_new_text()
        combo_box.set_size_request(300,50)
        hbox.pack_start(combo_box, True,True, 0)
        
        new_section("Nytt uppdrag", main_box)
        
        # create entries
        self.event_entry = new_entry("     Händelse:", main_box)

        self.location_entry = new_entry("     Skadeplats:", main_box)

        self.hurted_entry = new_entry("     Antal skadade:", main_box)

        new_section("Kontaktperson", main_box)

        self.name_entry = new_entry("     Namn:", main_box)

        self.number_entry = new_entry("     Nummer:", main_box)

        new_section("Övrigt", main_box)
        self.random_entry = new_entry("     Information:", main_box)
        

        select_unit_button = SelectUnitButton(self.db)
        main_box.add(select_unit_button)
        
        # add selectable types
        for alarm in self.db.get_all_alarms():
                combo_box.append_text(alarm.event)
                

        # add event handler
        combo_box.connect('changed', self.select_alarm)

        # set the first item added as active
#        combo_box.set_active(0)

        # show 'em all! (:
        main_box.show_all()

    '''Handle events
    '''

    def select_alarm(self, combobox):
        '''
        Call when combobox changes to switch obstacle type.
        @param combobox: the changed combobox
        '''
        # set the selected type
        self.selected_alarm = combobox.get_active_text()
        for alarm in self.db.get_all_alarms():
            if alarm.event == self.selected_alarm:
                self.event_entry.set_text(alarm.event)
                self.location_entry.set_text(alarm.location_name)
                self.name_entry.set_text(alarm.contact_person)
                self.hurted_entry.set_text(str(alarm.number_of_wounded))
                self.number_entry.set_text(alarm.contact_number)
                self.random_entry.set_text(alarm.other)
                
    def ok_button_function(self, event):
        alarm = None
        for a in self.db.get_all_alarms():
            if a.event == self.selected_alarm:
                alarm = a
        mission = shared.data.MissionData(self.event_entry.get_text(), alarm.poi, self.hurted_entry.get_text(), self.name_entry.get_text(), self.random_entry.get_text())
        self.db.add(mission)
