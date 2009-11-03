# -*- coding: utf-8 -*-
import gtk
import gobject
import shared.data
import gui
import pango
from selectunit import SelectUnitButton
from selectunit import SelectUnitDialog

class MissionScreen(gtk.ScrolledWindow, gui.Screen):
    
    selected_type = None
    
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        
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
        
        new_mission_label = gtk.Label("Nytt uppdrag:")
        new_mission_label.set_alignment(0, 0.5)
        #invisible_label = gtk.Label("")
        hbox1 = gtk.HBox(True,0)
        main_box.add(hbox1)
        hbox1.pack_start(new_mission_label,True,True,0)
        
        # create entries
        self.event_entry = new_entry("     Händelse:", main_box)

        self.location_entry = new_entry("     Skadeplats:", main_box)

        self.hurted_entry = new_entry("     Antal skadade:", main_box)

        contact = gtk.Label("Kontaktperson:")
        contact.set_alignment(0, 0.5)
        hbox5 = gtk.HBox(True,0)
        main_box.add(hbox5)
        hbox5.pack_start(contact,True,True,0)

        self.name_entry = new_entry("     Namn:", main_box)

        self.number_entry = new_entry("     Nummer:", main_box)

        self.random_entry = new_entry("Övrigt:", main_box)

        select_unit_button = SelectUnitButton()
        main_box.add(select_unit_button)
        
        # add selectable types
        for type in shared.data.ObstacleType.__dict__.keys():
            if type[0] != "_":
                combo_box.append_text(type)

        # add event handler
        combo_box.connect('changed', self.select_type)

        # set the first item added as active
        combo_box.set_active(0)

        # show 'em all! (:
        main_box.show_all()

    '''Handle events
    '''

    def select_type(self, combobox):
        '''
        Call when combobox changes to switch obstacle type.
        @param combobox: the changed combobox
        '''
        # set the selected type
        self.selected_type = combobox.get_active()
        

