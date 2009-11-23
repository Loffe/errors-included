#!/usr/bin/env python
# coding: utf-8
import gtk
import dbus.mainloop.glib
import gobject
import pango
import threading
import datetime
import messagedispatcher
from shared.data import *
import shared.queueinterface
from shared.util import getLogger
log = getLogger("client.log")
log.debug("clientgui imported log")
from map.mapdata import *
import controller
from database import ClientDatabase
from gui.gui import Screen
from gui.mapscreen import MapScreen
from gui.alarmscreen import AlarmScreen
from gui.inboxscreen import InboxScreen
from gui.obstaclescreen import ObstacleScreen
from gui.missionscreen import MissionScreen
from gui.newmessagescreen import NewMessageScreen
from gui.outboxscreen import OutboxScreen
from gui.alarminboxscreen import AlarmInboxScreen
from gui.faqscreen import FAQScreen
from gui.infoscreen import InfoScreen
from gui.statusscreen import StatusScreen
from gui.patientjournalscreen import PatientJournalScreen
from gui.contactscreen import ContactScreen
from gui.camerascreen import CamScreen


try:
    import hildon
    Program = hildon.Program
except:
    hildon = gtk
    class Program(object):
        def add_window(self, window):
            pass
    hildon.Program = Program

log.debug("imports ready")

class ClientGui(hildon.Program):
    queue = None
    db = None

    def __init__(self):
        '''
        Constructor. Creates the GUI (window and containing components).
        '''
        log.debug("ClientGui started")

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        self.queue = shared.queueinterface.get_interface(bus)
        self.message_dispatcher = messagedispatcher.MessageDispatcher(bus)
        self.mainloop = gobject.MainLoop()

        hildon.Program.__init__(self)
        self.window = hildon.Window()
        self.window.set_title("ClientGui")
        self.window.set_size_request(800,480)
        self.add_window(self.window)
        
        # Creates a empty list that contains previous screens
        self.prev_page = []

        # create the database
        db = ClientDatabase(self.queue)
        self.db = shared.data.create_database(db)

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
        self.alarm_screen.connect("okbutton-alarm-clicked", self.back_button_function) 
        vbox_right.pack_start(self.alarm_screen, True, True, 0)
        self.screens["alarm"] = self.alarm_screen

        # adding messages screen
        self.message_screen = InboxScreen(self.db)
        vbox_right.pack_start(self.message_screen, True, True, 0)
        self.screens["message"] = self.message_screen
        
        self.new_message_screen = NewMessageScreen(self.db)
        vbox_right.pack_start(self.new_message_screen, True, True, 0)
        self.screens["new_message"] = self.new_message_screen
        
        self.outbox_screen = OutboxScreen(self.db)
        vbox_right.pack_start(self.outbox_screen, True, True, 0)
        self.screens["output"] = self.outbox_screen
        
        self.alarm_inbox_screen = AlarmInboxScreen(self.db)               
        vbox_right.pack_start(self.alarm_inbox_screen, True, True, 0)
        self.screens["alarms"] = self.alarm_inbox_screen

        # add the obstacle screen
        self.obstacle_screen = ObstacleScreen(self.db)
        self.obstacle_screen.connect("okbutton-obstacle-clicked", self.back_button_function)
        vbox_right.pack_start(self.obstacle_screen, True, True, 0)
        self.screens["obstacle"] = self.obstacle_screen
        
        # add the create_mission screen
        self.mission_screen = MissionScreen(self.db)
        self.mission_screen.connect("okbutton-mission-clicked", self.back_button_function) 
        vbox_right.pack_start(self.mission_screen, True, True, 0)
        self.screens["make_mission"] = self.mission_screen
        

        self.faq_screen = FAQScreen(self.db)               
        vbox_right.pack_start(self.faq_screen, True, True, 0)
        self.screens["faq"] = self.faq_screen
        
        self.info_screen = InfoScreen(self.db)               
        vbox_right.pack_start(self.info_screen, True, True, 0)
        self.screens["info"] = self.info_screen
        
        self.status_screen = StatusScreen(self.db)               
        vbox_right.pack_start(self.status_screen, True, True, 0)
        self.screens["status"] = self.status_screen

        self.patient_journal_screen = PatientJournalScreen(self.db)               
        vbox_right.pack_start(self.patient_journal_screen, True, True, 0)
        self.screens["patient_journal"] = self.patient_journal_screen        

        # add the contact_screen and their menu
        self.contact_screen = ContactScreen(self.db)
        vbox_right.pack_start(self.contact_screen, True, True, 0)
        self.screens["contact"] = self.contact_screen
        
        # Videocamera
        self.cam_screen = CamScreen(self.db)
        vbox_right.pack_start(self.cam_screen, True, True, 0)
        self.screens["camera"] = self.cam_screen
        
        #Contact menu
        self.contact_menu = gtk.HBox(False, 0)
        self.contact_menu.set_size_request(0, 60)
        vbox_right.pack_start(self.contact_menu, False, False, 0)
        self.screens["contact_menu"] = self.contact_menu
        call = gtk.Button("Bröstsamtal")
        call.connect("clicked", self.show_voice)
        video = gtk.Button("Videosamtal")
        video.connect("clicked", self.show_cam)
        self.contact_menu.add(call)
        self.contact_menu.add(video)


        
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
        journal_button.connect("clicked", self.show_journals)
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
        
        self.back_button_box = gtk.HBox(False, 10)
        self.back_button_box.set_size_request(0, 60)
        self.screens["back_button_box"] = self.back_button_box
        
        back_button2 = gtk.Button("Bakåt")
        self.back_button_box.pack_start(back_button2)
        back_button2.connect("clicked", self.back_button_function)
        
        vbox_right.pack_start(self.back_button_box, False, False, 0)

        self.window.connect("destroy", lambda event: self.mainloop.quit())
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
        gobject.threads_init()
        # start gtk main (gui) thread
        self.start_controller()
        while self.mainloop.is_running():
            try:
                self.mainloop.run()
            except KeyboardInterrupt:
                self.mainloop.quit()

    def start_controller(self):
        '''
        Create and start ClientController
        '''
        name = "Ragnar Dahlberg"
        unit_type = shared.data.UnitType.commander
        status = "Available"
        self.controller = controller.ClientController(name,unit_type,status, self.db)

    ''' Handle events
    ''' 
    def back_button_function(self, event):
        self.show(self.prev_page[-2])
    
    def ok_button_function(self, event):
        for screen in self.screens.values():
            if screen.props.visible and isinstance(screen, Screen):
                screen.ok_button_function(event)
    
    def set_mission(self, data):
        '''
        Append a mission to own missions.
        @param data: the mission to append.
        '''
        self.controller.missions.append(data)
        print "got new mission:", type(data), data
    
    # mission view event handlers
    def show_mission(self, event):
        self.toggle_show("mission", ["notifications", "map", "mission_menu"], 
                         "Här visas dina uppdrag")
    
    # mission buttons event handlers
    def show_mission_info(self, event):
        self.show(["info", "buttons"])
    
    def show_status(self, event):
        self.show(["status", "buttons"])
  
