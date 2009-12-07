# -*- coding: utf-8 -*-

import gtk
import gobject
import map.mapdata
import shared.data
import datetime
import gui
import pango

class StatusScreen(gtk.ScrolledWindow, gui.Screen):
    
    
    
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
        Constructor. Create the statusscreen and its entries.
        '''
        gtk.ScrolledWindow.__init__(self)
        self.db = db 

        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        
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
        type_label = gtk.Label("Inkomna uppdrag:")
        type_label.modify_font(pango.FontDescription("sans 12"))
        type_label.set_alignment(0, 0.5)
        left_box.pack_start(type_label, True, True, 0)
        
        # create and pack combobox
        self.combo_box = gtk.combo_box_new_text()
        self.combo_box.set_size_request(300,50)
        self.combo_box.append_text("Välj larm...")
        right_box.pack_start(self.combo_box, True,False, 0)
        
        label = self.new_section("Nytt uppdrag", left_box, right_box)
        
        # create entries
        self.event_entry = self.new_entry("     Händelse:", left_box, right_box)

        self.location_entry2 = self.new_coordlabel("     Skadeplats: lon-Gps", left_box, right_box)
        self.location_entry3 = self.new_coordlabel("     Skadeplats: lat-Gps", left_box, right_box)        
        self.hurted_entry = self.new_entry("     Antal skadade:", left_box, right_box)
        self.new_section("Kontaktperson", left_box, right_box)
        self.name_entry = self.new_entry("     Namn:", left_box, right_box)
        self.number_entry = self.new_entry("     Nummer:", left_box, right_box)
        self.new_section("Övrigt", left_box, right_box)
        self.random_entry = self.new_entry("     Information:", left_box, right_box)

        

        # add event handler
        self.combo_box.connect('changed', self.select_mission)

        # set the first item added as active
        self.combo_box.set_active(0)

        # show 'em all! (:
        vbox.show_all()
        
        
        
        
    def ok_button_function(self, event):
        pass
        #self.mission.status = "klart"
                
        #self.db.change(mission_data)

    def select_mission(self, combobox):
        '''
        Call when combobox changes to switch selected mission.
        @param combobox: the changed combobox
        '''
        # set the selected type
        self.selected_mission = self.combo_box.get_active_text()
        for mission in self.db.get_all_missions():
            if mission.event_type == self.selected_mission:
                self.event_entry.set_text(mission.event_type)
                self.location_entry2.set_text(str(mission.poi.coordx))
                self.location_entry3.set_text(str(mission.poi.coordy))
                self.hurted_entry.set_text(str(mission.number_of_wounded))
                self.name_entry.set_text(mission.contact_person)
                self.number_entry.set_text(mission.contact_number)
                self.random_entry.set_text(mission.other)

        
        
        
        
        
        
        
        
        