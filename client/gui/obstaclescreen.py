# -*- coding: utf-8 -*-
import gtk
import gobject
import shared.data
import gui

class ObstacleScreen(gtk.ScrolledWindow, gui.Screen):
    
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
        main_box = gtk.HBox(False,0)
        self.add_with_viewport(main_box)
        left_box = gtk.VBox(True,0)
        right_box = gtk.VBox(True,0)
        main_box.pack_start(left_box,False,False,0)
        main_box.add(right_box)
        
        # create type label
        type_label = gtk.Label("Typ:")
        left_box.pack_start(type_label, True, True, 0)
        
        # create and pack combobox
        combo_box = gtk.combo_box_new_text()
        combo_box.set_size_request(300,50)
        right_box.pack_start(combo_box, True, False, 0)
        
        label, self.location_entry = new_entry("Händelse:")
        left_box.add(label)
        right_box.add(self.location_entry)
        
        label, self.location_entry = new_entry("Skadeplats:")
        left_box.add(label)
        right_box.add(self.location_entry)
        
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
