#!/usr/bin/python2.5 

"""
Tests statistics functions

Lauro Moura <lauro.neto@indt.org.br>, 2007
"""

import conic
import dbus
import dbus.glib
import gobject

counter = 0
loop = None
iap_id = None

def request_statistics(connection):
    global counter, loop
    print "request_statistics():"
    
    if counter >= 10:
        print "Max counter reached (%i), quitting", counter
        loop.quit()
        return True
        
    counter += 1
    connection.statistics(iap_id)
    
    return True    


def statistics_cb(connection, event, data):
    print "statistics(%s, %s, %x)" % (connection, event, data)
    
    print "time active=%i" % event.get_time_active()
    print "signal_strength=%i" % event.get_signal_strength()
    print "rx_packets=%u" % event.get_rx_packets()
    print "tx_packets=%u" % event.get_tx_packets()
    print "rx_bytes=%u" % event.get_rx_bytes()
    print "tx_bytes=%u" % event.get_tx_bytes()


def start():
    print "start():"
    connection = conic.Connection()
    connection.connect("connection-event", connection_cb, 0xFFAA)
    connection.connect("statistics", statistics_cb, 0x55AA)
    connection.request_connection(conic.CONNECT_FLAG_NONE)
    
    return False

    
def connection_cb(connection, event, data):
    global iap_id
    
    print "connection_cb(%s, %s, %x)" % (connection, event, data)

    status = event.get_status()
    error = event.get_error()
    iap_id = event.get_iap_id()
    bearer = event.get_bearer_type()
    
    if status == conic.STATUS_CONNECTED:
        print "1: (CONNECTED (%s, %s, %i, %i)" % (iap_id, bearer, status, error)
        gobject.timeout_add(10000, request_statistics, connection)
    elif status == conic.STATUS_DISCONNECTED:
        print "1: (DISCONNECTED (%s, %s, %i, %i)" % (iap_id, bearer, status, error)
    elif status == conic.STATUS_DISCONNECTING:
        print "1: (DISCONNECTING (%s, %s, %i, %i)" % (iap_id, bearer, status, error)
   

if __name__ == "__main__":
    loop = gobject.MainLoop()
    bus = dbus.SystemBus(private=True)
    
    gobject.idle_add(start)
    loop.run()
