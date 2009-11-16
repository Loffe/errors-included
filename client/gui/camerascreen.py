# coding: utf-8
#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst
import shared.data
import gui
import clientgui

class CamScreen(gtk.ScrolledWindow, gui.Screen):

    def __init__(self,db):
        gtk.ScrolledWindow.__init__(self)
        # set automatic horizontal and vertical scrolling
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
#        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
#        window.set_title("Webcam-Viewer")
#        window.set_default_size(500, 400)
#        window.connect("destroy", gtk.main_quit, "WM destroy")
        vbox = gtk.VBox()
        self.add_with_viewport(vbox)
        self.movie_window = gtk.DrawingArea()
        vbox.add(self.movie_window)
        hbox = gtk.HBox()
        vbox.pack_start(hbox, False)
        hbox.set_border_width(10)
        hbox.pack_start(gtk.Label())
        self.button = gtk.Button("Start")
        self.button.connect("clicked", self.start_stop)
        hbox.pack_start(self.button, False)
        #self.button2 = gtk.Button("Quit")
        #self.button2.connect("clicked", self.exit)
       # hbox.pack_start(self.button2, False)
        hbox.add(gtk.Label())
        self.show_all()


        #Listening for Input:
#        gst-launch udpsrc port=5434 caps=application/x-rtp,clock-rate=90000 ! rtph263depay ! hantro4100dec ! xvimagesink

        #Sending Video Output:
#        gst-launch v4l2src ! video/x-raw-yuv,width=352,height=288,framerate=8/1 ! hantro4200enc ! rtph263pay ! udpsink host=<other N800's ip> port=5434 

        #Stream to another device
        #self.sender = gst.parse_launch("v4l2src ! video/x-raw-yuv,width=320,height=240,framerate=8/1 ! hantro4200enc ! rtph263pay ! udpsink host=130.236.219.107 port=5434")
        
        #Show the incoming video
        #self.player = gst.parse_launch("udpsrc port=5432 caps=application/x-rtp,clock-rate=90000 ! rtph263depay ! hantro4100dec ! xvimagesink")
        
        #Stream both audio and video
#        self.player = gst.parse_launch("v4l2src ! video/x-raw-yuv,width=320,height=240,framerate=15/1 ! hantro4200enc stream-type=1 profile-and-level=1001 !video/x-h263,framerate=15/1 ! rtph263ppay mtu=1438 ! udpsink host=130.236.219.107 port=5434 dsppcmsrc ! queue ! audio/x-raw-int,channels=1,rate=8000 ! mulawenc ! rtppcmupay mtu=1438 ! udpsink host=130.236.219.107 port=5432")
            #Even try rate=48000
        
        # Show my webcam
        self.player = gst.parse_launch ("v4l2src ! video/x-raw-yuv, width=320, height=240, framerate=8/1 ! autovideosink")

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)
        
#        bus2 = self.sender.get_bus()
#        bus2.add_signal_watch()
#        bus2.enable_sync_message_emission()
#        bus2.connect("message", self.on_message)
#        bus2.connect("sync-message::element", self.on_sync_message)

    def start_stop(self, w):
       if self.button.get_label() == "Start":
           self.button.set_label("Stop")
           self.player.set_state(gst.STATE_PLAYING)
#           self.sender.set_state(gst.STATE_PLAYING)
       else:
           self.player.set_state(gst.STATE_NULL)
#           self.sender.set_state(gst.STATE_NULL)
           self.button.set_label("Start")

    def exit(self, widget, data=None):
        gtk.main_quit()

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
#            self.sender.set_state(gst.STATE_NULL)
            self.button.set_label("Start")
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.player.set_state(gst.STATE_NULL)
#            self.sender.set_state(gst.STATE_NULL)
            self.button.set_label("Start")

    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            # Assign the viewport
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", False)
            imagesink.set_xwindow_id(self.movie_window.window.xid)


gtk.gdk.threads_init()


