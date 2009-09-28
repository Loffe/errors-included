#!/usr/bin/env python
import gpsbt
import time

def main():
    print 'Connecting...' 
    context = gpsbt.start()
    
    if context == None:
        print 'Problem while connecting!'
        return

    # ensure that GPS device is ready to connect and to receive commands
    time.sleep(2)
    gpsdevice = gpsbt.gps()

    # read 4 times and show information
    for a in range(4):
        gpsdevice.get_fix()
        # print information stored under 'fix' variable
        print 'Altitude: %.3f'%gpsdevice.fix.altitude
        # dump all information available
        print gpsdevice
        time.sleep(2)

    # ends Bluetooth connection
    gpsbt.stop(context)

main()
