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
        print "Visar karta"
        self.map.show()
        self.menu_add.hide_all()
        self.new_larm.hide_all()
        
    def show_mission(self,event):
        print "Visar mission"
        self.map.hide()
        self.menu_add.hide_all()
        self.new_larm.hide_all()
        
    def add_create_buttons(self, event):
        self.map.show()
        self.menu_add.show_all()
        self.new_larm.hide_all()
        print "Trykte pa lägg till-knappen"
    
    def show_send_screen(self,event):
        print "Visar skicka-sidan"
        self.map.hide()
        self.menu_add.hide_all()
        self.new_larm.hide_all()
        
    def show_inkorg(self, event):
        print "Visar inkorgen"
        self.map.hide()
        self.menu_add.hide_all()
        self.new_larm.hide_all()
        
    def report_larm(self, event):
        self.map.hide()
        self.menu_add.hide_all()
        self.new_larm.show_all()
        
        

    def __init__(self):
        hildon.Program.__init__(self)
        self.window = hildon.Window()
        self.window.set_title("ClientGui")
        self.window.set_size_request(200, 200)

        self.add_window(self.window)

        # Panels
        panels = gtk.HBox(False, 2)
        self.window.add(panels)
        
        # Left menu
        vbox = gtk.VBox(False,5)
        panels.add(vbox)

#        hbox.set_homogeneous(False)
#        vbox.set_homogeneous(False)
        karta = gtk.Button("Karta")
        karta.connect("clicked", self.show_map)
        uppdrag = gtk.Button("Uppdrag")
        uppdrag.connect("clicked", self.show_mission)
        lagg_till = gtk.Button("Lägg till")
        lagg_till.connect("clicked", self.add_create_buttons)
        skicka = gtk.Button("Skicka")
        skicka.connect("clicked", self.show_send_screen)
        inkorg = gtk.Button("Inkorg")
        inkorg.connect("clicked", self.show_inkorg)
        
        vbox.add(karta)
        vbox.add(uppdrag)
        vbox.add(lagg_till)
        vbox.add(skicka)
        vbox.add(inkorg)
        
        # Right panel
        vbox_right = gtk.VBox(False, 2)
        panels.add(vbox_right)
        
        self.map = gui.mapgui.MapScreen()
        self.map.set_size_request(550,300)
        vbox_right.add(self.map)
        
        self.new_larm = gui.missionscreen.MissionScreen()
        self.new_larm.set_size_request(550,300)
        vbox_right.add(self.new_larm)
        

        # Add menu
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
