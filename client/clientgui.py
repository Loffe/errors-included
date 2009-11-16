#!/usr/bin/env python
# coding: utf-8
import gtk
import hildon
import gobject
import pango

import datetime

from shared.data import *
import shared.queueinterface
from shared.util import getLogger
log = getLogger("client.log")
log.debug("clientgui imported log")
from map.mapdata import *

from gui.gui import Screen
from gui.mapscreen import MapScreen
from gui.alarmscreen import AlarmScreen
from gui.inboxscreen import InboxScreen
from gui.obstaclescreen import ObstacleScreen
from gui.missionscreen import MissionScreen
from gui.newmessagescreen import NewMessageScreen
from gui.outboxscreen import OutboxScreen
from gui.alarminboxscreen import AlarmInboxScreen

log.debug("imports ready")

class ClientGui(hildon.Program):
    queue = shared.queueinterface.interface
    db = None
    '''
    The main GUI-process of the client
    '''
    
    ''' create GUI Structure
    '''
    def __init__(self):
        '''
        Constructor. Creates the GUI (window and containing components).
        '''
        log.debug("ClientGui started")
        hildon.Program.__init__(self)
        self.window = hildon.Window()
        self.window.set_title("ClientGui")
        self.add_window(self.window)
        
        # Creates a empty list that contains provius screens
        self.prev_page = []
        # create the database
        self.db = shared.data.create_database()

        # A dict containing all the containers (used for hiding/showing) 
        self.screens = {}

        # A dict containing all the buttons to show/hide
        self.menu_buttons = {}

        # Panels
        panels = gtk.HBox(False, 0)
        self.window.add(panels)

        # Left menu
        vbox = gtk.VBox(False,0)
        panels.pack_start(vbox, False, False, 0)
        vbox.set_size_request(150,350)

        # Buttons (menu)
        mission_button = gtk.ToggleButton("Uppdrag")
        mission_button.connect("clicked", self.show_mission)
        self.menu_buttons["mission"] = mission_button

        add_object_button = gtk.ToggleButton("Skapa")
        add_object_button.connect("clicked", self.show_add_object)
        self.menu_buttons["add_object"] = add_object_button

        contacts_button = gtk.ToggleButton("Kontakter")
        contacts_button.connect("clicked", self.show_contacts)
        self.menu_buttons["contacts"] = contacts_button

        messages_button = gtk.ToggleButton("Meddelande")
        messages_button.connect("clicked", self.show_messages)
        self.menu_buttons["messages"] = messages_button

        vbox.add(mission_button)
        vbox.add(add_object_button)
        vbox.add(contacts_button)
        vbox.add(messages_button)

        # Right panel
        vbox_right = gtk.VBox(False, 0)
        panels.pack_start(vbox_right, True, True, 0)
        
        # adding the notification bar
        notifications = gtk.Label("Team Med Fel")
        notifications.set_alignment(0,0)
        notifications.modify_font(pango.FontDescription("sans 14"))
        notifications.set_size_request(0, 25)
        vbox_right.pack_start(notifications, False, False, 0)
        self.screens["notifications"] = notifications

        # add the map screen
        self.map = MapScreen(self.db)
        vbox_right.pack_start(self.map, True, True, 0)
        self.screens["map"] = self.map

        # add the alarm screen
        self.alarm_screen = AlarmScreen(self.db)
        self.alarm_screen.connect("okbutton-clicked2", self.back_button_function) 
        vbox_right.pack_start(self.alarm_screen, True, True, 0)
        self.screens["alarm"] = self.alarm_screen

        # adding messages screen
        self.message_screen = InboxScreen()
        vbox_right.pack_start(self.message_screen, True, True, 0)
        self.screens["message"] = self.message_screen
        
        self.new_message_screen = NewMessageScreen()
        vbox_right.pack_start(self.new_message_screen, True, True, 0)
        self.screens["new_message"] = self.new_message_screen
        
        self.outbox_screen = OutboxScreen()
        vbox_right.pack_start(self.outbox_screen, True, True, 0)
        self.screens["output"] = self.outbox_screen
        
        self.alarm_inbox_screen = AlarmInboxScreen()               
        vbox_right.pack_start(self.alarm_inbox_screen, True, True, 0)
        self.screens["alarms"] = self.alarm_inbox_screen

        # add the obstacle screen
        self.obstacle_screen = ObstacleScreen(self.db)
        self.obstacle_screen.connect("okbutton-clicked", self.back_button_function)
        vbox_right.pack_start(self.obstacle_screen, True, True, 0)
        self.screens["obstacle"] = self.obstacle_screen
        
        # add the create_mission screen
        self.mission_screen = MissionScreen(self.db)
        vbox_right.pack_start(self.mission_screen, True, True, 0)
        self.screens["make_mission"] = self.mission_screen
        
        # Mission buttons and their menu
        self.mission_menu = gtk.HBox(False, 0)
        self.mission_menu.set_size_request(0, 60)
        vbox_right.pack_start(self.mission_menu, False, False, 0)
        self.screens["mission_menu"] = self.mission_menu

        info_button = gtk.Button("Info")
        info_button.connect("clicked", self.show_mission_info)
        status_button = gtk.Button("Status")
        status_button.connect("clicked", self.show_status)
        journal_button = gtk.Button("Patient\nJournal")
        faq_button = gtk.Button("FAQ")
        faq_button.connect("clicked", self.show_faq)
        self.mission_menu.add(info_button)
        self.mission_menu.add(status_button)
        self.mission_menu.add(journal_button)
        self.mission_menu.add(faq_button)
        
        #Message buttons and their menu
        self.message_menu = gtk.HBox(False, 0)
        self.message_menu.set_size_request(0, 60)
        vbox_right.pack_start(self.message_menu, False, False, 0)
        self.screens["message_menu"] = self.message_menu
        
        new_mess = gtk.Button("Nytt")
        new_mess.connect("clicked", self.create_new_message)
        inbox = gtk.Button("Inkorg")
        inbox.connect("clicked", self.show_inbox)
        outbox = gtk.Button("Utkorg")
        outbox.connect("clicked", self.show_outbox)
        in_alarms = gtk.Button("Inkomna larm")
        in_alarms.connect("clicked", self.show_alarms)
        self.message_menu.add(new_mess)
        self.message_menu.add(inbox)
        self.message_menu.add(outbox)
        self.message_menu.add(in_alarms)

        # Add object buttons and their menu
        self.add_object_menu = gtk.HBox(False, 0)
        self.add_object_menu.set_size_request(0, 60)
        vbox_right.pack_start(self.add_object_menu, False, False, 0)
        self.screens["add_object_menu"] = self.add_object_menu
        
        create_alarm_button = gtk.Button("Larm")
        create_alarm_button.connect("clicked", self.create_alarm)
        create_obstacle_button = gtk.Button("Hinder")
        create_obstacle_button.connect("clicked", self.create_obstacle)
        create_mission_button = gtk.Button("Uppdrag")
        create_mission_button.connect("clicked", self.create_mission)
        self.add_object_menu.add(create_alarm_button)
        self.add_object_menu.add(create_obstacle_button)
        self.add_object_menu.add(create_mission_button)
        
        # add back- and ok-button (used in alarmscreen, obstaclescreen etc)
        self.buttons_box = gtk.HBox(False, 10)
        self.buttons_box.set_size_request(0, 60)
        self.screens["buttons"] = self.buttons_box
        
        back_button = gtk.Button("Bakåt")
        self.buttons_box.pack_start(back_button)
        back_button.connect("clicked", self.back_button_function)

        ok_button = gtk.Button("OK")
        ok_button.connect("clicked", self.ok_button_function)
        ok_button.set_flags(gtk.CAN_DEFAULT)
        self.buttons_box.pack_start(ok_button)
        
        vbox_right.pack_start(self.buttons_box, False, False, 0)

        self.window.connect("destroy", gtk.main_quit)
        self.window.connect("key-press-event", self.on_key_press)
        self.window.connect("window-state-event", self.on_window_state_change)

        # Change to default True?
        self.window_in_fullscreen = False
        log.info("ClientGui created")
        
    def run(self):
        '''
        Main GUI loop
        '''
        self.window.show_all()
        self.show_default()
        gtk.main()
    
    ''' Handle events
    ''' 
    def back_button_function(self, event):
        print "back"
        self.show(self.prev_page[-2])
    
    def ok_button_function(self, event):
        for screen in self.screens.values():
            if screen.props.visible and isinstance(screen, Screen):
                screen.ok_button_function(event)
    
    # mission view event handlers
    def show_mission(self, event):
        self.toggle_show("mission", ["notifications", "map", "mission_menu"], 
                         "Här visas dina uppdrag")
    
    # mission buttons event handlers
    def show_mission_info(self, event):
        pass
    
    def show_status(self, event):
        
        dialog = gtk.Dialog("Samtal",
                 self.window,  #the toplevel wgt of your app
                 gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  #binary flags or'ed together
                 ("     Svara     ", 77, "  Upptaget  ", 666))
        who = gtk.Label("DT ringer...")
        who.show()
        dialog.set_size_request(400,200)
        #dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

        dialog.vbox.pack_start(who)
        question = gtk.Label("Vill du svara?")
        question.show()
        dialog.vbox.pack_start(question)
        dialog.show()
        result = dialog.run()
        if result == 77:
           print "svara"

           dia = gtk.Dialog("Samtal",
                 self.window,  #the toplevel wgt of your app
                 gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  #binary flags or'ed together
                 ("       Lägg på       ", 11))
        
           dia.set_size_request(400,200)

           qu = gtk.Label("Vill du lägga på?")
           qu.show()
           dia.vbox.pack_start(qu)
           dia.show()
           result = dia.run()
           
           dia.destroy()
           
        elif result == 666:
            print "upptaget"
        dialog.destroy()
    
    def show_journals(self, event):
        pass
    
    def show_faq(self, event):
        print "faq the system!"
        poi_data = shared.data.POIData(15.5769069,58.4088884, u"goal", datetime.now(), shared.data.POIType.accident)
