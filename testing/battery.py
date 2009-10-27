from __future__ import division
import dbus
 
bus = dbus.SystemBus()
hal_obj = bus.get_object ('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
hal = dbus.Interface (hal_obj, 'org.freedesktop.Hal.Manager')
uids = hal.FindDeviceByCapability('battery')
dev_obj = bus.get_object ('org.freedesktop.Hal', uids[0])
 
battery_left = dev_obj.GetProperty('battery.reporting.current')
battery_lifetime =dev_obj.GetProperty('battery.reporting.design')
laddar = dev_obj.GetProperty('battery.rechargeable.is_charging')
print "Laddar?!?!: ", laddar
print "Battery left (mAh): ", battery_left
print "Battery lifetime (mAh): ", battery_lifetime
percentage_left = battery_left*100/battery_lifetime
print "Battery left (%): ", percentage_left


dev_obj = bus.get_object ('org.freedesktop.Hal', hal.FindDeviceByCapability ('laptop_panel'))

# get an interface to the device
dev = dbus.Interface (dev_obj, 'org.freedesktop.Hal.Device')
print dev.GetProperty ('info.product')
print "Brightness levels:", dev.GetProperty ('laptop_panel.num_levels')

# get a difference interface to the device
dev = dbus.Interface (dev_obj, 'org.freedesktop.Hal.Device.LaptopPanel')

print "Current brightness:", dev.GetBrightness ()
dev.SetBrightness (int (sys.argv[1]))
print "New brightness:", dev.GetBrightness ()


#print 'charge level percentage',\
#      dev_obj.GetProperty('battery.charge_level.percentage')
#print 'charge current', dev_obj.GetProperty('battery.reporting.current')
#print 'charge design', dev_obj.GetProperty('battery.reporting.design')
#print 'charge last full',\
#      dev_obj.GetProperty('battery.reporting.last_full')
#print 'charge unit', dev_obj.GetProperty('battery.reporting.unit')
#print 'voltage current', dev_obj.GetProperty('battery.voltage.current')
#print 'voltage design', dev_obj.GetProperty('battery.voltage.design')
#print 'voltage unit', dev_obj.GetProperty('battery.voltage.unit')
    
