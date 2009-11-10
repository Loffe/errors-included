# -*- coding: utf-8 -*-
from __future__ import division
import dbus
import dbus.mainloop.glib
import dbus.service
import time
import threading
import gobject

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

    def check_battery_level(self):
        '''
        Update the battery level.
        '''
        hal_obj = self.session_bus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
        hal = dbus.Interface(hal_obj, 'org.freedesktop.Hal.Manager')
        uids = hal.FindDeviceByCapability('battery')
        dev_obj = self.session_bus.get_object('org.freedesktop.Hal', uids[0])
        
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
        import gpsbt
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
        self.signal_new_gps_coord(self.gps_coord)

    def start(self):
        threading.Thread(target=self.run).start()
        self.dbusloop()
    
    def run(self):
        running = True
        battery = self.battery_level
        signal = self.signal_strength
        while running:
            # get levels
            try:
                battery = self.check_battery_level()
                signal = self.check_signal_strength()
            except:
                # Not in N810, modules doesn't work; do nothing...
                pass

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

        self.close()
                
    def close(self):
        print "Shutting down QoS-Manager"
        gobject.idle_add(mainloop.quit)
    
    def dbusloop(self):
        mainloop = gobject.MainLoop()
        gobject.threads_init()
        print "Running client QoS-Manager (errors-included)."
        while mainloop.is_running():
            try:
                mainloop.run()
            except KeyboardInterrupt:
                mainloop.quit()

    @dbus.service.signal(dbus_interface='included.errors.QosManager', signature='v')
    def signal_new_gps_coord(self, coord):
        print "coordinates updated"

    @dbus.service.signal(dbus_interface='included.errors.QosManager', signature='s')
    def signal_changed_service_level(self, level):
        '''
        Signal to dbus; service level changed
        '''
        print "level changed"

if __name__ == '__main__':
    qos = QoSManager()
    qos.start()
