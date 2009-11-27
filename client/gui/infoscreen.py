# -*- coding: utf-8 -*-

import gtk
import gobject
import map.mapdata
import shared.data
import datetime
import gui
import pango

class InfoScreen(gtk.ScrolledWindow, gui.Screen):
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
        Constructor. Create the infoscreen and its entries.
        '''
        gtk.ScrolledWindow.__init__(self)
        self.db = db 
        
        self.entries = []

        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
#        def new_entry(labeltext, parent):
#            hbox = gtk.HBox(True, 0)
#            label = gtk.Label(labeltext)
#            label.set_alignment(0, 0.5)
#            #label.modify_font(pango.FontDescription("sans 12"))
#
#            entry = gtk.Label()
#            entry.set_alignment(0, 0.5)
#            #entry.modify_font(pango.FontDescription("sans 12"))
#            entry.select_region(0, len(entry.get_text()))
#            hbox.add(label)
#            hbox.add(entry)
#            parent.add(hbox)
#            return entry
#
#        def new_section(title, parent):
#            label = gtk.Label(title)
#            label.modify_font(pango.FontDescription("sans 12"))
#            label.set_alignment(0, 0.5)
#            parent.add(label)
#        
        # create layout boxes
        outer_container = gtk.VBox(False,0)
        #create and pack combobox
        self.combo_box = gtk.combo_box_new_text()
        self.combo_box.set_size_request(300,50)
        self.combo_box.append_text("Välj uppdrag...")
        outer_container.pack_start(self.combo_box, True, True, 0)
        main_box = gtk.HBox(False,0)
        outer_container.pack_start(main_box, True, True, 0)
        self.add_with_viewport(outer_container)
        left_box = gtk.VBox(False,0)
        right_box = gtk.VBox(False,0)
        main_box.pack_start(left_box,False,False,0)
        main_box.add(right_box)
#        
#        # create type label
#        type_label = gtk.Label("Inkomna larm:")
#        type_label.set_alignment(0, 0.5)
#        hbox.pack_start(type_label, True, True, 0)
        
        # create and pack combobox
#        self.combo_box = gtk.combo_box_new_text()
#        self.combo_box.set_size_request(300,50)
#        self.combo_box.append_text("Välj larm...")
#        hbox.pack_start(self.combo_box, True,True, 0)
#        
#        new_section("Nytt uppdrag", main_box)
        
        # create entries
        self.new_section("Mitt uppdarag", left_box, right_box)
        self.event_entry = self.new_entry("     Händelse:", left_box, right_box)

        self.location_entry2 = self.new_coordlabel("     Skadeplats: lon-Gps", left_box, right_box)
        self.location_entry3 = self.new_coordlabel("     Skadeplats: lat-Gps", left_box, right_box)      
        self.hurted_entry = self.new_entry("     Antal skadade:", left_box, right_box)
        self.new_section("Kontaktperson", left_box, right_box)
        self.name_entry = self.new_entry("     Namn:", left_box, right_box)
        self.number_entry = self.new_entry("     Nummer:", left_box, right_box)
        self.new_section("Övrigt", left_box, right_box)
        self.random_entry = self.new_entry("     Information:", left_box, right_box)

#        self.select_unit_button = SelectUnitButton(self.db)
#        main_box.add(self.select_unit_button)        
#
#        # add event handler
#        self.combo_box.connect('changed', self.select_alarm)
#
#        # set the first item added as active
#        self.combo_box.set_active(0)

        self.combo_box.connect('changed', self.select_mission)

        # show 'em all! (:
        main_box.show_all()

    '''Handle events
    '''

#    def select_alarm(self, combobox):
#        '''
#        Call when combobox changes to switch obstacle type.
#        @param combobox: the changed combobox
#        '''
#        pass
        # set the selected type
#        self.selected_alarm = self.combo_box.get_active_text()
#        alarms = self.db.get_all_alarms()
#        for alarm in alarms:
#            if alarm.event == self.selected_alarm:
#                self.event_entry.set_text(alarm.event)
#                self.location_entry2.set_text(str(alarm.poi.coordx))
#                self.location_entry3.set_text(str(alarm.poi.coordy))                
#                self.name_entry.set_text(alarm.contact_person)
#                self.hurted_entry.set_text(str(alarm.number_of_wounded))
#                self.number_entry.set_text(alarm.contact_number)
#                self.random_entry.set_text(alarm.other)

    def ok_button_function(self, event):
        pass
#        self.event_entry.set_text(controller.mission.event_type)
#        self.location_entry2.set_text(str("hej"))
#        self.location_entry3.set_text(str("hej"))                
#        self.name_entry.set_text("hej")
#        self.hurted_entry.set_text(str("hej"))
#        self.number_entry.set_text("hej")
#        self.random_entry.set_text("hej")

    def update_info(self, controller):
        if len(controller.missions) > 0:
            self.event_entry.set_text(controller.missions[0].event_type)
            # @todo: to be continued to fill in the rest of the fields.
            self.location_entry2.set_text(str(controller.missions[0].poi.coordx))
            self.location_entry3.set_text(str(controller.missions[0].poi.coordy))                
            self.name_entry.set_text(controller.missions[0].contact_person)
            self.hurted_entry.set_text(str(controller.missions[0].number_of_wounded))
            self.number_entry.set_text(controller.missions[0].contact_number)
            self.random_entry.set_text(controller.missions[0].other)
            
#        self.event_type = event_type
#        self.poi = poi
#        self.number_of_wounded = number_of_wounded
#        self.contact_person = contact_person
#        self.other = other
#        self.timestamp = timestamp
#        self.units = units
#        self.id = id
    def select_mission(self, combobox):
        '''
        Call when combobox changes to switch obstacle type.
        @param combobox: the changed combobox
        '''
        # set the selected type
        self.selected_mission = self.combo_box.get_active_text()
        missions = self.db.get_all_missions()
        for mission in missions:
            if mission.event == self.selected_mission:
                self.event_entry.set_text(mission.event_type)
                self.location_entry2.set_text(str(mission.poi.coordx))
                self.location_entry3.set_text(str(mission.poi.coordy))    
                self.hurted_entry.set_text(str(mission.number_of_wounded))
                self.name_entry.set_text(mission.contact_person)
                self.number_entry.set_text(mission.contact_number)
                self.random_entry.set_text(mission.other)
