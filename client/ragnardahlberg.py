#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared.data
import dbus
import dbus.mainloop.glib
import gobject

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
        
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        remote_object = bus.get_object("included.errors.QoSManager", "/QoSManager")
        interface = dbus.Interface(remote_object, "included.errors.QoSManager")
        
        # TODO: Connect to dbus signals, to update gps-pos when QoSManager signals
        interface.connect_to_signal("signal_new_gps_coord", self.update_coords, sender_keyword='included.errors.QoSManager')
        
        self.unit_type = unit_type
        self.mission = None
        self.status = status
        self.coords = (0,0)
        
    def update_coords(self, coords):
        self.coords = coords
        print "Got coords update"
    
    def run(self):
        self.dbusloop()
        
    def dbusloop(self):
        self.mainloop = gobject.MainLoop()
        gobject.threads_init()
        print "Running selfness loop listening to da buzz."
        while self.mainloop.is_running():
            try:
                self.mainloop.run()
            except KeyboardInterrupt:
                self.mainloop.quit()
                self.close()
    
    def close(self):
        print "Selfness aborted"

if __name__ == "__main__":
    unit_type = shared.data.UnitType.commander
    status = "Available"
    client = RagnarDahlberg(unit_type, status)
    client.run()
