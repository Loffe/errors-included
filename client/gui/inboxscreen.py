# coding: utf-8

#InboxScreen

import gtk
import gobject
import map.mapdata
import shared.data
import datetime
import gui
import pango

class InboxScreen(gtk.ScrolledWindow, gui.Screen):
    '''
    The screen in which you create a new alarm.
    '''
    # the entries
    event_entry = None
    location_entry = None
    location_entry2 = None
    location_entry3 = None
    hurted_entry = None
    name_entry = None
    number_entry = None
    random_entry = None
    db = None

    def __init__(self, db):
        '''
        Constructor. Create the infoscreen and its entries.
        '''
        gtk.ScrolledWindow.__init__(self)
        self.db = db 

        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        def new_entry(labeltext, parent):
            hbox = gtk.HBox(True, 0)
            label = gtk.Label(labeltext)
            label.set_alignment(0, 0.5)
            #label.modify_font(pango.FontDescription("sans 12"))

            entry = gtk.Label()
            entry.set_alignment(0, 0.5)
            #entry.modify_font(pango.FontDescription("sans 12"))
            entry.select_region(0, len(entry.get_text()))
            hbox.add(label)
            hbox.add(entry)
            parent.add(hbox)
            return entry

        def new_section(title, parent):
            label = gtk.Label(title)
            label.modify_font(pango.FontDescription("sans 12"))
            label.set_alignment(0, 0.5)
            parent.add(label)
#        
        # create layout boxes
        main_box = gtk.VBox(False,0)
        self.add_with_viewport(main_box)
        hbox = gtk.HBox(False,0)
        main_box.pack_start(hbox,True,True,0)
#        
#        # create type label
#        type_label = gtk.Label("Inkomna larm:")
#        type_label.set_alignment(0, 0.5)
#        hbox.pack_start(type_label, True, True, 0)
        
        # create and pack combobox
#        self.combo_box = gtk.combo_box_new_text()
#        self.combo_box.set_size_request(300,50)
#        self.combo_box.append_text("Välj larm...")
#        hbox.pack_start(self.combo_box, True,True, 0)
#        
#        new_section("Nytt uppdrag", main_box)
        
        # create entries
        
       
        self.event_entry = new_entry("Från:", main_box)

        self.location_entry2 = new_entry("amne", main_box)
        self.location_entry3 = new_entry("Innehall", main_box)        
        
        

#        self.select_unit_button = SelectUnitButton(self.db)
#        main_box.add(self.select_unit_button)        
#
#        # add event handler
#        self.combo_box.connect('changed', self.select_alarm)
#
#        # set the first item added as active
#        self.combo_box.set_active(0)

        # show 'em all! (:
        main_box.show_all()

    '''Handle events
    '''

    def select_alarm(self, combobox):
        pass
        '''
        Call when combobox changes to switch obstacle type.
        @param combobox: the changed combobox
        '''
        # set the selected type
#        self.selected_alarm = self.combo_box.get_active_text()
#        alarms = self.db.get_all_alarms()
#        for alarm in alarms:
#            if alarm.event == self.selected_alarm:
#                self.event_entry.set_text(alarm.event)
#                self.location_entry2.set_text(str(alarm.poi.coordx))
#                self.location_entry3.set_text(str(alarm.poi.coordy))                
#                self.name_entry.set_text(alarm.contact_person)
#                self.hurted_entry.set_text(str(alarm.number_of_wounded))
#                self.number_entry.set_text(alarm.contact_number)
#                self.random_entry.set_text(alarm.other)
                

#    