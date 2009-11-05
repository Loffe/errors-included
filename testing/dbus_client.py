import sys
from traceback import print_exc

import dbus

def main():
    bus = dbus.SessionBus()

    try:
        remote_object = bus.get_object("com.example.Queue",
                                       "/Queue")

        # you can either specify the dbus_interface in each call...
        hello_reply_list = remote_object.enqueue("Hello from example-client.py!",
            dbus_interface = "com.example.Queue")
    except dbus.DBusException:
        print_exc()
        sys.exit(1)

    print (hello_reply_list)

    # ... or create an Interface wrapper for the remote object
    iface = dbus.Interface(remote_object, "com.example.Queue")
    print iface.enqueue("Hello")
    return

    hello_reply_tuple = iface.GetTuple()

    print hello_reply_tuple

    hello_reply_dict = iface.GetDict()

    print hello_reply_dict

    # D-Bus exceptions are mapped to Python exceptions
    try:
        iface.RaiseException()
    except dbus.DBusException, e:
        print str(e)

    # introspection is automatically supported
    print remote_object.Introspect(dbus_interface="org.freedesktop.DBus.Introspectable")

    if sys.argv[1:] == ['--exit-service']:
        iface.Exit()

if __name__ == '__main__':
    main()
