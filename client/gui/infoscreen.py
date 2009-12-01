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

        self.combo_box.connect('changed', self.select_mission)

        # show 'em all! (:
        main_box.show_all()

    '''Handle events
    '''

    def ok_button_function(self, event):
        pass

    def update_info(self, controller):
        if len(controller.missions) > 0:
            self.event_entry.set_text(controller.missions[0].event_type)
            self.location_entry2.set_text(str(controller.missions[0].poi.coordx))
            self.location_entry3.set_text(str(controller.missions[0].poi.coordy))                
            self.name_entry.set_text(controller.missions[0].contact_person)
            self.hurted_entry.set_text(str(controller.missions[0].number_of_wounded))
            self.number_entry.set_text(controller.missions[0].contact_number)
            self.random_entry.set_text(controller.missions[0].other)

    def select_mission(self, combobox):
        '''
        Call when combobox changes to switch obstacle type.
        @param combobox: the changed combobox
        '''
        # set the selected type
        self.selected_mission = self.combo_box.get_active_text()
        missions = self.db.get_all_missions()
        for mission in missions:
            if mission.event_type == self.selected_mission:
                self.event_entry.set_text(mission.event_type)
                self.location_entry2.set_text(str(mission.poi.coordx))
                self.location_entry3.set_text(str(mission.poi.coordy))    
                self.hurted_entry.set_text(str(mission.number_of_wounded))
                self.name_entry.set_text(mission.contact_person)
                self.number_entry.set_text(mission.contact_number)
                self.random_entry.set_text(mission.other)
