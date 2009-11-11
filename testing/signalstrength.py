#!/usr/bin/python2.5 

"""
Tests statistics functions

Lauro Moura <lauro.neto@indt.org.br>, 2007
"""

import conic
import dbus
import dbus.glib
import gobject
import struct
import binascii

iap_id = None
loop = None

def start():
    print "Start"
    connection = conic.Connection()
    connection.request_connection(conic.CONNECT_FLAG_NONE)
    connection.connect("connection-event", connection_cb, 0xFFAA)
    
def connection_cb(connection, event, data):
    global iap_id
#        print "connection_cb(%s, %s, %x)" % (connection, event, data)
    status = event.get_status()
    iap_id = event.get_iap_id()
    connection.statistics(iap_id)
    if status == conic.STATUS_CONNECTED:
        print "CONNECTED"
    elif status == conic.STATUS_DISCONNECTED:
        print "DISCONNECTED"
    elif status == conic.STATUS_DISCONNECTING:
        print "DISCONNECTING"
        
    x = event.get_signal_strength()
    hex = "%x"%x
    try:
        signal_strength = struct.unpack('!i', binascii.unhexlify(hex))[0]
        print "Signalstyrka", signal_strength
    except TypeError:
        print "Disconnected"


if __name__ == "__main__":
    loop = gobject.MainLoop()
    bus = dbus.SystemBus(private=True)
    gobject.idle_add(start)
    loop.run()



