# -*- coding: utf-8 -*-
import gtk
import gui

class UnitScreen(gtk.ScrolledWindow, gui.Screen):
    
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)

        #all entries
        self.entries = []

        # set automatic horizontal and vertical scrolling
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        # create layout boxes
        main_box = gtk.HBox(False,0)
        self.add_with_viewport(main_box)
        left_box = gtk.VBox(False,0)
        right_box = gtk.VBox(False,0)
        main_box.pack_start(left_box,False,False,0)
        main_box.add(right_box)

        self.new_section("Enhet", left_box, right_box)
        self.name_entry = self.new_label("Namn:", left_box, right_box)
        self.type_entry = self.new_label("Typ:", left_box, right_box)

        self.new_section("Position:", left_box, right_box)
        self.coordx_entry= self.new_label("Longitud:", left_box, right_box)      
        self.coordy_entry = self.new_label("Latitud:", left_box, right_box)

        # show 'em all! (:
        main_box.show_all()
        
    def set_entries(self, unit):
        self.name_entry.set_text(unit.name)
        self.type_entry.set_text(unit.type)
        self.coordx_entry.set_text(str(unit.coordx))
        self.coordy_entry.set_text(str(unit.coordy))
