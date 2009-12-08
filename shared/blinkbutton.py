import gtk
import gobject
import math

class BlinkToggleButton(gtk.ToggleButton):

    color1 = gtk.gdk.color_parse("#FA0")
    color2 = gtk.gdk.color_parse("#FFF")
    interval = 20
    speed = 0.05
    t = 0
    attention = False
    def __init__(self, label=None):
        gtk.Button.__init__(self, label)
        self.default_bg = self.get_style().bg


    def set_attention(self, attention=True):
        self.attention = attention
        if attention:
            self.t = 0
            gobject.timeout_add(self.interval, self.pulse)
        else:
            self.clear()

    def blend(self, c1, c2, t):
        return gtk.gdk.Color( int(c1.red * (1-t) + c2.red * t),
                              int(c1.green * (1-t) + c2.green * t),
                              int(c1.blue * (1-t) + c2.blue * t))

    def pulse(self):
        self.t += 0.05
        a = (math.sin(self.t)+1)/2
        new_color = self.blend(self.color1, self.color2, a)
        self.modify_bg(gtk.STATE_NORMAL, new_color)
        self.modify_bg(gtk.STATE_PRELIGHT, new_color)
        self.modify_bg(gtk.STATE_ACTIVE, new_color)
        if self.attention:
            gobject.timeout_add(self.interval, self.pulse)
        else:
            self.clear()

    def clear(self):
        self.modify_bg(gtk.STATE_NORMAL, self.default_bg[2])
        self.modify_bg(gtk.STATE_ACTIVE, self.default_bg[1])
        self.modify_bg(gtk.STATE_PRELIGHT, self.default_bg[2])




if __name__ == "__main__":
    win = gtk.Window()

    button = BlinkToggleButton("HellO")
    button.set_attention()
    def stop(event):
        print "clicked"
        button.set_attention(not button.attention)

    button.connect("clicked", stop)
    win.add(button)
    win.show_all()
    win.resize(200, 100)

    win.connect("destroy", gtk.main_quit)

    gtk.main()
