import gtk
import gobject
import math

class BlinkButton(gtk.Button):

    active_color = gtk.gdk.color_parse("#F8F")
    interval = 10
    direction = 1
    t = 0
    def __init__(self, label):
        gtk.Button.__init__(self, label)


    def set_attention(self, attention=True):
        if attention:
            gobject.timeout_add(self.interval, self.pulse)
        else:
            self.clear()

    def pulse(self):
        self.t += 0.1
        a = 0.75 + 0.25*(math.sin(self.t)+1)/2
        c = self.active_color
        new_color = gtk.gdk.Color(int(c.red*a), int(c.green*a), int(c.blue*a))
        self.modify_bg(gtk.STATE_NORMAL, new_color)
        self.modify_bg(gtk.STATE_PRELIGHT, new_color)
        self.modify_bg(gtk.STATE_ACTIVE, new_color)
        gobject.timeout_add(self.interval, self.pulse)

    def clear(self):
        pass




if __name__ == "__main__":
    win = gtk.Window()

    button = BlinkButton("HellO")
    button.set_attention()
    win.add(button)
    win.show_all()
    win.resize(200, 100)

    win.connect("destroy", gtk.main_quit)

    gtk.main()
