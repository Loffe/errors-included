#!/usr/bin/env python

# example entry.py

import pygtk
pygtk.require('2.0')
import gtk

class EntryExample:
    def enter_callback(self, widget, entry):
        entry_text = entry.get_text()
        print "Entry contents: %s\n" % entry_text
        
    def new_entry(self, labeltext):
        label = gtk.Label(labeltext)
        label.show()
        entry = gtk.Entry()
        entry.set_max_length(100)
        entry.connect("activate", self.enter_callback, entry)
        entry.set_text("")
        entry.select_region(0, len(entry.get_text()))
        entry.show()
        return (label, entry)


    def __init__(self):
        # create a new window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(200, 100)
        window.set_title("Skapa uppdrag")
        window.connect("delete_event", lambda w,e: gtk.main_quit())
        hscrollbar = gtk.HSscrollbar(adjustment=None)
        window.add(hscrollbar)
        hscrollbar.show()


        vbox = gtk.VBox(False, 0)
        window.add(vbox)
        vbox.show()
        
        label, event_entry = self.new_entry("Handelse")
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(event_entry, True, True, 0)
        
        label, location_entry = self.new_entry("Skadeplats")
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(location_entry, True, True, 0)
        
        label, hurted_entry = self.new_entry("Antal skadade")
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(hurted_entry, True, True, 0)
        
        label, contact_entry = self.new_entry("Kontaktperson(Namn & Nummer)")
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(contact_entry, True, True, 0)
        
        label, random_entry = self.new_entry("Ovrig information")
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(random_entry, True, True, 0)
        
        label, random_entry = self.new_entry("Ovrig information")
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(random_entry, True, True, 0)
        
        label, random_entry = self.new_entry("Ovrig information")
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(random_entry, True, True, 0)
        
        label, random_entry = self.new_entry("Ovrig information")
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(random_entry, True, True, 0)
        
        #In med HANDELS-LABEL
#        handelseLabel = gtk.Label("Handelse")
#        vbox.pack_start(handelseLabel, True, True, 0)
#        handelseLabel.show()
#        handelse = gtk.Entry()
#        handelse.set_max_length(50)
#        handelse.connect("activate", self.enter_callback, handelse)
#        handelse.set_text("")
#        handelse.select_region(0, len(handelse.get_text()))
#        vbox.pack_start(handelse, True, True, 0)
#        handelse.show()
        #In med SKADEPLATS-LABEL
#        platsLabel = gtk.Label("Skadeplats")
#        vbox.pack_start(platsLabel, True, True, 0)
#        platsLabel.show()
#        skadeplats = gtk.Entry()
#        skadeplats.set_max_length(50)
#        skadeplats.connect("activate", self.enter_callback, skadeplats)
#        skadeplats.set_text("")
#        skadeplats.select_region(0, len(skadeplats.get_text()))
#        vbox.pack_start(skadeplats, True, True, 0)
#        skadeplats.show()

        hbox = gtk.HBox(False, 0)
        vbox.add(hbox)
        hbox.show()
                                                                
        button = gtk.Button(stock=gtk.STOCK_CLOSE)
        button.connect("clicked", lambda w: gtk.main_quit())
        vbox.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()
        window.show()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    EntryExample()
    main()
