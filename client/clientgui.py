#!/usr/bin/env python
# coding: utf-8
import config
import gtk
import dbus.mainloop.glib
import gobject
import pango
import threading
import datetime
import shared.messagedispatcher
from shared.data import *
import shared.queueinterface
from shared.util import getLogger, get_ip
log = getLogger("client.log")
log.debug("clientgui imported log")
from map.mapdata import *
import controller
import config
import shared.util
from shared.blinkbutton import BlinkToggleButton
from database import ClientDatabase
from gui.gui import Screen
from gui.mapscreen import MapScreen
from gui.alarmscreen import AlarmScreen
from gui.inboxscreen import InboxScreen
from gui.obstaclescreen import ObstacleScreen
from gui.changeobstaclescreen import ChangeObstacleScreen
from gui.missionscreen import MissionScreen
from gui.changemissionscreen import ChangeMissionScreen
from gui.unitscreen import UnitScreen
from gui.newmessagescreen import NewMessageScreen
from gui.outboxscreen import OutboxScreen
from gui.faqscreen import FAQScreen
from gui.missioninfoscreen import MissionInfoScreen
from gui.statusscreen import StatusScreen
from gui.patientjournalscreen import PatientJournalScreen
from gui.contactscreen import ContactScreen
from gui.camerascreen import CamScreen
from mapobjecthandler import MapObjectHandler
from textmessagehandler import TextMessageHandler
from journalhandler import JournalHandler
from gui.notificationscreen import NotificationScreen
from gui.selectunit import SelectUnitButton
from gui.selectunit import SelectUnitDialog
from gui.activities import Activities
from gui.patientjournalmessagescreen import PatientJournalMessageScreen


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
        self.mainloop = gobject.MainLoop()

        hildon.Program.__init__(self)
        self.window = hildon.Window()
        self.window.set_title("ClientGui")
        self.window.set_size_request(800,480)
        self.add_window(self.window)

        # create the database
        db = ClientDatabase(self.queue)
        self.db = shared.data.create_database(db)
        # create message dispatcher
        self.message_dispatcher = shared.messagedispatcher.MessageDispatcher(bus, db)
        # connect the dispatcher to database
        self.db.dispatcher = self.message_dispatcher

        self.mapobjecthandler = MapObjectHandler(self.db, self.queue)
        self.textmessagehandler = TextMessageHandler(self.db, self.queue)

        self.message_dispatcher.connect_to_type(MessageType.object, self.mapobjecthandler.handle)
        self.message_dispatcher.connect_to_type(MessageType.text, self.textmessagehandler.handle)
        
        self.journalhandler = JournalHandler(self.db, self.queue)
        self.message_dispatcher.connect_to_type(MessageType.journal, self.journalhandler.handle)

        # create gui
        self.create_gui()
    
    def build_icon(self, label, icon, box_type = "v"):
        image = gtk.Image()
        image.set_from_file(icon)

        if box_type == "v":
            vbox = gtk.VBox()
            vbox.add(image)
            vbox.add(gtk.Label(label))
            return vbox
        else:
            hbox = gtk.HBox(True, 0)
            hbox.add(image)
            hbox.add(gtk.Label(label))
            return hbox

    def create_gui(self):
        # Creates a empty list that contains previous screens
        self.prev_page = []

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
        self.mission_button = BlinkToggleButton()
        self.mission_button.add(self.build_icon("Uppdrag",
                                           "icons/emblem-important.png"))
        self.mission_button.connect("clicked", self.show_mission)
        self.mapobjecthandler.connect("got-new-mission", self.new_mission)
        self.menu_buttons["mission"] = self.mission_button

        add_object_button = gtk.ToggleButton()
        add_object_button.add(self.build_icon("Skapa",
                                              "icons/list-add.png"))
        add_object_button.connect("clicked", self.show_add_object)
        self.menu_buttons["add_object"] = add_object_button

        contacts_button = gtk.ToggleButton()
        contacts_button.add(self.build_icon("Kontakter",
                                            "icons/x-office-address-book.png"))
        contacts_button.connect("clicked", self.show_contacts)
        self.menu_buttons["contacts"] = contacts_button

        self.messages_button = BlinkToggleButton()
        self.messages_button.add(self.build_icon("Meddelande",
                                                 "icons/internet-mail.png"))
        self.messages_button.connect("clicked", self.show_messages) 
        self.textmessagehandler.connect("got-new-message", self.new_message)
        self.menu_buttons["messages"] = self.messages_button

        vbox.add(self.mission_button)
        vbox.add(add_object_button)
        vbox.add(contacts_button)
        vbox.add(self.messages_button)
        
        if config.client.type == 'commander':
            patient_journal_message = gtk.ToggleButton()
            patient_journal_message.add(self.build_icon("Patient-\njournal",
                                                        "icons/text-x-generic.png"))
            patient_journal_message.connect("clicked", self.show_patient_journal_message) 
            #self.textmessagehandler.connect("got-new-message", self.new_message)
            self.menu_buttons["patient_journal_message"] = patient_journal_message
            vbox.add(patient_journal_message)      

        # Right panel
        vbox_right = gtk.VBox(False, 0)
        panels.pack_start(vbox_right, True, True, 0)
        
        # adding the notification bar
        self.notifications = NotificationScreen()
        vbox_right.pack_start(self.notifications, False, False, 0)
        self.screens["notifications"] = self.notifications

        # add the map screen
        self.map = MapScreen(self.db)
        self.map.connect("object-clicked", self.change_object)
        vbox_right.pack_start(self.map, True, True, 0)
        self.screens["map"] = self.map

        # add the alarm screen
        self.alarm_screen = AlarmScreen(self.db)
        self.alarm_screen.connect("okbutton-alarm-clicked",
                                  self.back_button_function) 
        vbox_right.pack_start(self.alarm_screen, True, True, 0)
        self.screens["alarm"] = self.alarm_screen

        # adding messages screen
        self.message_screen = InboxScreen(self.db)
        vbox_right.pack_start(self.message_screen, True, True, 0)
        self.screens["message"] = self.message_screen
        
        self.new_message_screen = NewMessageScreen(self.db)
        self.new_message_screen.connect("okbutton_clicked_new_message",
                                        self.back_button_function) 
        vbox_right.pack_start(self.new_message_screen, True, True, 0)
        self.screens["new_message"] = self.new_message_screen
        
        self.outbox_screen = OutboxScreen(self.db)
        vbox_right.pack_start(self.outbox_screen, True, True, 0)
        self.screens["output"] = self.outbox_screen

        # add the obstacle screen
        self.obstacle_screen = ObstacleScreen(self.db)
        self.obstacle_screen.connect("okbutton-obstacle-clicked",
                                     self.back_button_function)
        vbox_right.pack_start(self.obstacle_screen, True, True, 0)
        self.screens["obstacle"] = self.obstacle_screen
        
        # add the change obstacle screen
        self.change_obstacle_screen = ChangeObstacleScreen(self.db)
        vbox_right.pack_start(self.change_obstacle_screen, True, True, 0)
        self.screens["change_obstacle"] = self.change_obstacle_screen
        
        # add the create_mission screen
        self.mission_screen = MissionScreen(self.db)
        self.mission_screen.connect("okbutton-mission-clicked",
                                    self.back_button_function)
        vbox_right.pack_start(self.mission_screen, True, True, 0)
        self.screens["make_mission"] = self.mission_screen

        # add the change mission screen
        self.change_mission_screen = ChangeMissionScreen(self.db)
        vbox_right.pack_start(self.change_mission_screen, True, True, 0)
        self.screens["change_mission"] = self.change_mission_screen
        
        self.unit_screen = UnitScreen()
        vbox_right.pack_start(self.unit_screen, True, True, 0)
        self.screens["view_unit"] = self.unit_screen

        self.faq_screen = FAQScreen(self.db)               
        vbox_right.pack_start(self.faq_screen, True, True, 0)
        self.screens["faq"] = self.faq_screen
        
        self.info_screen = MissionInfoScreen(self.db)               
        vbox_right.pack_start(self.info_screen, True, True, 0)
        self.screens["info"] = self.info_screen

        self.patient_journal_screen = PatientJournalScreen(self.db, self.queue)
        self.patient_journal_screen.connect("okbutton_clicked_PatientJournalScreen",
                                            self.back_button_function)               
        vbox_right.pack_start(self.patient_journal_screen, True, True, 0)
        self.screens["patient_journal"] = self.patient_journal_screen        

        # add the contact_screen and their menu
        self.contact_screen = ContactScreen(self.db)
        vbox_right.pack_start(self.contact_screen, True, True, 0)
        self.screens["contact"] = self.contact_screen
        
        # Videocamera
        self.cam_screen = CamScreen(self.db)
        self.cam_screen.button.connect("clicked", self.back_button_function)
        vbox_right.pack_start(self.cam_screen, True, True, 0)
        self.screens["camera"] = self.cam_screen
        
        #Contact menu
        self.contact_menu = gtk.HBox(False, 0)
        self.contact_menu.set_size_request(0, 60)
        vbox_right.pack_start(self.contact_menu, False, False, 0)
        self.screens["contact_menu"] = self.contact_menu
        call = gtk.Button("Röstsamtal")
        call.connect("clicked", self.sending_voip)
        video = gtk.Button("Videosamtal")
        video.connect("clicked", self.sending_vvoip)
        self.contact_menu.add(call)
        self.contact_menu.add(video)

        # Mission buttons and their menu
        self.mission_menu = gtk.HBox(True, 0)
        self.mission_menu.set_size_request(0, 60)
        vbox_right.pack_start(self.mission_menu, False, False, 0)
        self.screens["mission_menu"] = self.mission_menu

        info_button = gtk.Button()
        info_button.add(self.build_icon("Mina Uppdrag",
                                        "icons/emblem-important.png", "h"))
        info_button.connect("clicked", self.show_mission_info)
        journal_button = gtk.Button()
        journal_button.add(self.build_icon("Patient-\njournal",
                                           "icons/text-x-generic.png", "h"))
        journal_button.connect("clicked", self.show_journals)
        faq_button = gtk.Button()
        faq_button.add(self.build_icon("FAQ","icons/help-browser.png", "h"))
        faq_button.connect("clicked", self.show_faq)
        self.mission_menu.add(info_button)
        #self.mission_menu.add(status_button)
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
        self.message_menu.add(new_mess)
        self.message_menu.add(inbox)
        self.message_menu.add(outbox)
        
        self.patient_journal_message_screen = PatientJournalMessageScreen(self.db)
        self.journalhandler.connect("got-new-journal-request", self.patient_journal_message_screen.add_request)
        self.journalhandler.connect("got-new-journal-response",
                                    self.screens["patient_journal"].got_journal_response)
        vbox_right.pack_start(self.patient_journal_message_screen, True, True, 0)
        self.screens["patient_journal_message_screen"] = self.patient_journal_message_screen
        
        vbox2 = gtk.VBox(False,0)
        #panels.pack_start(vbox2, False, False, 0)
        vbox2.set_size_request(150,0)
        
        #self.activities = gtk.VBox(False,0)
        self.activities = Activities(self.db)
        vbox2.pack_start(self.activities, False, False, 0)
        self.screens["act"] = self.activities 
        #self.activities = Activities(self.db)
             
        #self.ac = Activities(self.db)
        #self.activities.add(self.ac)  

        # Add object buttons and their menu
        self.add_object_menu = gtk.HBox(True, 0)
        self.add_object_menu.set_size_request(0, 60)
        vbox_right.pack_start(self.add_object_menu, False, False, 0)
        self.screens["add_object_menu"] = self.add_object_menu
        
        create_alarm_button = gtk.Button("Larm")
        create_alarm_button.connect("clicked", self.create_alarm)
        create_obstacle_button = gtk.Button("Hinder")
        create_obstacle_button.connect("clicked", self.create_obstacle)
        self.add_object_menu.add(create_alarm_button)
        self.add_object_menu.add(create_obstacle_button)
        if config.client.type == 'commander':
            create_mission_button = gtk.Button("Uppdrag")
            create_mission_button.connect("clicked", self.create_mission)
            self.add_object_menu.add(create_mission_button)

        # add back- and ok-button (used in alarmscreen, obstaclescreen etc)
        self.buttons_box = gtk.HBox(True, 0)
        self.buttons_box.set_size_request(0, 60)
        self.screens["buttons"] = self.buttons_box
        
        back_button = gtk.Button()
        back_button.add(self.build_icon("Bakåt", "icons/edit-undo.png", "h"))
        self.buttons_box.pack_start(back_button)
        back_button.connect("clicked", self.back_button_function)

        ok_button = gtk.Button()
        ok_button.add(self.build_icon("OK", "icons/list-add.png", "h"))
        ok_button.connect("clicked", self.ok_button_function)
        ok_button.set_flags(gtk.CAN_DEFAULT)
        self.buttons_box.pack_start(ok_button)
        
        vbox_right.pack_start(self.buttons_box, False, False, 0)
        
        self.back_button_box = gtk.HBox(True, 0)
        self.back_button_box.set_size_request(0, 60)
        self.screens["back_button_box"] = self.back_button_box
        
        back_button2 = gtk.Button()
        back_button2.add(self.build_icon("Bakåt", "icons/edit-undo.png", "h"))
        self.back_button_box.pack_start(back_button2)
        back_button2.connect("clicked", self.back_button_function)
        
        vbox_right.pack_start(self.back_button_box, False, False, 0)
        
        vbox_right.pack_start(self.create_pj_message_buttons(), False, False, 0)

        vbox_right.pack_start(self.create_pj_request_buttons(), False, False, 0)

        vbox_right.pack_start(self.create_change_buttons(), False, False, 0)

        self.window.connect("destroy", lambda event: self.mainloop.quit())
        self.window.connect("key-press-event", self.on_key_press)
        self.window.connect("window-state-event", self.on_window_state_change)

        # Change to default True?
        self.window_in_fullscreen = False
        log.info("ClientGui created")

    def create_pj_message_buttons(self):
        pj_button_box = gtk.HBox(False, 10)
        pj_button_box.set_size_request(0, 60)
        self.screens["pj_button_box"] = pj_button_box
        
        
        no_button = gtk.Button("Neka")
        no_button.connect("clicked", self.no_button_function)
        no_button.set_flags(gtk.CAN_DEFAULT)
        pj_button_box.pack_start(no_button)
        
        ok_button = gtk.Button("Bevilja")
        ok_button.connect("clicked", self.ok_button_function)
        ok_button.set_flags(gtk.CAN_DEFAULT)
        pj_button_box.pack_start(ok_button)
        
        return pj_button_box

    def create_pj_request_buttons(self):
        pj_button_box = gtk.HBox(False, 10)
        pj_button_box.set_size_request(0, 60)
        self.screens["pj_request_button_box"] = pj_button_box
        
        back_button = gtk.Button()
        back_button.add(self.build_icon("Bakåt", "icons/edit-undo.png", "h"))
        pj_button_box.pack_start(back_button)
        back_button.connect("clicked", self.back_button_function)

        ok_button = gtk.Button("Begär ny journal")
        ok_button.connect("clicked", self.ok_button_function)
        ok_button.set_flags(gtk.CAN_DEFAULT)
        pj_button_box.pack_start(ok_button)
        
        return pj_button_box

    def create_change_buttons(self):
        # add back-, change- and delete-button (used in ChangeObstacleScreen etc)
        self.change_buttons = gtk.HBox(False, 0)
        self.change_buttons.set_size_request(0, 60)
        self.screens["change_buttons"] = self.change_buttons
        
        change_back_button = gtk.Button()
        change_back_button.add(self.build_icon("Bakåt", 
                                               "icons/edit-undo.png", "h"))
        self.change_buttons.pack_start(change_back_button)
        change_back_button.connect("clicked", self.back_button_function)
        
        delete_button = gtk.Button()
        delete_button.add(self.build_icon("Ta bort", 
                                          "icons/emblem-unreadable.png", "h"))
        delete_button.connect("clicked", self.delete_button_function)
        delete_button.set_flags(gtk.CAN_DEFAULT)
        self.change_buttons.pack_start(delete_button)

        change_button = gtk.Button()
        change_button.add(self.build_icon("Spara ändringar", 
                                          "icons/document-save.png", "h"))
        change_button.connect("clicked", self.change_button_function)
        change_button.set_flags(gtk.CAN_DEFAULT)
        self.change_buttons.pack_start(change_button)
        
        return self.change_buttons

    def new_message(self,event):
        print "*****************"
        print "GOT NEW MESSAGE!!"
        print "*****************"
        
        self.messages_button.set_attention(True)
        shared.util.set_color(0,255,0)
        shared.util.play_uri("snd/mail3b.wav")
        label = self.messages_button.get_child()
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
        
    def new_mission(self,event):
        shared.util.set_color(255,0,0)
        self.mission_button.set_attention(True)

    def change_object(self, event, object):
        keys = []
        for key in self.screens.keys():
                screen = self.screens[key]
                if screen.props.visible:
                    keys.append(key)
        self.prev_page.append(keys)
        if object.__class__ == POIData:
            # show the changeobstaclescreen
            self.change_obstacle(object)
        elif object.__class__ == MissionData:
            self.change_mission(object)
        elif object.__class__ == UnitData:
            self.view_unit(object)
            
    def change_obstacle(self, poi):
        self.show(["change_obstacle", "change_buttons"])
        self.screens["change_obstacle"].set_entries(poi)
        
    def change_mission(self, mission):
        self.show(["change_mission", "change_buttons"])
        self.screens["change_mission"].set_entries(mission)
        
    def view_unit(self, unit):
        self.show(["view_unit", "back_button_box"])
        self.screens["view_unit"].set_entries(unit)

    def sending_voip(self, event):
        msg = shared.data.Message(self.controller.name, 
                                  self.screens["contact"].name,
                                  type=shared.data.MessageType.voip, 
                                  subtype=shared.data.VOIPType.request,
                                  unpacked_data={"ip": get_ip(), "port": 5432,
                                                 "class": "dict"},
                                  prio = 5)
        self.queue.enqueue(msg.packed_data, msg.prio)
        self.out_call_popup(msg)
        
    def sending_vvoip(self, event):
        msg = shared.data.Message(self.controller.name, 
                                  self.screens["contact"].name,
                                  type=shared.data.MessageType.vvoip, 
                                  subtype=shared.data.VVOIPType.request,
                                  unpacked_data={"ip": get_ip(), "port1": 5432, 
                                                 "port2": 5434, "class": "dict"},
                                  prio = 5)
        self.queue.enqueue(msg.packed_data, msg.prio)
        self.out_call_popup(msg)
    
    def check_if_ok(self, msg):
        print "Check if ok-function"
        sender = msg.sender
        receiver = msg.receiver
        type = msg.type
        subtype = msg.subtype
        data = msg.unpacked_data
        print "Data:", data
        if type == shared.data.MessageType.voip:
            if subtype == shared.data.VOIPType.response:
                print "voip response"
                self.out_dialog.destroy()
                self.show_voice(ip=data["ip"], port=data["port"])
            if subtype == shared.data.VOIPType.request:
                shared.util.set_color(0,0,255)
                print "voip request"
                self.inc_call_popup(msg)
        elif type == shared.data.MessageType.vvoip:
            if subtype == shared.data.VVOIPType.response:
                print "vvoip response"
                self.out_dialog.destroy()
                self.show_cam(ip=data["ip"], port1=data["port1"],
                              port2=data["port2"])
            elif subtype == shared.data.VVOIPType.request:
                shared.util.set_color(0,0,255)
                print "vvoip request"
                self.inc_call_popup(msg)
    
    def start_voip(self, msg):
        print "Staring voip"
        sender = msg.sender
        receiver = msg.receiver
        type = msg.type
        subtype = msg.subtype
        data = msg.unpacked_data
        message = shared.data.Message(self.controller.name, sender,
                                      type=shared.data.MessageType.voip, 
                                      subtype=shared.data.VOIPType.response,
                                      unpacked_data={"ip": get_ip(), "port": 5432, 
                                                     "class": "dict"},
                                      prio = 5)
        self.queue.enqueue(message.packed_data, message.prio)
        self.show_voice(ip=data["ip"], port=data["port"])
        
    def start_vvoip(self, msg):
        print "Staring vvoip"
        sender = msg.sender
        receiver = msg.receiver
        type = msg.type
        subtype = msg.subtype
        data = msg.unpacked_data
        message = shared.data.Message(self.controller.name, sender,
                                  type=shared.data.MessageType.vvoip, 
                                  subtype=shared.data.VVOIPType.response,
                                  unpacked_data={"ip": get_ip(), "port1": 5432,
                                                 "port2": 5434, "class": "dict"},
                                  prio = 5)
        self.queue.enqueue(message.packed_data, message.prio)
        self.show_cam(ip=data["ip"], port1=data["port1"], port2=data["port2"])
    
    def inc_call_popup(self, msg):
        sender = msg.sender
        print "Inkommande samtal = popup"
        inc_dialog = gtk.Dialog("Samtal",
                 self.window,  #the toplevel wgt of your app
                 gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  #binary flags or'ed together
                 )
        who = gtk.Label(str(sender+" ringer..."))
        who.show()
        inc_dialog.set_size_request(400,200)
        #dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        hang_up_button = gtk.Button("  Lägg på  ")
        inc_dialog.action_area.pack_start(hang_up_button)
        def hang_up(event):
            shared.util.set_color(0,0,0)
            # @todo: return nack if we dont want to answer
            print "upptaget"
            inc_dialog.destroy()
        hang_up_button.connect("clicked", hang_up)
        
        answer_button = gtk.Button("     Svara     ")
        inc_dialog.action_area.pack_start(answer_button)
        def answer(event):
            shared.util.set_color(0,0,0)
            if msg.type == shared.data.MessageType.voip:
                self.start_voip(msg)
                inc_dialog.destroy()
            elif msg.type == shared.data.MessageType.vvoip:
                self.start_vvoip(msg)
                inc_dialog.destroy()
        answer_button.connect("clicked", answer)
        
        inc_dialog.vbox.pack_start(who)
        question = gtk.Label("Vill du svara?")
        question.show()
        inc_dialog.vbox.pack_start(question)
        inc_dialog.show_all()
        
    def out_call_popup(self, msg):
        print "Utgående samtal = popup"
        if self.screens["contact"].name == None:
            return 0
        
        self.out_dialog = gtk.Dialog("Samtal",
                 self.window,  #the toplevel wgt of your app
                 gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  #binary flags or'ed together
                 ("     Lägg på     ", 77))
        
        who = gtk.Label("Du ringer till "+self.screens["contact"].name)
        who.show()
        #dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.out_dialog.vbox.pack_start(who)
        self.out_dialog.set_size_request(400,200)
        #dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.out_dialog.show()
        result = self.out_dialog.run()
        if result == 77:
            if msg.type == shared.data.MessageType.voip:
                print "Lägger på"
            elif msg.type == shared.data.MessageType.vvoip:
                print "Lägger på"
        self.out_dialog.destroy()

    def start(self, event):
        # only do start method once
        self.db.disconnect(self.ready_handler_id)
        # start controller
        self.start_controller()
        self.message_dispatcher.process_items()
        # show gui
        self.window.show_all()
        self.show_default()
        # connect service level signal from controller
        self.controller.interface.connect_to_signal("signal_changed_service_level",
                                                    self.update_service_level)
        self.message_dispatcher.connect_to_type(shared.data.MessageType.vvoip,
                                                self.check_if_ok)
        self.message_dispatcher.connect_to_type(shared.data.MessageType.voip,
                                                self.check_if_ok)

    def run(self):
        '''
        Main GUI loop
        '''
        gobject.threads_init()
        self.ready_handler_id = self.db.connect("ready", self.start)
        self.db.ensure_ids()
        while self.mainloop.is_running():
            try:
                self.mainloop.run()
            except KeyboardInterrupt:
                self.mainloop.quit()

    def start_controller(self):
        '''
        Create and start ClientController
        '''
        # My initial status
        status = u"Available"
        self.controller = controller.ClientController(status, self.db)
        self.mapobjecthandler.controller = self.controller

    def update_service_level(self, service_level):
        self.screens["notifications"].update_label(service_level)
        unpacked_data = {"class": "dict", "service_level": service_level}
        if service_level == "ad-hoc" or service_level == "mega-low":
            pass
        else:
            msg = Message(self.controller.name, "server",
                          shared.data.MessageType.service_level,
                          unpacked_data = unpacked_data)
            self.queue.enqueue(msg.packed_data, msg.prio)

    def back_button_function(self, event):
        self.show(self.prev_page[-2])

    def ok_button_function(self, event):
        for screen in self.screens.values():
            if screen.props.visible and isinstance(screen, Screen):
                screen.ok_button_function(event)
                
    def no_button_function(self, event):
        for screen in self.screens.values():
            if screen.props.visible and isinstance(screen, Screen):
                screen.no_button_function(event)

    def change_button_function(self, event):
        for screen in self.screens.values():
            if screen.props.visible and isinstance(screen, Screen):
                screen.change_button_function(event)
        self.back_button_function(event)
                
    def delete_button_function(self, event):
        for screen in self.screens.values():
            if screen.props.visible and isinstance(screen, Screen):
                screen.delete_button_function(event)
        self.back_button_function(event)

    # mission view event handlers
    def show_mission(self, event):
        shared.util.set_color(0,0,0)
        self.mission_button.set_attention(False)
        self.toggle_show("mission", ["notifications", "map", "mission_menu"], 
                         "Här visas information relaterade till dina uppdrag")

    # mission buttons event handlers
    def show_mission_info(self, event):
        self.show(["info", "change_buttons"])
        missions = []
        for m in self.db.get_all_missions():
            for u in m.units:
                if u.name == config.client.name:
                    missions.append(m)
        self.screens["info"].set_missions(missions)

    def show_status(self, event):
        self.toggle_show("mission", ["notifications", "status", "buttons"], 
                         "Här kan du välj en status")

        combo = self.screens["status"].combo_box
        combo.get_model().clear()
        combo.append_text("Välj uppdrag...")
        combo.set_active(0)
        for mission in self.controller.missions:
            combo.append_text(mission.event_type)
    
    def show_journals(self, event):
        self.toggle_show("mission", ["notifications", "patient_journal", "pj_request_button_box"], 
                         "Här kan du hämta patient journaler")
    
    def show_faq(self, event):
        self.toggle_show("mission", ["notifications", "faq", "back_button_box"], 
                         "Här kan du få information om vanliga sjukdomar")
        
    # add object view event handlers
    def show_add_object(self, event):
        self.toggle_show("add_object", 
                         ["notifications", "map","add_object_menu"], 
                         "Välj en koordinat och sedan typ av objekt")
    
    # add object buttons event handlers
    def create_alarm(self, event):
        self.show(["alarm", "buttons"])
        self.screens["alarm"].coordx_entry.set_text(str(self.screens["map"].gps_x))
        self.screens["alarm"].coordy_entry.set_text(str(self.screens["map"].gps_y))
            
    def create_obstacle(self, event):
        self.show(["obstacle", "buttons"])
        self.screens["obstacle"].location_entry2.set_text(str(self.screens["map"].gps_x))
        self.screens["obstacle"].location_entry3.set_text(str(self.screens["map"].gps_y))
    
    def create_mission(self, event):
        self.show(["make_mission", "buttons"])
        self.screens["make_mission"].coordx_entry.set_text(str(self.screens["map"].gps_x))
        self.screens["make_mission"].coordy_entry.set_text(str(self.screens["map"].gps_y))

        combo = self.screens["make_mission"].combo_box
        combo.get_model().clear()
        combo.append_text("Välj larm...")
        combo.set_active(0)
        alarms = self.db.get_all_alarms()
        for alarm in alarms:
            combo.append_text(alarm.event)

    def create_new_message(self, event):
        self.toggle_show("messages", ["notifications", "new_message","buttons"], "Här kan du skriva ett nytt meddelanden")
        #self.show(["new_message", "buttons"])
        
    def show_cam(self,ip, port1, port2, event = None):
        self.screens["camera"].start_vvoip(ip, port1, port2)
        self.show(["camera"])
        
    def show_voice(self, ip, port, event = None):
        self.screens["camera"].start_voip(ip, port)
        self.show(["camera"])
        
    def show_outbox(self, event):
        self.toggle_show("messages", ["notifications", "output","back_button_box"], "Här visas dina utgångna meddelanden")
        #self.show(["output", "message_menu"])
       
        combo = self.screens["output"].combo_box
        combo.get_model().clear()
        combo.append_text("Välj textmeddelande...")
        combo.set_active(0)
         
        for textmessages in self.db.textmessages():
            list = []
            for unit in textmessages.units:
                list.append(unit)
            names = [u.name for u in list][:3]
            unitnames = ", ".join(names)
            if len(list) > 3:
                unitnames += "..."
            receiverandsubject = "Till: " + str(unitnames) + "    Ämne: " + str(textmessages.subject)
            
            if config.client.name == textmessages.sender:
                combo.append_text(receiverandsubject)
       
    def show_inbox(self, event):
        self.toggle_show("messages", ["notifications", "message","back_button_box"], "Här visas dina inkomna meddelanden")
        
        self.update_messagesbox(event)
        shared.util.set_color(0,0,0)
          
        self.messages_button.set_attention(False)
        label = self.messages_button.get_child()
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        
    # contacts view event handlers
    def show_contacts(self,event):
        self.toggle_show("contacts", ["notifications","contact", "contact_menu"], "Här visas dina kontakter och du kan ringa till dem")
        screen = self.screens["contact"]
        screen.buttons = []
        for child in screen.vbox.get_children():
            screen.vbox.remove(child)
        for u in self.db.get_all_units():
            button = gtk.ToggleButton("%s" % u.name)
            button.show()
            screen.vbox.pack_start(button)
            button.connect("pressed", screen.select_contacts)
            screen.buttons.append(button)

    # messages view event handlers
    def show_messages(self, event):
        self.toggle_show("messages", ["notifications", "map","message_menu"], "Här kan du hantera dina meddelanden")
        
        self.update_messagesbox(event)
            
    def update_messagesbox(self, event):
        combo = self.screens["message"].combo_box
        combo.get_model().clear()
        combo.append_text("Välj textmeddelande...")
        combo.set_active(0)
        #self.db.units_in_text()
                  
        for textmessages in self.db.textmessages():
            #print textmessages.senderandsubject
            senderandsubject = "från: " + str(textmessages.sender) + "    Ämne: " + str(textmessages.subject)
            #textmessages.
            if config.client.name != textmessages.sender:
                combo.append_text(senderandsubject)
                
    def show_patient_journal_message(self, event):
        self.toggle_show("patient_journal_message", ["notifications", "patient_journal_message_screen","pj_button_box"], "Här visas dina meddelanden")
        
        self.screens["patient_journal_message_screen"].update_list()

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
        self.screens["notifications"].show_all()
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

