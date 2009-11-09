# -*- coding: utf-8 -*-
from __future__ import division
import dbus

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
        
        # under those levels we have lower service level
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
        percentage_left = battery_left*100/battery_lifetime
        
        # return battery level
        if charging:
            return ("charging",1)
        elif percentage_left < self.critical_battery_level:
            return ("critical", -1)
        else:
            return ("normal", 0)

    def check_signal_strength(self):
        '''
        Update the signal strength.
        '''
        return ("normal", 0)
    
    def get_gps_coord(self):
        '''
        Update the gps coordinate (own position).
        '''

    def mainloop(self):
        while True:
            battery = check_battery_level()
            signal = check_signal_strength()

    '''
    dbus Signals
    '''
    def signal_new_gps_coord(self):
        pass
    
    def signal_changed_service_level(self):
        pass
