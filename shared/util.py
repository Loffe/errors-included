import logging
import subprocess
import re
import time
import wave
try:
    import pygst
    pygst.require("0.10")
    import gst
except:
    class gst(object):
        pass
import gobject, sys
#import pymedia.audio.sound as sound

def getLogger(filename="log.txt"):
    logger = logging.getLogger(filename)
    fh = logging.FileHandler(filename,'w')
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)

    return logger

def get_ip():
    get_ip_command = ["ip", "-f", "inet", "addr"]
    result = subprocess.Popen(get_ip_command, stdout=subprocess.PIPE, close_fds=True).stdout.read()
    regexp = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    ip = re.findall(regexp, result)[1]
    return ip

def set_color(r,g,b):
    try:
        set_mode("direct")
        value = "%X:%X:%X" % (r,g,b)
        FILE = open("/sys/devices/platform/i2c_omap.2/i2c-0/0-0032/color","w")
        FILE.write(value)
        FILE.close()
    except:
        "Couldnt find led"

def set_mode(mode):
    try:
        FILE = open("/sys/devices/platform/i2c_omap.2/i2c-0/0-0032/mode","w")
        FILE.write(mode)
        FILE.close()
    except:
        print "Couldnt fint led"
        
#Parsing wave header is a simple thing using wave module:
def play_sound():
    try:
        f= wave.open( 'snd/mail3b.wav', 'rb' )
        sampleRate= f.getframerate()
        channels= f.getnchannels()
    
        snd= sound.Output( sampleRate, channels, format )
        s= f.readframes( 300000 )
        snd.play( s )
        while snd.isPlaying(): time.sleep( 0.05 )
    except:
        print "Couldnt play sound"
        


def play_uri(uri):
    try:
        player = gst.element_factory_make("playbin", "player")
        
        print 'Playing:', uri
        player.set_property('uri', uri)
        player.set_state(gst.STATE_PLAYING)
        #play_uri("/home/user/tada.wav")
        #pygame.time.delay(5000)
    except:
        print "Couldnt play sound"

        
