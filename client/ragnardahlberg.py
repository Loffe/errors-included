#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared.data
import dbus

class RagnarDahlberg(object):
    '''
    Self. This is me. Holds my unit_type, status and gps-coordinates.
    '''
    def __init__(self, unit_type, status):
        '''
        Constructor.
        @param unit_type: my unit type.
        @param status: my status.
        '''
        self.unit_type = unit_type
        self.status = status
        self.coords = (0,0)
        
        bus = dbus.SessionBus()
        remote_object = bus.get_object("included.errors.QoSManager", "/QoSManager")
        interface = dbus.Interface(remote_object, "included.errors.QoSManager")
        
        # TODO: Connect to dbus signals, to update gps-pos when QoSManager signals
    
    def run(self):
        while True:
            pass

if __name__ == "__main__":
    unit_type = shared.data.UnitType.commander
    status = "Available"
    client = RagnarDahlberg(unit_type, status)
    client.run()