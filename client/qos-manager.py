# -*- coding: utf-8 -*-
from __future__ import division
import dbus
import gpsbt
import time

class QoSManager(object):
    '''
    This class manages and updates the service level depending on battery level
    and signal strength.
    '''
    def __init__(self):
        '''
        Constructor.
        '''
        # the service level
        self.service_level = 0

        # the variables updated by this class
        self.gps_coord = (0,0)
        self.signal_strength = 0
        self.battery_level = 0
        
        # gps update interval (every X seconds)
        self.gps_update_interval = 60
        
        # lower service level if under those levels
        self.critical_battery_level = 20
        self.critical_signal_strength = 0
        
        # da buzz
        self.bus = dbus.SystemBus()

    def check_battery_level(self):
        '''
        Update the battery level.
        '''
        hal_obj = bus.get_object('org.freedesktop.Hal',
                                 '/org/freedesktop/Hal/Manager')
        hal = dbus.Interface(hal_obj, 'org.freedesktop.Hal.Manager')
        uids = hal.FindDeviceByCapability('battery')
        dev_obj = bus.get_object('org.freedesktop.Hal', uids[0])
        
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

    # UNSTABLE! DOESN'T DO SHIT!
    def check_signal_strength(self):
        '''
        Update the signal strength.
        '''
        # dbus getters?
        signal_strength = None

        self.signal_strength = signal_strength

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
        context = gpsbt.start()
        
        # wait for the gps to start (Needed?)
        time.sleep(2)

        # create the device
        gpsdevice = gpsbt.gps()
        
        # get the gps coordinates
        x,y = (0,0)
        while (x,y) == (0,0):
            x, y = gpsdevice.get_position()
            time.sleep(1)

        # Stop the GPS
        gpsbt.stop(context)
        
        # set gps coordinates
        self.gps_coord = (x,y)


    def mainloop(self):
        while True:
            # get levels
            battery = check_battery_level()
            signal = check_signal_strength()
            
            # temporary store the current service level
            current_level = self.service_level

            # calculate and set the service level            
            if battery == "low" and signal == "offline":
                self.service_level = "mega-low"
            if battery == "low" and (signal == "low" or signal == "high"):
                self.service_level = "energysaving"
            if (battery == "high" or battery == "charging") and signal == "offline":
                self.service_level = "ad-hoc"
            if (battery == "high" or battery == "charging") and signal == "low":
                self.service_level = "send few"
            if (battery == "high" or battery == "charging") and signal == "high":
                self.service_level = "max"
                
            # signal if service level changed!
            if self.service_level != current_level:
                self.signal_changed_service_level()

    '''
    dbus Signals
    '''
    def signal_new_gps_coord(self):
        pass
    
    def signal_changed_service_level(self):
        '''
        Signal to dbus; service level changed
        '''
        # dbus signal!
        pass