#        unit_data = shared.data.UnitData(15.5749069, 58.4068884, u"enhet 1337", datetime.now(), shared.data.UnitType.commander)
#        mission_data = shared.data.MissionData(u"accidänt", poi_data, 7, u"Me Messen", u"det gör jävligt ont i benet på den dära killen dårå", [unit_data])
        self.db.add(poi_data)
        
        enhet3 = UnitData(15.5746475, 58.4077164 ,u"Enhet3",datetime.now(), UnitType.ambulance)
        self.db.add(enhet3)
        
    # add object view event handlers
    def show_add_object(self, event):
        self.toggle_show("add_object", 
                         ["notifications", "map","add_object_menu"], 
                         "Välj en koordinat och sedan typ av objekt")
    
    # add object buttons event handlers
    def create_alarm(self, event):
        self.show(["alarm", "buttons"])
    
    def create_obstacle(self, event):
        self.show(["obstacle", "buttons"])
    
    def create_mission(self, event):
        self.show(["make_mission", "buttons"])

    def create_new_message(self, event):
        self.show(["new_message", "buttons"])
        
    def show_outbox(self, event):
        self.show(["output", "message_menu"])
        
    def show_inbox(self, event):
        self.show(["message", "message_menu"])
        
    def show_alarms(self, event):
        self.show(["alarms", "message_menu"])
        
    # contacts view event handlers
    def show_contacts(self,event):
        self.toggle_show("contacts", ["notifications"], "Här visas dina kontakter och du kan ringa till dem")

    # messages view event handlers
    def show_messages(self, event):
        self.toggle_show("messages", ["notifications", "message","message_menu"], "Här visas dina meddelanden")

    # show certain screen methods
    def toggle_show(self, button_key, screen_keys, notification_text = ""):
        '''
        Toggle clicked button, show specified screens and set notification.
        @param button_key: the key of the clicked button.
        @param screen_keys: the screens to show.
        @param notification_text: the notification text to set.
        '''
        if self.menu_buttons[button_key].get_active():
            for menu_button in self.menu_buttons.keys():
                if menu_button != button_key:
                    self.menu_buttons[menu_button].set_active(False)
            self.show(screen_keys)
            self.screens["notifications"].set_label(notification_text)
        else:
            self.show_default()
    
    def show(self, keys):
        '''
        Show specified screens.
        @param keys: a list with keys to the screens to show. 
        '''
        self.prev_page.append(keys)

        for key in self.screens.keys():
            self.screens[key].hide_all()
        for key in keys:
            self.screens[key].show_all()
            
    def show_default(self):
        '''
        Show only default screens (GUI-background).
        '''
        for key in self.screens.keys():
            self.screens[key].hide_all()
        self.screens["notifications"].set_label("Team Med Fel")
        self.screens["notifications"].show()
        self.screens["map"].show()

    # handle key press events
    def on_key_press(self, widget, event, *args):
        # react on fullscreen button press
        if event.keyval == gtk.keysyms.F6:
            if self.window_in_fullscreen:
                self.window.unfullscreen()
            else:
                self.window.fullscreen()
        # Zoom out (-)
        if event.keyval == gtk.keysyms.F8:
            self.map.zoom("-")
        # Zoom in (+)
        elif event.keyval == gtk.keysyms.F7:
            self.map.zoom("+")  

    def on_window_state_change(self, widget, event, *args):
        if event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN:
            self.window_in_fullscreen = True
        else:
            self.window_in_fullscreen = False  

