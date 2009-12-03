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
        
    def delete(self, event):
        pass

    def change(self, event):
        pass
#        self.emit("okbutton-mission-clicked")
        
#gobject.type_register(MissionScreen)
#gobject.signal_new("okbutton-mission-clicked", MissionScreen, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
