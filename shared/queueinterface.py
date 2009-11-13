# -*- coding: utf-8 -*-
import dbus

bus = dbus.SessionBus()
remote_object = bus.get_object("com.example.Queue", "/Queue")
interface = dbus.Interface(remote_object, "com.example.Queue")

if __name__ == '__main__':
    import data
    from datetime import datetime
    login_msg = data.Message("ragnar dahlberg", "server", type=data.MessageType.login,
                             unpacked_data={"class": "dict", "password": "prydlig frisyr"})
    interface.enqueue(login_msg.packed_data, 5)

    poi_data = data.POIData(12,113, u"goal", datetime.now(), data.POIType.accident)
    alarm = data.Alarm(u"Bilolycka", u"Linköping", poi_data,
                       u"Laban Andersson", u"070-741337", 7)
    msg = data.Message("ragnar dahlberg", "server", type=data.MessageType.alarm, unpacked_data=alarm)
    data = msg.packed_data
    print "Sent:", data
    print interface.enqueue(data, msg.prio)
