#!/usr/bin/env python
#-*- coding: utf-8 -*-
import gpsbt
import time

def gps_pos():
    #Startar GPS:en
    context = gpsbt.start()
    #Väntar för att se att GPSen startats och kan ta emot kommandon
    while context == None:
        time.sleep(1) #2
    gpsdevice = gpsbt.gps()
    #Skriver ut Longitud och Latitud
    x, y = gpsdevice.get_position()
    print "Longitud: ",x
    print "Latitud: ",y
    # Stänger av GPS:en
    gpsbt.stop(context)
    
    return pos

gps_pos()
