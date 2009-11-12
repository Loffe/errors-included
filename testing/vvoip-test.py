#!/usr/bin/env python
import sys, os
import pygtk, gtk, gobject
import pygst
from easy import audio
pygst.require("0.10")
import gst

class GTK_Main:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Videosamtal")
        window.set_default_size(500, 400)
        window.connect("destroy", gtk.main_quit, "WM destroy")
        vbox = gtk.VBox()
        window.add(vbox)
        self.movie_window = gtk.DrawingArea()
        vbox.add(self.movie_window)
        hbox = gtk.HBox()
        vbox.pack_start(hbox, False)
        hbox.set_border_width(10)
        hbox.pack_start(gtk.Label())
        self.button = gtk.Button("Start")
        self.button.connect("clicked", self.start_stop)
        hbox.pack_start(self.button, False)
        self.button2 = gtk.Button("Quit")
        self.button2.connect("clicked", self.exit)
        hbox.pack_start(self.button2, False)
        self.button3 = gtk.Button("Audio")
        self.button3.connect("clicked", self.audio)
        hbox.pack_start(self.button3, False)
        hbox.add(gtk.Label())
        window.show_all()
        print "Button 3"
        options = "v4l2src ! video/x-raw-yuv, width=320, height=240, framerate=20/1 ! autovideosink"
        self.player = gst.parse_launch ( options )
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)
        
    def start_stop(self, w):
        if self.button.get_label() == "Start":
            self.button.set_label("Stop")
            self.player.set_state(gst.STATE_PLAYING)
        else:
            self.player.set_state(gst.STATE_NULL)
            self.button.set_label("Start")
            
    def exit(self, widget, data=None):
        gtk.main_quit()
        
    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.button.set_label("Start")
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.player.set_state(gst.STATE_NULL)
            self.button.set_label("Start")
            
    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", False)
            imagesink.set_xwindow_id(self.movie_window.window.xid)
    
#    def play_moby(self):
#        playbin = gst.element_factory_make("playbin", "my-playbin")
        
    def audio(self):
        audio.record("hello_world.wav", 3)
        audio.set_volume(5)
        audio.play("hello_world.wav")
        
GTK_Main()
gtk.gdk.threads_init()
gtk.main()