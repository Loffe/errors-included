# -*- coding: utf-8 -*-
import gtk
import gobject
import shared.data
import gui
import pango

class SelectUnitButton(gtk.HBox):
    db = None
    
    def __init__(self, db):
        
        gtk.HBox.__init__(self)

        self.db = db
        
        choose_units_button = gtk.Button("Välj enheter")
        label = choose_units_button.get_child()
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))
        select_dialog = SelectUnitDialog(self.db)
        choose_units_button.connect("clicked", select_dialog.select_units)
        unit_label = gtk.Label("Valda enheter")
        self.add(choose_units_button)
        self.add(unit_label)
    
class SelectUnitDialog(gtk.Dialog):
    db = None
    
    
    def __init__(self, db):
        gtk.Dialog.__init__(self, "Välj enheter",
                 None,  #the toplevel wgt of your app
                 gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  #binary flags or'ed together
                 ("     Avbryt     ", 666, "  Ok  ", 77))
        self.set_size_request(400,400)

        self.db = db

        units = self.db.get_all_units()

        for u in units:
            unit_button = gtk.ToggleButton("%s (%d)" % (u.name, u.id))
            unit_button.show()
            self.vbox.pack_start(unit_button)
    
    def run(self):
        #loopa listan
        print "loopa"
        gtk.Dialog.run(self)
           
    def select_units(self, event):
        result = self.run()
        if result == 77:
            
            self.hide()
            print "Skapade uppdrag"
        elif result == 666:
            print "Avbrot"
        self.hide()

