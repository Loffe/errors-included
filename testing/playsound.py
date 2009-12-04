import pygst
pygst.require('0.10')
import gst
import gobject, sys
import gtk

def play_uri(uri):
    player = gst.element_factory_make("playbin", "player")
    print 'Playing:', uri
    player.set_property('uri', uri)
    player.set_state(gst.STATE_PLAYING)
    
play_uri("snd/mail3b.wav")
gtk.main()