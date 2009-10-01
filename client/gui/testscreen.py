import gtk

import gui
import socket

class TestScreen(gtk.VBox, gui.Screen):

    def __init__(self):
        gtk.VBox.__init__(self, False)

        ip_entry = gtk.Entry()
        self.pack_start(ip_entry, False)

        textview = gtk.TextView()
        textview.set_editable(False)
        self.pack_start(textview, True)

        entry = gtk.Entry()
        self.pack_start(entry, False)

        button = gtk.Button("Send")
        button.connect("clicked", self.send_message)
        self.pack_start(button, False)

        self.show_all()

        buffer = textview.get_buffer()
        buffer.set_text("Hejsan\noch hall")

        self.ip_entry = ip_entry
        self.textview = textview
        self.entry = entry
        self.button = button

    def open_socket(self):
        host = self.ip_entry.get_text()
        port = 50000
        self.size = 1024
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host,port))
        except socket.error, (value,message):
            if s:
                s.close()
        self.socket = s

    def send_message(self, event):
        self.open_socket()
        send_data = self.entry.get_text()
        if len(send_data) <= 1:
            return
        self.socket.send(send_data)

        recv_data = self.socket.recv(self.size)
        buffer = self.textview.get_buffer()
        iter = buffer.get_end_iter()

        buffer.insert(iter, recv_data + "\n")

        print 'Recieved:', recv_data
