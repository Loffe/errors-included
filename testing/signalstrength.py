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

connection.connect("statistics", statistics_cb, 0x55AA)

connection.request_connection(conic.CONNECT_FLAG_NONE)

print "signal_strength=%i" % event.get_signal_strength()

status = event.get_status()
if status == conic.STATUS_CONNECTED:
    print "CONNECTED"
elif status == conic.STATUS_DISCONNECTED:
    print "DISCONNECTED"
elif status == conic.STATUS_DISCONNECTING:
    print "DISCONNECTING"
   

