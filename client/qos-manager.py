# -*- coding: utf-8 -*-
from __future__ import division
import dbus
import dbus.mainloop.glib
import dbus.service
import time
import threading
import gobject
import struct
import binascii
#try:
import conic
#except:
    # Not in N810, no conic module; do nothing...
#    pass
try:
    import gpsbt
except:
    # Not in N810, got no GPS-device; do nothing...
    pass

class QoSManager(dbus.service.Object):
    '''
    This class manages and updates the service level depending on battery level
    and signal strength.
    '''
    def __init__(self):
        '''
        Constructor.
        '''
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.session_bus = dbus.SessionBus()
        self.name = dbus.service.BusName("included.errors.QoSManager", self.session_bus)
        dbus.service.Object.__init__(self, self.session_bus, '/QoSManager')
        self.bus = dbus.SystemBus()
        
        # the service level
        self.service_level = "None"

        # the variables updated by this class
        self.gps_coord = (0,0)
        self.signal_strength = 0
        self.battery_level = 0
        
        # gps update interval (every X seconds)
        self.gps_update_interval = 30
        # try this number of times every time ;P
        self.try_limit = 29
        
        # service level update interval (every X seconds)
        self.service_level_update_interval = 10
        
        # lower service level if under those levels
        self.critical_battery_level = 20
        self.critical_signal_strength = 0
        
        self.running = False
        
        self.iap_id = None
        self.connection = conic.Connection()

    def check_battery_level(self):
        '''
        Update the battery level.
        '''
        hal_obj = self.bus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
        hal = dbus.Interface(hal_obj, 'org.freedesktop.Hal.Manager')
        uids = hal.FindDeviceByCapability('battery')
        dev_obj = self.bus.get_object('org.freedesktop.Hal', uids[0])

        # Battery left (mAh)
        battery_left = dev_obj.GetProperty('battery.reporting.current')
        # Battery lifetime (mAh)
        battery_lifetime = dev_obj.GetProperty('battery.reporting.design')
        # True if charging
        charging = dev_obj.GetProperty('battery.rechargeable.is_charging')
        # Battery left in %
        self.battery_level = battery_left*100/battery_lifetime
        
        # return battery level
        if charging:
            return "charging"
        elif self.battery_level < self.critical_battery_level:
            return "low"
        else:
            return "high"

    def connection_cb(connection, event, data):
        self.iap_id = event.get_iap_id()
        
    def statistics_cb(connection, event, data):
        
        x = event.get_signal_strength()
        hex = "%x"%x
        try:
            self.signal_strength = struct.unpack('!i', binascii.unhexlify(hex))[0]
            print "Signalstyrka", self.signal_strength
        except TypeError:
            self.signal_strength = 0
            print "Disconnected", self.signal_strength            

    # UNSTABLE! DOESN'T DO SHIT!
    def check_signal_strength(self):
        '''
        Update the signal strength.
        '''

        # update the connection stats
        try:
            self.connection.statistics(self.iap_id)
        except:
            pass

        # return signal strength
        if self.signal_strength == None:
            return "offline"
        elif signal_strength < self.critical_signal_strength:
            return "low"
        else:
            return "high"

    def update_gps_coord(self):
        '''
        Update the gps coordinates (own position).
        '''
        # start the GPS
        self.gps_context = gpsbt.start()
        
        # wait for the gps to start (Needed?)
        time.sleep(2)

        # create the device
        gpsdevice = gpsbt.gps()
        
        # get the gps coordinates
        x,y = (0,0)
        tries = 0
        while (x,y) == (0,0):
            x, y = gpsdevice.get_position()
            tries += 1
            if tries >= self.try_limit:
                break
            time.sleep(1)

        # TODO: LIMIT TRIES COUNT?!
        print "tries:", str(tries)

        # Stop the GPS
        gpsbt.stop(self.gps_context)

        # set gps coordinates
        if not (x,y) == (0,0):
            self.gps_coord = (x,y)
            self.signal_new_gps_coord(self.gps_coord)

    def start(self):
        '''
        Start service level updater, gps updater and dbus loop.
        '''
        print "Running client QoS-Manager (errors-included)"
        self.running = True
        threading.Thread(target=self.service_level_updater).start()
        threading.Thread(target=self.gps_updater).start()
        self.dbusloop()
        
    def gps_updater(self):
        '''
        Update the gps coordinate on specified udate interval.
        '''
        # main loop
        while self.running:
            time.sleep(self.gps_update_interval)
            print "gps_updater"
            try:
                self.update_gps_coord()
                print "GPS-coordinate:", self.gps_coord
            except:
                # Not in N810, got no GPS-device; do nothing...
                print "gps failure"
    
    def service_level_updater(self):
        '''
        Update service level, depending on battery level and signal strength.
        '''
        battery = self.battery_level
        signal = self.signal_strength
        self.connection.connect("connection-event", self.connection_cb, 0xFFAA)

        self.connection.connect("statistics", self.statistics_cb, 0x55AA)

        self.connection.request_connection(conic.CONNECT_FLAG_NONE)
        
        # main loop
        while self.running:
            time.sleep(self.service_level_update_interval)
            print "service_level_updater"
            # get battery level
            try:
                battery = self.check_battery_level()
                print "battery level:", self.battery_level, battery
            except:
                # Not in N810, modules doesn't work; do nothing...
                print "battery level: failure"

            # get signal strength
#            try:
            signal = self.check_signal_strength()
            print "signal strength:", self.signal_strength, signal
#            except:
                # Not in N810, modules doesn't work; do nothing...
#                print "signal strength: failure"

            # temporary store the current service level
            current_level = self.service_level

            # calculate and set the service level
            if battery == "low" and signal == "offline":
                self.service_level = "mega-low"
                self.gps_update_interval = 60
            if battery == "low" and (signal == "low" or signal == "high"):
                self.service_level = "energysaving"
                self.gps_update_interval = 30
            if (battery == "high" or battery == "charging") and signal == "offline":
                self.service_level = "ad-hoc"
                self.gps_update_interval = 30
            if (battery == "high" or battery == "charging") and signal == "low":
                self.service_level = "send few"
                self.gps_update_interval = 30
            if (battery == "high" or battery == "charging") and signal == "high":
                self.service_level = "max"
                self.gps_update_interval = 30

            # signal if service level changed!
            if self.service_level != current_level:
                self.signal_changed_service_level(self.service_level)
                
            print "service level:", self.service_level

    def close(self):
        print "Shutting down QoS-Manager"
        self.running = False
        try:
            # Stop the GPS
            gpsbt.stop(self.gps_context)
        except:
            # No GPS-device loaded/started
            pass

    def dbusloop(self):
        self.mainloop = gobject.MainLoop()
        gobject.threads_init()
        while self.mainloop.is_running():
            try:
                self.mainloop.run()
            except KeyboardInterrupt:
                self.close()

    @dbus.service.method(dbus_interface='included.errors.QoSManager', in_signature='', out_signature='s')
    def dbus_close(self):
        self.close()

    @dbus.service.signal(dbus_interface='included.errors.QoSManager', signature='v')
    def signal_new_gps_coord(self, coord):
        print "coordinates updated"

    @dbus.service.signal(dbus_interface='included.errors.QoSManager', signature='s')
    def signal_changed_service_level(self, level):
        print "service level changed"

    @dbus.service.method(dbus_interface='included.errors.QoSManager', in_signature='', out_signature='v')
    def get_service_level(self):
        return self.service_level

if __name__ == '__main__':
    qos = QoSManager()
    qos.start()
