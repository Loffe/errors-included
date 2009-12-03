# -*- coding: utf-8 -*-
import gtk
import gobject
import shared.data
import datetime
import gui
import clientgui
import pango
import mapscreen

class ChangeObstacleScreen(gtk.ScrolledWindow, gui.Screen):
    
    def __init__(self, db):
        gtk.ScrolledWindow.__init__(self)
        self.db = db
        
        # the poi to change (MUST be set upon showing this screen)
        self.poi = None

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

        # create type label
        type_label = gtk.Label("Typ:")
        type_label.modify_font(pango.FontDescription("sans 12"))
        type_label.set_alignment(0, 0.5)
        left_box.pack_start(type_label, True, True, 0)
        
        # create and pack combobox
        combo_box = gtk.combo_box_new_text()
        #combo_box.set_size_request(300,50)
        right_box.pack_start(combo_box, True, False, 0)
        
        self.location_entry = self.new_entry("Händelse:", left_box, right_box)
        
        self.location_entry2 = self.new_coordlabel("Skadeplats GPS-lon:", left_box, right_box)      
                
        self.location_entry3 = self.new_coordlabel("Skadeplats GPS-lat:", left_box, right_box)

        # add selectable types

        types = {}
        i = 0
        types = ["tree", "bridge", "other"]
        for type in types:
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
        self.selected_type = unicode(combobox.get_active_text())
    
    def delete(self, event):
        pass    
    
    def change(self, event):
        pass

#        self.emit("okbutton-obstacle-clicked")

#gobject.type_register(ObstacleScreen)
#gobject.signal_new("okbutton-obstacle-clicked", ObstacleScreen, gobject.SIGNAL_RUN_FIRST,
#                   gobject.TYPE_NONE, ())
