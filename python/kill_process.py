#!/usr/bin/env python

# Kill Process GUI TOOL
# Author : Ray Chen
# Date : 2007-12-15

import os,sys
import gtk
import pygtk
import gobject

FILE_NAME = "/home/ray/.entry_history"

class KillProcess:
    """Kill running process"""
    
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_border_width(20)
        self.window.set_title("Kill Process")
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.table = gtk.Table(rows=3, columns=2, homogeneous=False)
        self.window.add(self.table)
        self.draw_gui()
        self.fill_table(self.table)
        # set default widget
        self.window.set_default(self.button_ok)
        self.window.set_resizable(False)
        self.window.show()
        # set entry completion
        self.init_completion(FILE_NAME)
        
        # Connect signals
        self.window.connect("destroy", gtk.main_quit)
        self.button_sigkill.connect("clicked", self.button_clicked, 'kill')
        self.button_sigterm.connect("clicked", self.button_clicked, 'term')
        self.button_canel.connect("clicked", gtk.main_quit)
        self.button_ok.connect("clicked", self.button_ok_clicked)
        
        # Set private variables
        self.process, self.signal = "", "SIGKILL"
        
    def fill_table(self, table):
        self.table.attach(self.label_process,0,1,0,1)
        self.table.attach(self.entry_process,1,2,0,1)
        self.table.attach(self.button_sigkill,0,1,1,2)
        self.table.attach(self.button_sigterm ,1,2,1,2)
        self.table.attach(self.button_canel,0,1,2,3)
        self.table.attach(self.button_ok,1,2,2,3)
        self.table.show()
        
    def draw_gui(self):
        self.label_process = gtk.Label("Process Name(ID) :  ")
        self.label_process.show()
        self.entry_process = gtk.Entry()
        self.entry_process.set_activates_default(True)
        self.entry_process.show()
        self.button_sigkill = gtk.RadioButton(None, "SIGKILL")
        self.button_sigkill.set_active(True)
        self.button_sigkill.show()
        self.button_sigterm = gtk.RadioButton(self.button_sigkill, "SIGTERM")
        self.button_sigterm.show()
        self.button_canel = gtk.Button("Quit")
        self.button_canel.show()
        self.button_ok = gtk.Button("Kill")
        self.button_ok.set_flags(gtk.CAN_DEFAULT)
        self.button_ok.show()
        
    def init_completion(self, file_open=""):
        self.completion = gtk.EntryCompletion()
        self.entry_process.set_completion(self.completion)

        # Create a tree model and use it as the completion model        
        self.completion_model = self.create_completion_model(file_open)
        self.completion.set_model(self.completion_model)

        # Use model column 0 as the text column
        self.completion.set_text_column(0)
        
    def create_completion_model(self, file_open=""):
        try:
            #path = os.getcwd()
            #full_name = os.path.join(path, file_open)
            full_name = file_open
            file_entry_history = open(full_name)
        except:
            print "Can't open %s" %full_name
            sys.exit(1)
            
        # list store
        store = gtk.ListStore(gobject.TYPE_STRING)
            
        for line in file_entry_history.readlines():
            word = line.strip('\n')
            # append words
            iter = store.append()
            store.set(iter, 0, word)
            
        return store
        
    def save_entry_text(self, word, file_save=""):
        if file_save == "":
            return
            
        #path = os.getcwd()
        #full_name = os.path.join(path, file_save)
        full_name = file_save
        file = open(full_name, 'a+')
        # if an inserted word already exists in entry history, 
        # just skip, don't save
        inserted_str = word + '\n'
        if not inserted_str in file.readlines():
            file.write(inserted_str)
        
        return 

    def button_clicked(self, widget, data=None):
        if data == 'kill':
            self.signal = "SIGKILL"

        if data == 'term':
            self.signal = "SIGTERM"

    def button_ok_clicked(self, *args):
        self.process = self.entry_process.get_text()
        if self.process != "":
            # set command
            if self.process.isdigit():
                command = "kill"
            else:
                self.save_entry_text(self.process,FILE_NAME)
                command = "killall"
                
            self.command = "%s -%s %s" %(command,self.signal,self.process)
            os.system(self.command)

    def main(self):
        gtk.main()
        

if __name__ == "__main__":
    example = KillProcess()
    example.main()
