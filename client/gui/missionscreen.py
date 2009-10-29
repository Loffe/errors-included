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
    name_entry = None
    number_entry = None
    random_entry = None

    def new_entry(self, labeltext):
        label = gtk.Label(labeltext)
        entry = gtk.Entry()
        entry.set_max_length(100)
        entry.set_text("")
        entry.select_region(0, len(entry.get_text()))
        
#        entry.show()
        return (label, entry)

    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        # create a new window

        hbox = gtk.HBox(False,2)
        self.add_with_viewport(hbox)
        left_box = gtk.VBox(True,8)
        right_box = gtk.VBox(True,8)
        hbox.add(left_box)
        hbox.add(right_box)
        

        label, self.event_entry = self.new_entry("Händelse")
        left_box.add(label)
        right_box.add(self.event_entry)
        
        label, self.location_entry = self.new_entry("Skadeplats")
        left_box.add(label)
        right_box.add(self.location_entry)

        label, self.hurted_entry = self.new_entry("Antal skadade")
        left_box.add(label)
        right_box.add(self.hurted_entry)
        
        contact = gtk.Label("Kontaktperson:")
        invisible_label = gtk.Label("")
        left_box.add(contact)
        right_box.add(invisible_label)
        
        label, self.name_entry = self.new_entry("Namn")
        left_box.add(label)
        right_box.add(self.name_entry)
        
        label, self.number_entry = self.new_entry("Nummer")
        left_box.add(label)
        right_box.add(self.number_entry)

        label, self.random_entry = self.new_entry("Övrig information")
        left_box.add(label)
        right_box.add(self.random_entry)

        close = gtk.Button(stock=gtk.STOCK_CLOSE)
        close.set_size_request(10,10)
        close.connect("clicked", gtk.main_quit)
        left_box.add(close)
        close.set_flags(gtk.CAN_DEFAULT)

        ok = gtk.Button(stock=gtk.STOCK_OK)
        ok.connect("clicked", self.add_mission)
        right_box.add(ok)
        ok.set_flags(gtk.CAN_DEFAULT)
        
        self.show_all()

    def add_mission(self, event):
        mission_data = shared.data.MissionData(self.event_entry.get_text(),
                                               self.location_entry.get_text(),
                                               self.hurted_entry.get_text(),
                                               self.contact_entry.get_text(),
                                               self.random_entry.get_text())

        mission = map.mapdata.Mission(mission_data)

        print "mission created"
