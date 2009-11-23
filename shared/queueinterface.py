# -*- coding: utf-8 -*-
import dbus

def get_interface(bus):
    remote_object = bus.get_object("included.errors.Client", "/Queue")
    interface = dbus.Interface(remote_object, "included.errors.Client")
    return interface

if __name__ == '__main__':
    import data
    from datetime import datetime
    interface = get_interface(dbus.SessionBus())
    login_msg = data.Message("ragnar", "server", type=data.MessageType.login,
                             unpacked_data={"class": "dict", "password": "prydlig frisyr"})
    local_id = interface.enqueue(login_msg.packed_data, 5)
    print "sent login with id:", local_id

    '''
    poi_data = data.POIData(12,113, u"goal", datetime.now(), data.POIType.accident)
    alarm = data.Alarm(u"Bilolycka", u"Linköping", poi_data,
                       u"Laban Andersson", u"070-741337", 7)
    msg = data.Message("ragnar", "server", type=data.MessageType.alarm, unpacked_data=alarm)
    data = msg.packed_data
    print "Sent:", data
    print interface.enqueue(data, msg.prio)
    '''
