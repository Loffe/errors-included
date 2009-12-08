# -*- coding: utf-8 -*-
import gtk
import gobject
import shared.data
import gui
import datetime
import pango
from missioninfoscreen import MissionInfoScreen 

class ChangeMissionScreen(MissionInfoScreen):
    
    def __init__(self, db):
        MissionInfoScreen.__init__(self, db, False)
