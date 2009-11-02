# -*- coding: utf-8 -*-
import gtk
import gobject
import shared.data
import gui
import pango

class MissionScreen(gtk.ScrolledWindow, gui.Screen):
    
    selected_type = None
    
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        
        # set automatic horizontal and vertical scrolling
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        def new_entry(labeltext):
            label = gtk.Label(labeltext)
            label.set_alignment(0, 0.5)
            entry = gtk.Entry()
            entry.set_max_length(300)
            entry.set_text("")
            entry.select_region(0, len(entry.get_text()))
            return (label, entry)
        
        # create layout boxes
        main_box = gtk.HBox(False,)
        self.add_with_viewport(main_box)
        left_box = gtk.VBox(True,0)
        right_box = gtk.VBox(True,0)
        main_box.pack_start(left_box,False,False,10)
        main_box.add(right_box)
        
        # create type label
        type_label = gtk.Label("Inkomna larm:")
        left_box.pack_start(type_label, True, True, 0)
        
        # create and pack combobox
        combo_box = gtk.combo_box_new_text()
        combo_box.set_size_request(300,50)
        right_box.pack_start(combo_box, True, False, 0)
        
#        label, self.location_entry = new_entry("Nytt uppdrag:")
#        left_box.add(label)
#        right_box.add(self.location_entry)
        
        new_mission_label = gtk.Label("Nytt uppdrag:")
        new_mission_label.set_alignment(0, 0.5)
        invisible_label = gtk.Label("")
        left_box.add(new_mission_label)
        right_box.add(invisible_label)
        
        # create entries
        label, self.event_entry = new_entry("Händelse:")
        label.set_alignment(0.5, 0.5)
        label.modify_font(pango.FontDescription("sans 12"))
        left_box.add(label)
        right_box.add(self.event_entry)
        
        label, self.location_entry = new_entry("Skadeplats:")
        label.set_alignment(0.5, 0.5)
        label.modify_font(pango.FontDescription("sans 12"))
        left_box.add(label)
        right_box.add(self.location_entry)

        label, self.hurted_entry = new_entry("Antal skadade:")
        label.set_alignment(0.5, 0.5)
        label.modify_font(pango.FontDescription("sans 12"))
        left_box.add(label)
        right_box.add(self.hurted_entry)

        contact = gtk.Label("Kontaktperson:")
        label.set_alignment(0.5, 0.5)
        label.modify_font(pango.FontDescription("sans 12"))
        invisible_label = gtk.Label("")
        left_box.add(contact)
        right_box.add(invisible_label)
        
        label, self.name_entry = new_entry("Namn:")
        label.set_alignment(0.5, 0.5)
        label.modify_font(pango.FontDescription("sans 12"))
        left_box.add(label)
        right_box.add(self.name_entry)
        
        label, self.number_entry = new_entry("Nummer:")
        label.set_alignment(0.5, 0.5)
        label.modify_font(pango.FontDescription("sans 12"))
        left_box.add(label)
        right_box.add(self.number_entry)

        label, self.random_entry = new_entry("Övrigt:")
        left_box.add(label)
        right_box.add(self.random_entry)
        
        
        choose_units_button = gtk.Button("Välj enheter")
        label = choose_units_button.get_child()
#        choose_units_button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("red"))
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))

#        choose_units_button.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))

        choose_units_button.connect("clicked", self.select_units)
        unit_label = gtk.Label("Valda enheter")

#        eb = gtk.EventBox()
#        eb.add(choose_units_button)
#        eb.modify_bg(gtk.STATE_SELECTED | gtk.STATE_NORMAL | gtk.STATE_ACTIVE, gtk.gdk.color_parse("green"))


        left_box.add(choose_units_button)
        right_box.add(unit_label)
        
        # add selectable types
        for type in shared.data.ObstacleType.__dict__.keys():
            if type[0] != "_":
                combo_box.append_text(type)

        # add event handler
        combo_box.connect('changed', self.select_type)

        # set the first item added as active
        combo_box.set_active(0)

        # show 'em all! (:
        main_box.show_all()

    '''Handle events
    '''

    def select_type(self, combobox):
        '''
        Call when combobox changes to switch obstacle type.
        @param combobox: the changed combobox
        '''
        # set the selected type
        self.selected_type = combobox.get_active()
        
    def select_units(self, event):
        dialog = gtk.Dialog("Välj enheter",
                 None,  #the toplevel wgt of your app
                 gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  #binary flags or'ed together
                 ("     Avbryt     ", 666, "  Ok  ", 77))
        
        #Units to choose

        unit1 = gtk.ToggleButton("Enhet 1")
        unit1.show()
        unit2 = gtk.ToggleButton("Enhet 2")
        unit2.show()
        unit3 = gtk.ToggleButton("Enhet 3")
        unit3.show()
        unit4 = gtk.ToggleButton("Enhet 4")
        unit4.show()
        dialog.vbox.pack_start(unit1)
        dialog.vbox.pack_start(unit2)
        dialog.vbox.pack_start(unit3)
        dialog.vbox.pack_start(unit4)
        #dialog.add(table)
        
        
        
        
        dialog.set_size_request(400,400)


        dialog.show()
        result = dialog.run()
        if result == 77:
            print "Skapade uppdrag"
            dialog.destroy()
           
        elif result == 666:
            print "Avbrot"
        dialog.destroy()
