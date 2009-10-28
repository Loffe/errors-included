#!/usr/bin/env python
# coding: utf-8
import gtk
import hildon
import gobject

import gui.mapgui
import gui.testscreen
import gui.missionscreen
import gui.creategui

class ClientGui(hildon.Program):
    

    def __init__(self):
        hildon.Program.__init__(self)
        self.window = hildon.Window()
        self.window.set_title("ClientGui")
        self.window.set_size_request(200, 200)

        self.add_window(self.window)
        
        hbox = gtk.HBox(False, 3)
        vbox = gtk.VBox(False,5)
        hbox.add(vbox)
        karta = gtk.Button("Karta")
        uppdrag = gtk.Button("Uppdrag")
        lagg_till = gtk.Button("Lägg till")
        skicka = gtk.Button("Skicka")
        inkorg = gtk.Button("Inkorg")
        map = gui.mapgui.MapScreen()
        map.set_size_request(550,200)
        hbox.add(map)
        vbox.add(karta)
        vbox.add(uppdrag)
        vbox.add(lagg_till)
        vbox.add(skicka)
        vbox.add(inkorg)

        self.window.add(hbox)
        
        self.window.show_all()

        self.window.connect("destroy", gtk.main_quit)


    def run(self):
        self.window.show_all()
        gtk.main()


# den här borde skapa nya vyer av mission och kartan
if __name__ == "__main__":
    app = ClientGui()
    app.run()
