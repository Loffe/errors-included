# coding: utf-8
#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
try:
    import pygst
    pygst.require("0.10")
    import gst
except:
    class gst(object):
        pass
import shared.data
import gui
import clientgui

class CamScreen(gtk.ScrolledWindow, gui.Screen):

    video_started = False

    def __init__(self,db):
        gtk.ScrolledWindow.__init__(self)
        # set automatic horizontal and vertical scrolling
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        vbox = gtk.VBox()
        self.add_with_viewport(vbox)
        self.movie_window = gtk.DrawingArea()
        vbox.add(self.movie_window)
        hbox = gtk.HBox()
        vbox.pack_start(hbox, False)
        hbox.set_border_width(10)
        hbox.pack_start(gtk.Label())
        self.button = gtk.Button("Stop")
        self.button.connect("clicked", self.stop)
        hbox.pack_start(self.button, False)

        hbox.add(gtk.Label())
        self.show_all()

    def start_audio_send(self,ip,port):

        self.audio_sender = gst.parse_launch("dspilbcsrc dtx=0 ! audio/x-iLBC,rate=8000,channels=1,mode=20 ! udpsink host="+str(ip)+" port= "+str(port))
        bus = self.audio_sender.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)
        self.audio_sender.set_state(gst.STATE_PLAYING)


    def start_audio_recv(self,port):
        '''
        Starts an audio server
        @param myIp
        @param port
        '''

        self.audio_recv = gst.parse_launch("udpsrc port="+str(port)+" ! audio/x-iLBC,rate=8000,channels=1,mode=20 ! dspilbcsink")
        bus1 = self.audio_recv.get_bus()
        bus1.add_signal_watch()
        bus1.enable_sync_message_emission()
        bus1.connect("message", self.on_message)
        bus1.connect("sync-message::element", self.on_sync_message)
        self.audio_recv.set_state(gst.STATE_PLAYING)
    
    
    def start_video_send(self, ip,port):
        print ip
        #Stream to another device
        self.video_sender = gst.parse_launch("v4l2src ! video/x-raw-yuv,width=320,height=240,framerate=8/1 ! hantro4200enc ! rtph263pay ! udpsink host="+str(ip)+" port="+str(port))

        bus2 = self.video_sender.get_bus()
        bus2.add_signal_watch()
        bus2.enable_sync_message_emission()
        bus2.connect("message", self.on_message)
        bus2.connect("sync-message::element", self.on_sync_message)
        self.video_sender.set_state(gst.STATE_PLAYING)
        
        
    def start_video_recv(self,port):
        #Show the incoming video
        self.video_recv = gst.parse_launch("udpsrc port="+str(port)+ " caps=application/x-rtp,clock-rate=90000 ! rtph263depay ! hantro4100dec ! xvimagesink")

        bus3 = self.video_recv.get_bus()
        bus3.add_signal_watch()
        bus3.enable_sync_message_emission()
        bus3.connect("message", self.on_message)
        bus3.connect("sync-message::element", self.on_sync_message)
        self.video_recv.set_state(gst.STATE_PLAYING)
        
        
    def start_vvoip(self,ip,port1,port2):
            self.start_audio_recv(port1)
            self.start_audio_send(ip, port1)
            self.start_video_recv(port2)
            self.start_video_send(ip, port2)
            self.video_started = True            
            
    def start_voip(self, ip, port):
            self.start_audio_recv(port) #5432 ?
            self.start_audio_send(ip,port)          
 
    def stop(self,w):
        if self.video_started:
            self.audio_sender.set_state(gst.STATE_NULL)
            self.video_sender.set_state(gst.STATE_NULL)
            self.video_recv.set_state(gst.STATE_NULL)
            self.audio_recv.set_state(gst.STATE_NULL)
            self.video_started = False         
        else:
            self.audio_sender.set_state(gst.STATE_NULL)
            self.audio_recv.set_state(gst.STATE_NULL)

    def exit(self, widget, data=None):
        gtk.main_quit()

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            if self.video_started:
                self.audio_sender.set_state(gst.STATE_NULL)
                self.video_sender.set_state(gst.STATE_NULL)
                self.video_recv.set_state(gst.STATE_NULL)
                self.audio_recv.set_state(gst.STATE_NULL)         
            else:
                self.audio_sender.set_state(gst.STATE_NULL)
                self.audio_recv.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug

            if self.video_started:
                self.audio_sender.set_state(gst.STATE_NULL)
                self.video_sender.set_state(gst.STATE_NULL)
                self.video_recv.set_state(gst.STATE_NULL)
                self.audio_recv.set_state(gst.STATE_NULL)         
            else:
                self.audio_sender.set_state(gst.STATE_NULL)
                self.audio_recv.set_state(gst.STATE_NULL)

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


