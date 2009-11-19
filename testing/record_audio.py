#!/usr/bin/env python

# This is the MIT license:
# http://www.opensource.org/licenses/mit-license.php

# Copyright (c) 2009 Digital Achievement Incorporated and contributors.

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from optparse import OptionParser

import dbus
import gst
import sys
import time


def list_capture_devices():
    bus = dbus.SystemBus()
    hal_manager = bus.get_object("org.freedesktop.Hal", "/org/freedesktop/Hal/Manager")
    hal_manager = dbus.Interface(hal_manager, "org.freedesktop.Hal.Manager")

    devices = hal_manager.FindDeviceStringMatch("alsa.type", "capture")

    identifiers = []

    for dev in devices:
        device = bus.get_object("org.freedesktop.Hal", dev)

        card = device.GetAllProperties(dbus_interface="org.freedesktop.Hal.Device")
        if card["alsa.card"] not in identifiers:
            print "%d. %s" % (card["alsa.card"], card["alsa.card_id"])
            identifiers.append(card["alsa.card"])

    return identifiers

def get_capture_device_id():
    capture_device_id = None

    while capture_device_id == None:
        identifiers = list_capture_devices()
        print "Enter a capture device ID: ",
        line = sys.stdin.readline().strip()
        
        try:
            capture_device_id = int(line)
        
            if capture_device_id in identifiers:
                return capture_device_id
        except ValueError:
            print "value error"


        print "Invalid entry\n"
        capture_device_id = None

def get_capture_path():
    capture_path = None
    while capture_path is None:
        print "Enter a capture path (.flac file): ",
        return sys.stdin.readline().strip()
    

def record(device_id, capture_path):
    pipeline = gst.parse_launch("""alsasrc device=hw:%d ! audioconvert ! level name=recordlevel interval=10000000 ! audioconvert ! flacenc ! filesink location=%s""" % (device_id, capture_path))
    pipeline.set_state(gst.STATE_PLAYING)

    print "recording, press enter to stop"
    sys.stdin.readline()

    pipeline.set_state(gst.STATE_NULL)
    time.sleep(5)

if __name__ == "__main__":
    
    print list_capture_devices()
    
    oparser = OptionParser()
    oparser.add_option("-f", "--file", dest="path",
                       help="save to FILE", metavar="FILE")
    oparser.add_option("-d", "--device", dest="device",
                       help="Use device DEVICE", metavar="DEVICE")
    (options, args) = oparser.parse_args()


    device_id = options.device
    capture_path = options.path

    if device_id is None:
        device_id = get_capture_device_id()

    if capture_path is None:
        capture_path = get_capture_path()

    record(device_id, capture_path)
    
    
