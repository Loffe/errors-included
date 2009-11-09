import dbus
bus = dbus.SystemBus()
eth0 = bus.get_object('org.freedesktop.NetworkManager',
                      '/org/freedesktop/NetworkManager/Devices/eth0')
eth0_dev_iface = dbus.Interface(eth0,
    dbus_interface='org.freedesktop.NetworkManager.Devices')
props = ewth0_dev_iface.getProperties()
print props
# props is the same as before
