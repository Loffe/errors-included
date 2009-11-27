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
        self.interface = dbus.Interface(remote_object, "included.errors.QoSManager")
        # listen to QoSManagers signaling of new GPS-coordinates
        self.interface.connect_to_signal("signal_new_gps_coord", self.update_coords)
        
        # the database to save to
        self.db = db

        # My name
        self.name = config.client.name
        # My unit type
        self.unit_type = unit_type
        # My status
        self.status = status
        # My missions
        self.missions = []
        # The unit I am (will be set upon login)
        self.unit_data = None

    def update_coords(self, coordx, coordy):
        '''
        Update my GPS-coordinates.
        @param coordx: the x-coordinate to set.
        @param coordy: the y-coordinate to set.
        '''
        if self.unit_data == None:
            return
        self.unit_data.coordx = float(coordx)
        self.unit_data.coordy = float(coordy)
        print "Got coords update", coordx, coordy
        self.unit_data.timestamp = datetime.datetime.now()
        self.db.change(self.unit_data)
    
    def add_mission(self, mission):
        self.missions.append(mission)
        print "got new mission:", type(data), data
