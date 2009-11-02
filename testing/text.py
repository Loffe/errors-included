import pygtk
pygtk.require('2.0')
import gtk

class text:
    entry = None
    entry2 = None
    entry3 = None
    
    def WindowDeleteEvent(self, widget, event):
        # return false so that window will be destroyed
        return False

    def WindowDestroy(self, widget, *data):
        # exit main loop
        gtk.main_quit()
        
    def enter_callback(self, widget, entry, entry2, entry3):
        entry_text = entry.get_text()
        entry2_text = entry2.get_text()
        entry3_text = entry3.get_text()
        print (entry_text, entry2_text, entry3_text)

    def __init__(self):
        # create the top level window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Mission-2")
        window.set_default_size(200, 100)
        window.connect("delete-event", self.WindowDeleteEvent)
        window.connect("destroy", self.WindowDestroy)
        # create the table and pack into the window
        table = gtk.Table(2, 2, False)
        window.add(table)
        # create the layout widget and pack into the table
        self.layout = gtk.Layout(None, None)
        self.layout.set_size(100, 1000)
        table.attach(self.layout, 0, 1, 0, 1, gtk.FILL|gtk.EXPAND,
                     gtk.FILL|gtk.EXPAND, 0, 0)
        # create the scrollbars and pack into the table
        vScrollbar = gtk.VScrollbar(None)
        table.attach(vScrollbar, 1, 2, 0, 1, gtk.FILL|gtk.SHRINK,
                     gtk.FILL|gtk.SHRINK, 0, 0)
        # tell the scrollbars to use the layout widget's adjustments
        vAdjust = self.layout.get_vadjustment()
        vScrollbar.set_adjustment(vAdjust)    
   
        self.entry = gtk.Entry()
        self.entry.set_max_length(200)
        self.entry.connect("activate", self.enter_callback, self.entry)
        self.entry.set_text("")
        self.entry.insert_text("", len(self.entry.get_text()))
        self.entry.select_region(0, len(self.entry.get_text()))
        self.layout.put(self.entry,0,0)
        self.entry.show()
        
        self.entry2 = gtk.Entry()
        self.entry2.set_max_length(200)
        self.entry2.connect("activate", self.enter_callback, self.entry2)
        self.entry2.set_text("")
        self.entry2.insert_text("", len(self.entry2.get_text()))
        self.entry2.select_region(0, len(self.entry.get_text()))
        self.layout.put(self.entry2,0,100)
        self.entry2.show()
        
        self.entry3 = gtk.Entry()
        self.entry3.set_max_length(200)
        self.entry3.connect("activate", self.enter_callback, self.entry3)
        self.entry3.set_text("")
        self.entry3.insert_text("", len(self.entry3.get_text()))
        self.entry3.select_region(0, len(self.entry.get_text()))
        self.layout.put(self.entry3,0,200)
        self.entry3.show()
        
        button = gtk.Button("Enter!")
        button.connect("clicked", self.enter_callback, self.entry, self.entry2, self.entry3)
        self.layout.put(button, 0, 300)
        
        window.show_all()
        
def main():
    # enter the main loop
    gtk.main()
    return 0

if __name__ == "__main__":
    text()
    main()          