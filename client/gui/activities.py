# -*- coding: utf-8 -*-
import gtk
import gobject
import shared.data
import gui
import pango

class Activities(gtk.HBox):
    db = None
    
    def __init__(self, db):
        
        gtk.VBox.__init__(self)

        self.db = db
        
        #type_label = gtk.Label("Inkomna larm:")
        #vbox2.add(type_label)
        
        #choose_units_button = gtk.Button("Välj enheter")
        #label = choose_units_button.get_child()
        #label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))
        #self.select_dialog = SelectUnitDialog(self.db)
        #choose_units_button.connect("clicked", self.select_units)
        #self.unit_label = gtk.Label("Valda enheter")
        #self.add(choose_units_button)
        #self.add(self.unit_label)

    def clear_selected(self):
        pass

    def select_units(self, event):
        pass

    
