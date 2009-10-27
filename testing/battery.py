from __future__ import division
import dbus
 
bus = dbus.SystemBus()
hal_obj = bus.get_object ('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
hal = dbus.Interface (hal_obj, 'org.freedesktop.Hal.Manager')
uids = hal.FindDeviceByCapability('battery')
dev_obj = bus.get_object ('org.freedesktop.Hal', uids[0])
 
battery_left = dev_obj.GetProperty('battery.reporting.current')
battery_lifetime =dev_obj.GetProperty('battery.reporting.design')
print "Battery left: ", battery_left
print "Battery lifetime: ", battery_lifetime
percentage_left = battery_left*100/battery_lifetime
print "Battery left (%): ", percentage_left



    
