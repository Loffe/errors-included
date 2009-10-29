#!/usr/bin/env python
# coding: utf-8
import gtk
import hildon
import gobject

import gui.mapgui
import gui.testscreen
import gui.missionscreen


class ClientGui(hildon.Program):

    def show_mission(self,event):
        self.show(["map", "mission_menu"])
        
    def show_add_object(self, event):
        self.show(["map","add_object_menu"])
        #self.map.show()
        #self.menu_add.show_all()
        #self.new_larm.hide_all()
    
    def show_send_screen(self,event):
        pass
#        print "Visar skicka-sidan"
#        self.show([])
        
    def show_inkorg(self, event):
        pass
#        print "Visar inkorgen"
#        self.show([])
        
    def report_larm(self, event):
        pass
#        self.show([1])

    def show(self, keys):
        for key in self.screens.keys():
            self.screens[key].hide_all()
        for key in keys:
            self.screens[key].show_all()
            
    def show_default(self):
        for key in self.screens.keys():
            self.screens[key].hide_all()
        self.map.show()

    def __init__(self):
        hildon.Program.__init__(self)
        self.window = hildon.Window()
        self.window.set_title("ClientGui")
        self.window.set_size_request(200, 200)

        self.add_window(self.window)

        # A list containing all the containers (used for hiding/showing) 
        self.screens = {}

        # Panels
        panels = gtk.HBox(False, 2)
        self.window.add(panels)
        
        # Left menu
        vbox = gtk.VBox(False,5)
        panels.add(vbox)

        # Buttons (menu)
        mission_button = gtk.ToggleButton("Uppdrag")
        mission_button.connect("clicked", self.show_mission)

        add_object_button = gtk.ToggleButton("Skapa")
        add_object_button.connect("clicked", self.show_add_object)

        send_button = gtk.ToggleButton("Kontakt")
        send_button.connect("clicked", self.show_send_screen)

        inbox_button = gtk.ToggleButton("Meddelande")
        inbox_button.connect("clicked", self.show_inkorg)
        
        vbox.add(mission_button)
        vbox.add(add_object_button)
        vbox.add(send_button)
        vbox.add(inbox_button)

        # Right panel
        vbox_right = gtk.VBox(False, 2)
        panels.add(vbox_right)

        self.map = gui.mapgui.MapScreen()
        self.map.set_size_request(550,300)
        vbox_right.add(self.map)
        self.screens["map"] = self.map
        
        self.mission = gui.missionscreen.MissionScreen()
        self.mission.set_size_request(550,300)
        vbox_right.add(self.mission)
        self.screens["mission"] = self.mission
        
        # Mission buttons
        self.mission_menu = gtk.HBox(False, 4)
        info_button = gtk.Button("Info")
#        info_button.connect("clicked", self.report_larm)
        status_button = gtk.Button("Status")
        journal_button = gtk.Button("Patient\nJournal")
        faq_button = gtk.Button("FAQ")
        self.mission_menu.add(info_button)
        self.mission_menu.add(status_button)
        self.mission_menu.add(journal_button)
        self.mission_menu.add(faq_button)
        
        vbox_right.add(self.mission_menu)
        self.screens["mission_menu"] = self.mission_menu

        # Add object buttons
        self.add_object_menu = gtk.HBox(False, 3)
        create_alarm_button = gtk.Button("Larm")
        create_alarm_button.connect("clicked", self.report_larm)
        create_obstacle_button = gtk.Button("Hinder")
        create_mission_button = gtk.Button("Uppdrag")
        self.add_object_menu.add(create_alarm_button)
        self.add_object_menu.add(create_obstacle_button)
        self.add_object_menu.add(create_mission_button)

        vbox_right.add(self.add_object_menu)
        self.screens["add_object_menu"] = self.add_object_menu

        self.window.connect("destroy", gtk.main_quit)
        self.window.connect("key-press-event", self.on_key_press)
        self.window.connect("window-state-event", self.on_window_state_change)

        # Change to default True?
        self.window_in_fullscreen = False

    def on_key_press(self, widget, event, *args):
        # react on fullscreen button press
        if event.keyval == gtk.keysyms.F6:
            if self.window_in_fullscreen:
                self.window.unfullscreen()
            else:
                self.window.fullscreen()
        # Zoom -
        if event.keyval == gtk.keysyms.F8:
            self.map.zoom("-")
        # Zoom +
        elif event.keyval == gtk.keysyms.F7:
            self.map.zoom("+")  

    def on_window_state_change(self, widget, event, *args):
        if event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN:
            self.window_in_fullscreen = True
        else:
            self.window_in_fullscreen = False  

    def run(self):
        self.window.show_all()
        self.show_default()
        gtk.main()

# den här borde skapa nya vyer av mission och kartan
if __name__ == "__main__":
    app = ClientGui()
    app.run()
