import dbus

bus = dbus.SessionBus()
remote_object = bus.get_object("com.example.Queue", "/Queue")
interface = dbus.Interface(remote_object, "com.example.Queue")

