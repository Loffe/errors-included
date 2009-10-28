# coding: utf-8

import gtk
import map.mapdata
import shared.data
import pygtk
pygtk.require('2.0')
import gui

class MissionScreen(gtk.ScrolledWindow, gui.Screen):
    event_entry = None
    location_entry = None
    hurted_entry = None
    contact_entry = None
    random_entry = None

    def new_entry(self, labeltext):
        label = gtk.Label(labeltext)
#        label.show()
        entry = gtk.Entry()
        entry.set_max_length(100)
        #entry.connect("activate", self.enter_callback, entry)
        entry.set_text("")
        entry.select_region(0, len(entry.get_text()))
#        entry.show()
        return (label, entry)

    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        # create a new window

        table = gtk.Table(10, 2)
        self.add_with_viewport(table)
        table.show()

        y = 0

        label, self.event_entry = self.new_entry("Händelse")
        table.attach(label, 0, 1, y, y+1)
        table.attach(self.event_entry, 1, 2, y, y+1)
        label.hide()
        y+=1

        label, self.location_entry = self.new_entry("Skadeplats")
        table.attach(label, 0, 1, y, y+1)
        table.attach(self.location_entry, 1, 2, y, y+1)
        label.hide()
        y+=1

        label, self.hurted_entry = self.new_entry("Antal skadade")
        table.attach(label, 0, 1, y, y+1)
        table.attach(self.hurted_entry, 1, 2, y, y+1)
        label.hide()
        y+=1

        label, self.contact_entry = self.new_entry("Kontaktperson(Namn & Nummer)")
        table.attach(label, 0, 1, y, y+1)
        table.attach(self.contact_entry, 1, 2, y, y+1)
        label.hide()
        y+=1

        label, self.random_entry = self.new_entry("Övrig information")
        table.attach(label, 0, 1, y, y+1)
        table.attach(self.random_entry, 1, 2, y, y+1)
        label.hide()
        y+=1

        close = gtk.Button(stock=gtk.STOCK_CLOSE)
        close.connect("clicked", gtk.main_quit)
        table.attach(close, 0, 1, y, y+1)
        close.set_flags(gtk.CAN_DEFAULT)
        close.hide()

        ok = gtk.Button(stock=gtk.STOCK_OK)
        ok.connect("clicked", self.add_mission)
        table.attach(ok, 1, 2, y, y+1)
        ok.set_flags(gtk.CAN_DEFAULT)
        ok.show()
        
        table.hide_all()

    def add_mission(self, event):
        mission_data = shared.data.MissionData(self.event_entry.get_text(),
                                               self.location_entry.get_text(),
                                               self.hurted_entry.get_text(),
                                               self.contact_entry.get_text(),
                                               self.random_entry.get_text())

        mission = map.mapdata.Mission(mission_data)

        print "mission created"
