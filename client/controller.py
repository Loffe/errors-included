#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared.data
import dbus
import dbus.mainloop.glib
import gobject

class ClientController(object):
    '''
    Self. This is me. Holds my unit_type, status and gps-coordinates.
    '''
    def __init__(self, unit_type, status):
        '''
        Constructor.
        @param unit_type: my unit type.
        @param status: my status.
        '''
        # create dbus session
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        remote_object = bus.get_object("included.errors.QoSManager", "/QoSManager")
        interface = dbus.Interface(remote_object, "included.errors.QoSManager")
        # listen to QoSManagers signaling of new GPS-coordinates
        interface.connect_to_signal("signal_new_gps_coord", self.update_coords)

        # My unit type
        self.unit_type = unit_type
        # My mission
        self.mission = None
        # My status
        self.status = status
        # My position (GPS-coordinates)
        self.coords = (0,0)

    def update_coords(self, coordx, coordy):
        '''
        Update my GPS-coordinates.
        @param coordx: the x-coordinate to set.
        @param coordy: the y-coordinate to set.
        '''
        self.coords = (coordx, coordy)
        print "Got coords update"

    def run(self):
        '''
        Start the mainloop.
        '''
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
    client = ClientController(unit_type, status)
    client.run()
