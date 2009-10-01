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
#        hscrollbar = gtk.HSscrollbar(adjustment=None)
#        window.add(hscrollbar)
#        hscrollbar.show()
        swindow = gtk.ScrolledWindow()
        swindow.show()
        window.add(swindow)

        table = gtk.Table(10, 2)
        swindow.add_with_viewport(table)
        table.show()
        
        y = 0
        label, event_entry = self.new_entry("Handelse")
        table.attach(label, 0, 1, y, y+1)
        table.attach(event_entry, 1, 2, y, y+1)
        y+=1
        
        label, location_entry = self.new_entry("Skadeplats")
        table.attach(label, 0, 1, y, y+1)
        table.attach(location_entry, 1, 2, y, y+1)
        y+=1
        
        label, hurted_entry = self.new_entry("Antal skadade")
        table.attach(label, 0, 1, y, y+1)
        table.attach(hurted_entry, 1, 2, y, y+1)
        y+=1
        
        label, contact_entry = self.new_entry("Kontaktperson(Namn & Nummer)")
        table.attach(label, 0, 1, y, y+1)
        table.attach(contact_entry, 1, 2, y, y+1)
        y+=1
        
        label, random_entry = self.new_entry("Ovrig information")
        table.attach(label, 0, 1, y, y+1)
        table.attach(random_entry, 1, 2, y, y+1)
        y+=1
        
        label, random_entry = self.new_entry("Ovrig information")
        table.attach(label, 0, 1, y, y+1)
        table.attach(random_entry, 1, 2, y, y+1)
        y+=1
        
        label, random_entry = self.new_entry("Ovrig information")
        table.attach(label, 0, 1, y, y+1)
        table.attach(random_entry, 1, 2, y, y+1)
        y+=1
        
        label, random_entry = self.new_entry("Ovrig information")
        table.attach(label, 0, 1, y, y+1)
        table.attach(random_entry, 1, 2, y, y+1)
        y+=1
        
        label, random_entry = self.new_entry("Ovrig information")
        table.attach(label, 0, 1, y, y+1)
        table.attach(random_entry, 1, 2, y, y+1)
        y+=1
        
        
        label, random_entry = self.new_entry("Ovrig information")
        table.attach(label, 0, 1, y, y+1)
        table.attach(random_entry, 1, 2, y, y+1)
        y+=1
        
        
        label, random_entry = self.new_entry("Ovrig information")
        table.attach(label, 0, 1, y, y+1)
        table.attach(random_entry, 1, 2, y, y+1)
        y+=1
        
        
        label, random_entry = self.new_entry("Ovrig information")
        table.attach(label, 0, 1, y, y+1)
        table.attach(random_entry, 1, 2, y, y+1)
        y+=1
        
        
        label, random_entry = self.new_entry("Ovrig information")
        table.attach(label, 0, 1, y, y+1)
        table.attach(random_entry, 1, 2, y, y+1)
        y+=1
        
        
        label, random_entry = self.new_entry("Ovrig information")
        table.attach(label, 0, 1, y, y+1)
        table.attach(random_entry, 1, 2, y, y+1)
        y+=1
        
        
        label, random_entry = self.new_entry("Ovrig information")
        table.attach(label, 0, 1, y, y+1)
        table.attach(random_entry, 1, 2, y, y+1)
        y+=1
        
        label, random_entry = self.new_entry("Ovrig information")
        table.attach(label, 0, 1, y, y+1)
        table.attach(random_entry, 1, 2, y, y+1)
        y+=1
        
        label, random_entry = self.new_entry("Ovrig information")
        table.attach(label, 0, 1, y, y+1)
        table.attach(random_entry, 1, 2, y, y+1)
        y+=1
        

                                                                
        close = gtk.Button(stock=gtk.STOCK_CLOSE)
        close.connect("clicked", lambda w: gtk.main_quit())
        table.attach(close, 0, 1, y, y+1)
        close.set_flags(gtk.CAN_DEFAULT)
        close.grab_default()
        close.show()
        
        ok = gtk.Button(stock=gtk.STOCK_OK)
        ok.connect("clicked", lambda w: gtk.main_quit())
        table.attach(ok, 1, 2, y, y+1)
        ok.set_flags(gtk.CAN_DEFAULT)
        ok.grab_default()
        ok.show()
        window.show()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    EntryExample()
    main()
