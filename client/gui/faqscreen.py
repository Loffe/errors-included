# -*- coding: utf-8 -*-

import gtk
import gobject
import map.mapdata
import shared.data
import datetime
import gui
import pango

class FAQScreen(gtk.ScrolledWindow, gui.Screen):
    '''
    The screen in which you create a new alarm.
    '''

    def __init__(self, db):
        '''
        Constructor. Create the faqscreen and its entries.
        '''
        gtk.ScrolledWindow.__init__(self)

        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        # create layout boxes
        main_box = gtk.VBox(False,0)
        self.add_with_viewport(main_box)
        
        #Load texts
        self.diabetes = gtk.TextBuffer()
        self.diabetes.set_text(open('../shared/FAQ/diabetes.txt', 'r').read().encode('utf-8'))
        self.hemorojder = gtk.TextBuffer()
        self.hemorojder.set_text(open('../shared/FAQ/hemorojder.txt', 'r').read().encode('utf-8'))
        self.svinis = gtk.TextBuffer()
        self.svinis.set_text(open('../shared/FAQ/svininfluensan.txt', 'r').read().encode('utf-8'))
        
        
        
        # create and pack combobox
        self.combo_box = gtk.combo_box_new_text()
        #combo_box.set_size_request(300,50)
        main_box.pack_start(self.combo_box, False, False, 0)
        self.textview = gtk.TextView()
        self.textview.set_editable(False)
        self.textview.set_size_request(400,-1)
        main_box.pack_start(self.textview)
        # add event handler
        self.combo_box.connect('changed', self.selected)
        
        self.combo_box.append_text("Välj sjukdom...")
        self.combo_box.append_text("Diabetes")
        self.combo_box.append_text("Hemorojder")
        self.combo_box.append_text("Svininfluensa")
        # set the first item added as active
        self.combo_box.set_active(0)

        # show 'em all! (:
        main_box.show_all()
        
    def selected(self, combobox):
        
        self.selected = self.combo_box.get_active_text()
        if self.selected == "Diabetes":
            self.textview.set_buffer(self.diabetes)
        elif self.selected == "Hemorojder":
            self.textview.set_buffer(self.hemorojder)
        elif self.selected == "Svininfluensa":
            self.textview.set_buffer(self.svinis)
        