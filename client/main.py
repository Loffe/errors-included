#!/usr/bin/env python
# coding: utf-8
import gtk
import hildon
import gobject
import pango

from gui.mapscreen import MapScreen
from gui.alarmscreen import AlarmScreen
from gui.messagescreen import MessageScreen

class ClientGui(hildon.Program):
    '''
    The main GUI-process of the client
    '''
    
    ''' create GUI Structure
    '''
    def __init__(self):
        '''
        Constructor. Creates the GUI (window and containing components).
        '''
        hildon.Program.__init__(self)
        self.window = hildon.Window()
        self.window.set_title("ClientGui")
        self.add_window(self.window)

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

        contacts_button = gtk.ToggleButton("Kontakt")
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

        # adding the map screen
        self.map = MapScreen()
        vbox_right.pack_start(self.map, True, True, 0)
        self.screens["map"] = self.map

        # adding the alarm screen
        self.alarm_screen = AlarmScreen()
        vbox_right.pack_start(self.alarm_screen, True, True, 0)
        self.screens["alarm"] = self.alarm_screen
        
        # adding messages screen
        self.message_screen = MessageScreen()
        vbox_right.pack_start(self.message_screen, True, True, 0)
        self.screens["message"] = self.message_screen
        
        # Mission buttons and their menu
        self.mission_menu = gtk.HBox(False, 0)
        self.mission_menu.set_size_request(0, 75)
        vbox_right.pack_start(self.mission_menu, False, False, 0)
        self.screens["mission_menu"] = self.mission_menu

        info_button = gtk.Button("Info")
        info_button.connect("clicked", self.show_mission_info)
        status_button = gtk.Button("Status")
        status_button.connect("clicked", self.show_status)
        journal_button = gtk.Button("Patient\nJournal")
        faq_button = gtk.Button("FAQ")
        self.mission_menu.add(info_button)
        self.mission_menu.add(status_button)
        self.mission_menu.add(journal_button)
        self.mission_menu.add(faq_button)

        # Add object buttons and their menu
        self.add_object_menu = gtk.HBox(False, 0)
        self.add_object_menu.set_size_request(0, 75)
        vbox_right.pack_start(self.add_object_menu, False, False, 0)
        self.screens["add_object_menu"] = self.add_object_menu
        
        create_alarm_button = gtk.Button("Larm")
        create_alarm_button.connect("clicked", self.create_alarm)
        create_obstacle_button = gtk.Button("Hinder")
        create_mission_button = gtk.Button("Uppdrag")
        self.add_object_menu.add(create_alarm_button)
        self.add_object_menu.add(create_obstacle_button)
        self.add_object_menu.add(create_mission_button)

        self.window.connect("destroy", gtk.main_quit)
        self.window.connect("key-press-event", self.on_key_press)
        self.window.connect("window-state-event", self.on_window_state_change)

        # Change to default True?
        self.window_in_fullscreen = False
        
    def run(self):
        '''
        Main GUI loop
        '''
        self.window.show_all()
        self.show_default()
        gtk.main()
    
    ''' Handle events
    '''
    # mission view event handlers
    def show_mission(self,event):
        self.toggle_show("mission", ["notifications", "map", "mission_menu"], "Här visas dina uppdrag")
        
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
        pass


    # add object view event handlers
    def show_add_object(self, event):
        self.toggle_show("add_object", ["notifications", "map","add_object_menu"], "Här kan du lägga till ett objekt")
        
    def create_alarm(self, event):
        self.show(["alarm"])
    
    def create_obstacle(self, event):
        pass
    
    def create_mission(self, event):
        pass


    # contacts view event handlers
    def show_contacts(self,event):
        self.toggle_show("contacts", [])


    # messages view event handlers
    def show_messages(self, event):
        self.toggle_show("messages", ["notifications", "message"], "Här visas dina meddelanden")


    # show certain screen methods
    def toggle_show(self, button_key, screen_keys, notification_text = ""):
        if self.menu_buttons[button_key].get_active():
            for menu_button in self.menu_buttons.keys():
                if menu_button != button_key:
                    self.menu_buttons[menu_button].set_active(False)
            for key in self.screens.keys():
                self.screens[key].hide_all()
            self.screens["notifications"].set_label(notification_text)
            for key in screen_keys:
                self.screens[key].show_all()
        else:
            self.show_default()
    
    def show(self, keys):
        for key in self.screens.keys():
            self.screens[key].hide_all()
        for key in keys:
            self.screens[key].show_all()
            
    def show_default(self):
        for key in self.screens.keys():
            self.screens[key].hide_all()
        self.screens["notifications"].set_label("Team Med Fel")
        self.screens["notifications"].show()
        self.screens["map"].show()
#        self.map.show()


    # handle key press events
    def on_key_press(self, widget, event, *args):
        # react on fullscreen button press
        if event.keyval == gtk.keysyms.F6:
            if self.window_in_fullscreen:
                self.window.unfullscreen()
            else:
                self.window.fullscreen()
        # Zoom -
        if event.keyval == gtk.keysyms.F8:
            self.map.zoom("-")
        # Zoom +
        elif event.keyval == gtk.keysyms.F7:
            self.map.zoom("+")  

    def on_window_state_change(self, widget, event, *args):
        if event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN:
            self.window_in_fullscreen = True
        else:
            self.window_in_fullscreen = False  

# den här borde skapa nya vyer av mission och kartan
if __name__ == "__main__":
    app = ClientGui()
    app.run()
