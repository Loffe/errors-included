#!/usr/bin/env python
# coding: utf-8
import gtk
import hildon
import gobject

import gui.mapgui
import gui.testscreen
import gui.missionscreen


class ClientGui(hildon.Program):
        
    def show_map(self,event):
        print "Showing map"
        self.show([0])
        
    def show_mission(self,event):
        print "Showing mission"
        self.show([1])
        
    def add_create_buttons(self, event):
        self.show([0,2])
        #self.map.show()
        #self.menu_add.show_all()
        #self.new_larm.hide_all()
        print "Pushed Add Object button"
    
    def show_send_screen(self,event):
        print "Visar skicka-sidan"
        self.show([])
        
    def show_inkorg(self, event):
        print "Visar inkorgen"
        self.show([])
        
    def report_larm(self, event):
        self.show([1])
        
    
    def show(self, indexes):
        for screen in self.screens:
#            screen.hide()
            screen.hide_all()
        for i in indexes:
            self.screens[i].show_all()

    def __init__(self):
        hildon.Program.__init__(self)
        self.window = hildon.Window()
        self.window.set_title("ClientGui")
        self.window.set_size_request(200, 200)

        self.add_window(self.window)

        # A list containing all the containers (used for hiding/showing) 
        self.screens = []

        # Panels
        panels = gtk.HBox(False, 2)
        self.window.add(panels)
        
        # Left menu
        vbox = gtk.VBox(False,5)
        panels.add(vbox)

        # Buttons (menu)
        map_button = gtk.Button("Karta")
        map_button.connect("clicked", self.show_map)

        mission_button = gtk.Button("Uppdrag")
        mission_button.connect("clicked", self.show_mission)

        add_object_button = gtk.Button("Lägg till")
        add_object_button.connect("clicked", self.add_create_buttons)

        send_button = gtk.Button("Skicka")
        send_button.connect("clicked", self.show_send_screen)

        inbox_button = gtk.Button("Inkorg")
        inbox_button.connect("clicked", self.show_inkorg)
        
        vbox.add(map_button)
        vbox.add(mission_button)
        vbox.add(add_object_button)
        vbox.add(send_button)
        vbox.add(inbox_button)
        
#        self.all.append(map_button)
#        self.all.append(mission_button)
#        self.all.append(add_object_button)
#        self.all.append(send_button)
#        self.all.append(inbox_button)
        
#        self.buttons.append(vbox.get_children())

        # Right panel
        vbox_right = gtk.VBox(False, 2)
        panels.add(vbox_right)

        self.map = gui.mapgui.MapScreen()
        self.map.set_size_request(550,300)
        vbox_right.add(self.map)
        self.screens.append(self.map)
#        self.containers.append(self.map)
        
        self.new_larm = gui.missionscreen.MissionScreen()
        self.new_larm.set_size_request(550,300)
        vbox_right.add(self.new_larm)
        self.screens.append(self.new_larm)
#        self.containers.append(self.new_larm)

        # Add object buttons
        self.menu_add = gtk.HBox(False, 3)
        self.larm = gtk.Button("Larm")
        self.larm.connect("clicked", self.report_larm)
        self.hinder = gtk.Button("Hinder")
        self.poi = gtk.Button("PoI")
        self.menu_add.add(self.larm)
        self.menu_add.add(self.hinder)
        self.menu_add.add(self.poi)
#        self.menu_add.hide_all()
        
        vbox_right.add(self.menu_add)
        self.screens.append(self.menu_add)
#        self.buttons = []
#        self.buttons.append(self.menu_add.get_children())
        
#        self.window.show_all()

        self.window.connect("destroy", gtk.main_quit)

        self.window.connect("key-press-event", self.on_key_press)
        self.window.connect("window-state-event", self.on_window_state_change)
        self.window_in_fullscreen = False

    def on_key_press(self, widget, event, *args):
        # react on fullscreen button press
        if event.keyval == gtk.keysyms.F6:
            if self.window_in_fullscreen:
                self.window.unfullscreen()
            else:
                self.window.fullscreen()

    def on_window_state_change(self, widget, event, *args):
        if event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN:
            self.window_in_fullscreen = True
        else:
            self.window_in_fullscreen = False

    def run(self):
        self.window.show_all()
        self.menu_add.hide_all()
        self.new_larm.hide_all()
        gtk.main()

# den här borde skapa nya vyer av mission och kartan
if __name__ == "__main__":
    app = ClientGui()
    app.run()
