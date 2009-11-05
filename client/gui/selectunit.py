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
        self.select_dialog = SelectUnitDialog(self.db)
        choose_units_button.connect("clicked", self.select_units)
        self.unit_label = gtk.Label("Valda enheter")
        self.add(choose_units_button)
        self.add(self.unit_label)

    def clear_selected(self):
        self.select_dialog.clear_selected()

    def select_units(self, event):
        selected_units = self.select_dialog.select_units()
        names = [u.name for u in selected_units][:3]
        text = ", ".join(names)
        if len(selected_units) > 3:
            text += "..."
        self.unit_label.set_text(text)

    
class SelectUnitDialog(gtk.Dialog):
    db = None
    selected_units = []
    buttons = {}
    
    
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
            self.buttons[u.id] = unit_button
    
    def run(self):
        #loopa listan
        print "loopa"
        return gtk.Dialog.run(self)

    def clear_selected(self):
        for b in self.buttons.values():
            b.set_active(False)
           
    def select_units(self):
        result = self.run()
        if result == 77:
            self.selected_units = []
            for key in self.buttons.keys():
                b = self.buttons[key]
                if b.get_active():
                    self.selected_units.append(key)
            self.hide()
            print "Skapade uppdrag till", self.selected_units
        elif result == 666:
            for key in self.buttons.keys():
                b = self.buttons[key]
                if key in self.selected_units:
                    b.set_active(True)
                else:
                    b.set_active(False)
            print "Avbrot"
        self.hide()

        return self.db.get_units(self.selected_units)

