#!/usr/bin/python

import gtk
import egg.trayicon

applet = egg.trayicon.TrayIcon("HelloApplet")
applet.add(gtk.Label("Hello"))
applet.show_all()
gtk.main()

