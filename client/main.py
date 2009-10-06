#!/usr/bin/env python
# coding: utf-8
import gtk
import hildon
import gobject

import gui.mapgui
import gui.testscreen
import gui.missionscreen

class ClientGui(hildon.Program):
    screens = {}

    def __init__(self):
        hildon.Program.__init__(self)
        self.window = hildon.Window()
        self.window.set_title("ClientGui")
        self.window.set_size_request(200, 200)

        self.add_window(self.window)

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(0)
        self.window.add(self.notebook)
        self.create_screens()

        for screen in self.screens.keys():
            print "Adding screen"
            print(screen)
            self.add_screen_to_tab(self.screens[screen])

        self.window.connect("destroy", gtk.main_quit)

    def create_screens(self):
        map_screen = gui.mapgui.MapScreen()
        self.screens['map'] = map_screen

        test_screen = gui.testscreen.TestScreen()
        self.screens['chat'] = test_screen

        mission_screen = gui.missionscreen.MissionScreen()
        self.screens['mission'] = mission_screen

    def add_screen_to_tab(self, screen):
        self.notebook.insert_page(screen)

    def run(self):
        self.window.show_all()
        gtk.main()


# den här borde skapa nya vyer av mission och kartan
if __name__ == "__main__":
    app = ClientGui()
    app.run()
