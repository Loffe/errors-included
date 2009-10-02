#!/usr/bin/env python
#-*- coding: utf-8 -*-
import gpsbt
import time

def gps_pos():
    #Startar GPS:en
    context = gpsbt.start()
    time.sleep(2)
    #Väntar för att se att GPSen startats och kan ta emot kommandon

    gpsdevice = gpsbt.gps()
    #Skriver ut Longitud och Latitud
    x,y = (0,0)
    while (x,y) == (0,0):
        x, y = gpsdevice.get_position()
        time.sleep(1)
    print "Longitud: ",x
    print "Latitud: ",y
    # Stänger av GPS:en
    gpsbt.stop(context)
    

gps_pos()
