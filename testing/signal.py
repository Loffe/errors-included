#!/usr/bin/python2.5 

"""
Tests statistics functions

Lauro Moura <lauro.neto@indt.org.br>, 2007
"""

import dbus
#from dbus.mainloop.glib import DBusGMainLoop
import gobject
import conic
import struct
import binascii

class Signal(object):
    def __init__(self):
#        DBusGMainLoop(set_as_default=True)
        self.iap_id = None
        self.wlan = None

    def request_statistics(self, connection):
        print "request_statistics():"
        
        self.wlan.statistics(self.iap_id)
        
        return True    


    def statistics_cb(self, connection, event, data):

        hex = "%x"%event.get_signal_strength()
        signal_strength = 0
        try:
            signal_strength = struct.unpack('!i', binascii.unhexlify(hex))[0]
        except TypeError:
            print "Disconnected"
        
        print "time active=%i" % event.get_time_active()
        print "signal_strength=%i" % event.get_signal_strength()
        print "signalstrength dB=", signal_strength
        print "rx_packets=%u" % event.get_rx_packets()
        print "tx_packets=%u" % event.get_tx_packets()
        print "rx_bytes=%u" % event.get_rx_bytes()
        print "tx_bytes=%u" % event.get_tx_bytes()


    def start(self):
        print "start():"
        self.wlan = conic.Connection()
        self.wlan.connect("connection-event", self.connection_cb, 0xFFAA)
        self.wlan.connect("statistics", self.statistics_cb, 0x55AA)
        self.wlan.request_connection(conic.CONNECT_FLAG_NONE)
        
        return False

    
    def connection_cb(self, connection, event, data):
        
        print "connection_cb(%s, %s, %x)" % (connection, event, data)
    
        status = event.get_status()
        error = event.get_error()
        self.iap_id = event.get_iap_id()
        bearer = event.get_bearer_type()
        
        if status == conic.STATUS_CONNECTED:
            print "1: (CONNECTED (%s, %s, %i, %i)" % (self.iap_id, bearer, status, error)
            gobject.timeout_add(10000, self.request_statistics, connection)
        elif status == conic.STATUS_DISCONNECTED:
            print "1: (DISCONNECTED (%s, %s, %i, %i)" % (self.iap_id, bearer, status, error)
        elif status == conic.STATUS_DISCONNECTING:
            print "1: (DISCONNECTING (%s, %s, %i, %i)" % (self.iap_id, bearer, status, error)
   
if __name__ == "__main__":
    
    loop = gobject.MainLoop()
    
#    bus = dbus.SystemBus(private=True)
    s = Signal()
    gobject.idle_add(s.start)
    loop.run()
