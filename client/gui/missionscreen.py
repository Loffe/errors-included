import gtk

import pygtk
pygtk.require('2.0')
import gui

class MissionScreen(gtk.ScrolledWindow, gui.Screen):
    def new_entry(self, labeltext):
        label = gtk.Label(labeltext)
        label.show()
        entry = gtk.Entry()
        entry.set_max_length(100)
        #entry.connect("activate", self.enter_callback, entry)
        entry.set_text("")
        entry.select_region(0, len(entry.get_text()))
        entry.show()
        return (label, entry)

    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        # create a new window

        table = gtk.Table(10, 2)
        self.add_with_viewport(table)
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

        close = gtk.Button(stock=gtk.STOCK_CLOSE)
        close.connect("clicked", lambda w: gtk.main_quit())
        table.attach(close, 0, 1, y, y+1)
        close.set_flags(gtk.CAN_DEFAULT)
        close.show()

        ok = gtk.Button(stock=gtk.STOCK_OK)
        ok.connect("clicked", lambda w: gtk.main_quit())
        table.attach(ok, 1, 2, y, y+1)
        ok.set_flags(gtk.CAN_DEFAULT)
        ok.show()
