#!/usr/bin/python2.5 

"""
Tests statistics functions

Lauro Moura <lauro.neto@indt.org.br>, 2007
"""

import conic
import dbus
import dbus.glib
import gobject
        
connection = conic.Connection()
connection.request_connection(conic.CONNECT_FLAG_NONE)
connection.connect("connection-event", connection_cb, 0xFFAA)


def connection_cb(connection, event, data):
#        print "connection_cb(%s, %s, %x)" % (connection, event, data)
    status = event.get_status()
    if status == conic.STATUS_CONNECTED:
        print "CONNECTED"
    elif status == conic.STATUS_DISCONNECTED:
        print "DISCONNECTED"
    elif status == conic.STATUS_DISCONNECTING:
        print "DISCONNECTING"
        
    print "signal_strength=%i" % event.get_signal_strength()


  
