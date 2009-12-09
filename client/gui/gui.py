import gtk
import pango

class Screen(gtk.Widget):
    name = "Screen"
    def __init__(self, name):
        self.name = name

    def ok_button_function(self, event):
        pass

    def no_button_function(self, event):
        pass

    def create_entry(self, labeltext, parent):
        ''' Creates a label and en entry in a HBox and adds the HBox to
            parent. Returns entry.
        '''
        hbox = gtk.HBox(True,0)
        label = gtk.Label(labeltext)
        label.set_alignment(0, 0.5)
        entry = gtk.Entry()
        entry.set_max_length(300)
        entry.set_text("")
        # TODO: usuable?
        entry.select_region(0, len(entry.get_text()))
        hbox.add(label)
        hbox.add(entry)
        parent.add(hbox)
        return entry

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
    
    def new_label(self, labeltext, left_box, right_box):
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
        invisible.modify_font(pango.FontDescription("sans 14"))
        invisible.set_alignment(0, 0.5)
        right_box.pack_start(invisible)