#        dialog = gtk.Dialog("Samtal",
#                 self.window,  #the toplevel wgt of your app
#                 gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  #binary flags or'ed together
#                 ("     Svara     ", 77, "  Upptaget  ", 666))
#        who = gtk.Label("DT ringer...")
#        who.show()
#        dialog.set_size_request(400,200)
#        #dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
#
#        dialog.vbox.pack_start(who)
#        question = gtk.Label("Vill du svara?")
#        question.show()
#        dialog.vbox.pack_start(question)
#        dialog.show()
#        result = dialog.run()
#        if result == 77:
#           print "svara"
#
#           dia = gtk.Dialog("Samtal",
#                 self.window,  #the toplevel wgt of your app
#                 gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  #binary flags or'ed together
#                 ("       Lägg på       ", 11))
#        
#           dia.set_size_request(400,200)
#
#           qu = gtk.Label("Vill du lägga på?")
#           qu.show()
#           dia.vbox.pack_start(qu)
#           dia.show()
#           result = dia.run()
#           
#           dia.destroy()
#           
#        elif result == 666:
#            print "upptaget"
#        dialog.destroy()
    
    def show_journals(self, event):
        self.show(["patient_journal", "buttons"])
    
    def show_faq(self, event):
        self.show(["faq", "back_button_box"])
        
    # add object view event handlers
    def show_add_object(self, event):
        self.toggle_show("add_object", 
                         ["notifications", "map","add_object_menu"], 
                         "Välj en koordinat och sedan typ av objekt")
    
    # add object buttons event handlers
    def create_alarm(self, event):
        self.show(["alarm", "buttons"])
        self.screens["alarm"].location_entry2.set_text(str(self.screens["map"].gps_x))
        self.screens["alarm"].location_entry3.set_text(str(self.screens["map"].gps_y))
            
    def create_obstacle(self, event):
        self.show(["obstacle", "buttons"])
        self.screens["obstacle"].location_entry2.set_text(str(self.screens["map"].gps_x))
        self.screens["obstacle"].location_entry3.set_text(str(self.screens["map"].gps_y))
    
    def create_mission(self, event):
        self.show(["make_mission", "buttons"])
        self.screens["make_mission"].location_entry2.set_text(str(self.screens["map"].gps_x))
        self.screens["make_mission"].location_entry3.set_text(str(self.screens["map"].gps_y))
        
#        self.screens["make_mission"].combo_box.clear()
        combo = self.screens["make_mission"].combo_box
        for alarm in self.db.get_all_alarms():
            combo.remove_text(alarm.id)
            combo.insert_text(alarm.id, alarm.event)

    def create_new_message(self, event):
        self.show(["new_message", "buttons"])
        
    def show_cam(self, event):
#        self.screens["camera"].start_video_send(self.screens["contact"].ip)
        self.screens["camera"].start_vvoip(self.screens["contact"].ip2)
        self.show(["camera"])
        
    def show_voice(self, event):
#        self.screens["camera"].start_video_send(self.screens["contact"].ip)
        self.screens["camera"].start_voip(self.screens["contact"].ip2)
        self.show(["camera"])
        
    def show_outbox(self, event):
        self.show(["output", "message_menu"])
        
    def show_inbox(self, event):
        self.show(["message", "message_menu"])
        
    def show_alarms(self, event):
        self.show(["alarms", "message_menu"])
        
    # contacts view event handlers
    def show_contacts(self,event):
        self.toggle_show("contacts", ["notifications","contact", "contact_menu"], "Här visas dina kontakter och du kan ringa till dem")

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
        if "add_object" in button_key and self.menu_buttons[button_key].get_active() == True:
            self.screens["map"].sign = True
            self.screens["map"].draw_sign()
        else:
            self.screens["map"].sign = False
            self.screens["map"].remove_sign()
    
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
        self.screens["map"].sign = False
        self.screens["map"].remove_sign()

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

