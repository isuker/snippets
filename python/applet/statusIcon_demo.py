#!/usr/bin/python

import pygtk
import gtk
pygtk.require('2.0')

class StatusIconDemo:
    """This is a demo to show GtkStatusIcon usage
         Display an icon in the system tray"""

    def __init__(self, message):
        self.tray = gtk.status_icon_new_from_stock(gtk.STOCK_QUIT)
        self.msg = message
        self.tray.connect('popup-menu', self.on_right_click, self.msg)

    def on_right_click(self, icon, event_button, event_time, data=None):
        self.make_menu(event_button, event_time, data)

    def show_message(self, item, message):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_border_width(10)
        window.set_position(gtk.WIN_POS_CENTER)

        text = gtk.Label(message)
        window.add(text)
        text.show()
        window.show()

        window.connect("destroy", window.destroy)

    def make_menu(self, event_button, event_time, data):
        menu = gtk.Menu()

        # show data string
        item = gtk.MenuItem("Demo")
        item.show()
        menu.append(item)
        item.connect('activate', self.show_message, data)

        # add quit item
        quit = gtk.MenuItem("Quit")
        quit.show()
        menu.append(quit)
        quit.connect('activate', gtk.main_quit)

        menu.popup(None, None, gtk.status_icon_position_menu, 
                   event_button, event_time, self.tray)

    def run(self):
        gtk.main()

if __name__ == "__main__":
    demo = StatusIconDemo("Hello, world!")
    demo.run()


