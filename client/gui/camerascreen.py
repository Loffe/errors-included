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
        self.button = gtk.Button("Lägg på")
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
        
#        bus2 = self.sender.get_bus()
#        bus2.add_signal_watch()
#        bus2.enable_sync_message_emission()
#        bus2.connect("message", self.on_message)
#        bus2.connect("sync-message::element", self.on_sync_message)
    def start_audio_send(self,ip,port):
#        sink = "dsppcmsink "
#        srcsink = "dsppcmsrc"
#        pout_r, pout_w = os.pipe()
#        pin_r, pin_w = os.pipe()
#    
#        pipeline_out = "fdsrc fd=%d ! audio/x-raw-int,endianness=(int)1234,width=(int)16,depth=(int)16,signed=(boolean)true,channels=(int)1,rate=(int)8000"\
#            " ! %s" % (pout_r, sink)
#    
#        pipeline_in = "%s ! audioconvert ! audio/x-raw-int,endianness=(int)1234,width=(int)16,depth=(int)16,signed=(boolean)true,channels=(int)1,rate=(int)8000"\
#            " ! fdsink fd=%d" % (srcsink, pin_w)
#            
#        pipeline_out = gst.parse_launch(pipeline_out)
#        pipeline_in = gst.parse_launch(pipeline_in)
#        pipeline_out.set_state(gst.STATE_PLAYING)
#        pipeline_in.set_state(gst.STATE_PLAYING)
        
        #self.sender = gst.parse_launch("dsppcmsrc ! audio/x-raw-int,endianness=(int)1234,width=(int)16,depth=(int)16,signed=(boolean)true,channels=(int)1,rate=(int)8000 ! udpsink host="+str(ip)+" port="+str(port))
        #self.player = gst.parse_launch("udpsrc port="+self.MYPORT+" ! audio/x-iLBC,rate=8000,channels=1,mode=20 ! dspilbcsink")
        self.audio_sender = gst.parse_launch("dspilbcsrc dtx=0 ! audio/x-iLBC,rate=8000,channels=1,mode=20 ! udpsink host="+str(ip)+" port="+str(port))
        bus = self.audio_sender.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)


    def start_audio_recv(self,port):
        '''
        Starts an audio server
        @param myIp
        @param port
        '''

#       #self.sender = gst.parse_launch("dsppcmsrc ! audio/x-raw-int,endianness=(int)1234,width=(int)16,depth=(int)16,signed=(boolean)true,channels=(int)1,rate=(int)8000 ! udpsink host="+str(ip)+" port="+str(port))
        #self.player = gst.parse_launch("udpsrc port="+self.MYPORT+" ! audio/x-iLBC,rate=8000,channels=1,mode=20 ! dspilbcsink")
        self.audio_recv = gst.parse_launch("udpsrc port="+str(port)+" ! audio/x-iLBC,rate=8000,channels=1,mode=20 ! dspilbcsink")
        bus1 = self.audio_recv.get_bus()
        bus1.add_signal_watch()
        bus1.enable_sync_message_emission()
        bus1.connect("message", self.on_message)
        bus1.connect("sync-message::element", self.on_sync_message)
    
    
    def start_video_send(self, ip,port):
        print ip
        #Stream to another device
        self.video_sender = gst.parse_launch("v4l2src ! video/x-raw-yuv,width=320,height=240,framerate=8/1 ! hantro4200enc ! rtph263pay ! udpsink host="+str(ip)+" port="+str(port))
        
        #Show the incoming video
        #self.player = gst.parse_launch("udpsrc port=5432 caps=application/x-rtp,clock-rate=90000 ! rtph263depay ! hantro4100dec ! xvimagesink")
        
        #Stream both audio and video
#        self.player = gst.parse_launch("v4l2src ! video/x-raw-yuv,width=320,height=240,framerate=15/1 ! hantro4200enc stream-type=1 profile-and-level=1001 !video/x-h263,framerate=15/1 ! rtph263ppay mtu=1438 ! udpsink host=130.236.219.107 port=5434 dsppcmsrc ! queue ! audio/x-raw-int,channels=1,rate=8000 ! mulawenc ! rtppcmupay mtu=1438 ! udpsink host=130.236.219.107 port=5432")
            #Even try rate=48000
        
        # Show my webcam
        #self.player = gst.parse_launch ("v4l2src ! video/x-raw-yuv, width=320, height=240, framerate=8/1 ! autovideosink")

        bus2 = self.video_sender.get_bus()
        bus2.add_signal_watch()
        bus2.enable_sync_message_emission()
        bus2.connect("message", self.on_message)
        bus2.connect("sync-message::element", self.on_sync_message)
        
    def start_video_recv(self,port):
        #Show the incoming video
        self.video_recv = gst.parse_launch("udpsrc port="+str(port)+ " caps=application/x-rtp,clock-rate=90000 ! rtph263depay ! hantro4100dec ! xvimagesink")
        
        #Stream both audio and video
#        self.player = gst.parse_launch("v4l2src ! video/x-raw-yuv,width=320,height=240,framerate=15/1 ! hantro4200enc stream-type=1 profile-and-level=1001 !video/x-h263,framerate=15/1 ! rtph263ppay mtu=1438 ! udpsink host=130.236.219.107 port=5434 dsppcmsrc ! queue ! audio/x-raw-int,channels=1,rate=8000 ! mulawenc ! rtppcmupay mtu=1438 ! udpsink host=130.236.219.107 port=5432")
            #Even try rate=48000
        
        # Show my webcam
        #self.player = gst.parse_launch ("v4l2src ! video/x-raw-yuv, width=320, height=240, framerate=8/1 ! autovideosink")

        bus3 = self.video_recv.get_bus()
        bus3.add_signal_watch()
        bus3.enable_sync_message_emission()
        bus3.connect("message", self.on_message)
        bus3.connect("sync-message::element", self.on_sync_message)
        
        
    def start_stop(self, w):
        if self.button.get_label() == "Start":
            self.button.set_label("Stop")
            self.audio_sender.set_state(gst.STATE_PLAYING)
            self.video_sender.set_state(gst.STATE_PLAYING)
            self.video_recv.set_state(gst.STATE_PLAYING)
            self.audio_recv.set_state(gst.STATE_PLAYING)
        else:
            self.audio_sender.set_state(gst.STATE_NULL)
            self.video_sender.set_state(gst.STATE_NULL)
            self.video_recv.set_state(gst.STATE_NULL)
            self.audio_recv.set_state(gst.STATE_NULL)
            self.button.set_label("Start")


    def exit(self, widget, data=None):
        gtk.main_quit()

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.audio_sender.set_state(gst.STATE_NULL)
            self.video_sender.set_state(gst.STATE_NULL)
            self.audio_recv.set_state(gst.STATE_NULL)
            self.video_recv.set_state(gst.STATE_NULL)
            self.button.set_label("Start")
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
#            self.player.set_state(gst.STATE_NULL)
            self.audio_sender.set_state(gst.STATE_NULL)
            self.video_sender.set_state(gst.STATE_NULL)
            self.audio_recv.set_state(gst.STATE_NULL)
            self.video_recv.set_state(gst.STATE_NULL)
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


