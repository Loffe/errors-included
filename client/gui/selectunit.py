# -*- coding: utf-8 -*-
import gtk
import gobject
import shared.data
import gui
import pango

class SelectUnitButton(gtk.HBox):
    
    def __init__(self):
        
        gtk.HBox.__init__(self)
        
        choose_units_button = gtk.Button("Välj enheter")
        label = choose_units_button.get_child()
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))
        select_dialog = SelectUnitDialog()
        choose_units_button.connect("clicked", select_dialog.select_units)
        unit_label = gtk.Label("Valda enheter")
        self.add(choose_units_button)
        self.add(unit_label)
    
    
    
    
class SelectUnitDialog(gtk.Dialog):
    
    
    def __init__(self):
        gtk.Dialog.__init__(self, "Välj enheter",
                 None,  #the toplevel wgt of your app
                 gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  #binary flags or'ed together
                 ("     Avbryt     ", 666, "  Ok  ", 77))
        self.set_size_request(400,400)

        unit1 = gtk.ToggleButton("Enhet 1")
        unit1.show()
        unit2 = gtk.ToggleButton("Enhet 2")
        unit2.show()
        unit3 = gtk.ToggleButton("Enhet 3")
        unit3.show()
        unit4 = gtk.ToggleButton("Enhet 4")
        unit4.show()
        self.vbox.pack_start(unit1)
        self.vbox.pack_start(unit2)
        self.vbox.pack_start(unit3)
        self.vbox.pack_start(unit4)
           
    def select_units(self, event):
        result = self.run()
        if result == 77:
            self.hide()
            print "Skapade uppdrag"
        elif result == 666:
            print "Avbrot"
        self.hide()

 