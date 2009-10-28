#!/usr/bin/python2.4
import osso
import hildon
import gtk

def send_rpc(widget, osso_c):
    osso_c.rpc_run("spam.eggs.osso_test_receiver",
                   "/spam/eggs/osso_test_receiver",
                   "spam.eggs.osso_test_receiver",
                   "do_something")

    print "RPC sent"
    
osso_c = osso.Context("osso_test_sender", "0.0.1", False)

window = hildon.Window()
window.connect("destroy", gtk.main_quit)
send_button = gtk.Button("Send RPC")
window.add(send_button) 
send_button.connect("clicked",
                    send_rpc, osso_c)
window.show_all()
gtk.main()  
