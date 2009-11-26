import gtk
import pango

class Screen(gtk.Widget):
    name = "Screen"
    def __init__(self, name):
        self.name = name

    def ok_button_function(self, event):
        
        print "Default ok buttton pressed"

    def new_entry(self, labeltext, left_box, right_box):
        label = gtk.Label(labeltext)
        label.set_alignment(0, 0.5)
        label.modify_font(pango.FontDescription("sans 12"))
        entry = gtk.Entry()
        entry.set_max_length(300)
        entry.set_text("")
        entry.select_region(0, len(entry.get_text()))
        left_box.pack_start(label)
        right_box.pack_start(entry)
        self.entries.append(entry)
        return entry
    
    def new_coordlabel(self, labeltext, left_box, right_box):
        label = gtk.Label(labeltext)
        label.modify_font(pango.FontDescription("sans 12"))
        label.set_alignment(0, 0.5)
#        rightlabel.select_region(0, len(rightlabel.get_text()))
        rightlabel = gtk.Label()
        rightlabel.modify_font(pango.FontDescription("sans 12"))
        rightlabel.set_alignment(0, 0.5)
        left_box.pack_start(label)
        right_box.pack_start(rightlabel)
        self.entries.append(rightlabel)
        return rightlabel

    def new_section(self, title, left_box, right_box):
        label = gtk.Label(title)
        label.modify_font(pango.FontDescription("sans 14"))
        label.set_alignment(0, 0.5)
        left_box.pack_start(label)
        invisible = gtk.Label()
        invisible.set_alignment(0, 0.5)
        right_box.pack_start(invisible)
