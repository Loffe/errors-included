#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared.data
import dbus
import dbus.mainloop.glib
import gobject
import datetime

class ClientController(object):
    '''
    Self. This is me. Holds my name, unit_type, status and gps-coordinates.
    '''
    def __init__(self, name, unit_type, status, db):
        '''
        Constructor. Creates a client controller.
        @param name: my name.
        @param unit_type: my unit type.
        @param status: my status.
        @param db: the database to save to.
        '''
        # create dbus session
        bus = dbus.SessionBus()
        remote_object = bus.get_object("included.errors.QoSManager", "/QoSManager")
        interface = dbus.Interface(remote_object, "included.errors.QoSManager")
        # listen to QoSManagers signaling of new GPS-coordinates
        interface.connect_to_signal("signal_new_gps_coord", self.update_coords)

        # the database to save to
        self.db = db
        # set sender name in db
        self.db.name = name

        # My name
        self.name = name
        # My unit type
        self.unit_type = unit_type
        # My status
        self.status = status
        # My mission
        self.mission = None
        # The unit I am
        self.unit_data = shared.data.UnitData(0, 0, name, datetime.datetime.now(), 
                 unit_type)
        
    def update_coords(self, coordx, coordy):
        '''
        Update my GPS-coordinates.
        @param coordx: the x-coordinate to set.
        @param coordy: the y-coordinate to set.
        '''
        self.unit_data.coordx = coordx
        self.unit_data.coordy = coordy
        self.unit_data.timestamp = datetime.datetime.now()
        print "Got coords update"

#    def run(self):
#        '''
#        Start the mainloop.
#        '''
#        self.dbusloop()
#
#    def dbusloop(self):
#        
#        gobject.threads_init()
#        print "Running ClientController"
#        while self.mainloop.is_running():
#            try:
#                self.mainloop.run()
#            except KeyboardInterrupt:
#                self.mainloop.quit()
#                self.close()

    def close(self):
        print "ClientController aborted"

if __name__ == "__main__":
    name = "Ragnar Dahlberg"
    unit_type = shared.data.UnitType.commander
    status = "Available"
    client = ClientController(name, unit_type, status)
    client.run()
