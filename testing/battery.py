import dbus
 
bus = dbus.SystemBus()
hal_obj = bus.get_object ('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
hal = dbus.Interface (hal_obj, 'org.freedesktop.Hal.Manager')
uids = hal.FindDeviceByCapability('battery')
dev_obj = bus.get_object ('org.freedesktop.Hal', uids[0])
 
#print 'charge level percentage',\
#    dev_obj.GetProperty('battery.charge_level.percentage')
print 'charge current', dev_obj.GetProperty('battery.reporting.current')
print 'charge design', dev_obj.GetProperty('battery.reporting.design')
battery_left = dev_obj.GetProperty('battery.reporting.current')
battery_lifetime =dev_obj.GetProperty('battery.reporting.design')
print "Battery left: ", battery_left
print "Battery lifetime: ", battery_lifetime
percentage_left = battery_left/battery_lifetime
print "Battery left (%): ", percentage_left
#print 'charge last full',\
#    dev_obj.GetProperty('battery.reporting.last_full')
#print 'charge unit', dev_obj.GetProperty('battery.reporting.unit')
#print 'voltage current', dev_obj.GetProperty('battery.voltage.current')
#print 'voltage design', dev_obj.GetProperty('battery.voltage.design')
#print 'voltage unit', dev_obj.GetProperty('battery.voltage.unit')
    
