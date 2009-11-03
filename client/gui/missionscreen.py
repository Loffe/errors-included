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
        
        def new_entry(labeltext):
            label = gtk.Label(labeltext)
            label.set_alignment(0, 0.5)
            entry = gtk.Entry()
            entry.set_max_length(300)
            entry.set_text("")
            entry.select_region(0, len(entry.get_text()))
            return (label, entry)
        
        # create layout boxes
        main_box = gtk.VBox(False,0)
        self.add_with_viewport(main_box)
        hbox = gtk.HBox(False,0)
        #right_box = gtk.VBox(True,0)
        main_box.pack_start(hbox,True,True,0)
        #main_box.add(right_box)
        
        # create type label
        type_label = gtk.Label("Inkomna larm:")
        type_label.set_alignment(0, 0.5)
        hbox.pack_start(type_label, True, True, 0)
        
        # create and pack combobox
        combo_box = gtk.combo_box_new_text()
        combo_box.set_size_request(300,50)
        hbox.pack_start(combo_box, True,True, 0)
        
#        label, self.location_entry = new_entry("Nytt uppdrag:")
#        left_box.add(label)
#        right_box.add(self.location_entry)
        
        new_mission_label = gtk.Label("Nytt uppdrag:")
        new_mission_label.set_alignment(0, 0.5)
        #invisible_label = gtk.Label("")
        hbox1 = gtk.HBox(True,0)
        main_box.add(hbox1)
        hbox1.pack_start(new_mission_label,True,True,0)
        #hbox1.pack_start(invisible_label,True,True,0)
        
        # create entries
        label, self.event_entry = new_entry("     Händelse:")
        label.modify_font(pango.FontDescription("sans 12"))
        hbox2 = gtk.HBox(True,0)
        main_box.add(hbox2)
        hbox2.pack_start(label,True,True,0)
        hbox2.pack_start(self.event_entry,True,True,0)
        
        label, self.location_entry = new_entry("     Skadeplats:")
        label.modify_font(pango.FontDescription("sans 12"))
        hbox3 = gtk.HBox(True,0)
        main_box.add(hbox3)
        hbox3.pack_start(label,True,True,0)
        hbox3.pack_start(self.location_entry,True,True,0)

        label, self.hurted_entry = new_entry("     Antal skadade:")
        label.modify_font(pango.FontDescription("sans 12"))
        hbox4 = gtk.HBox(True,0)
        main_box.add(hbox4)
        hbox4.add(label)
        hbox4.add(self.hurted_entry)

        contact = gtk.Label("Kontaktperson:")
        contact.set_alignment(0, 0.5)
        #label.modify_font(pango.FontDescription("sans 12"))
        #invisible_label = gtk.Label("")
        hbox5 = gtk.HBox(True,0)
        main_box.add(hbox5)
        hbox5.pack_start(contact,True,True,0)
        #hbox5.add(invisible_label)

        
        label, self.name_entry = new_entry("     Namn:")
        label.set_alignment(0, 0.5)
        label.modify_font(pango.FontDescription("sans 12"))
        hbox6 = gtk.HBox(True,0)
        main_box.add(hbox6)
        hbox6.add(label)
        hbox6.add(self.name_entry)
        
        label, self.number_entry = new_entry("     Nummer:")
        label.set_alignment(0, 0.5)
        label.modify_font(pango.FontDescription("sans 12"))
        hbox7 = gtk.HBox(True,0)
        main_box.add(hbox7)
        hbox7.add(label)
        hbox7.add(self.number_entry)

        label, self.random_entry = new_entry("Övrigt:")
        hbox8 = gtk.HBox(True,0)
        main_box.add(hbox8)
        hbox8.add(label)
        hbox8.add(self.random_entry)
        
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
        

