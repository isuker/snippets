#/usr/bin/env python

import common
import tetris
import pygtk
pygtk.require('2.0')
import gtk
import gobject

class MyBlock:
    """This class covers main GUI"""
    def __init__(self):
        self.pause_str = ["Pause","Resume"]
        self.start_stop_str = ["Start Game","Stop game"]
        self.level_speeds = [1000,886,785,695,616,546,483,428,379,336,298,\
				             264,234,207,183,162,144,127,113,100]
        # init game values
        self.game_play = False
        #get_opt_file(option_f, 100)
        self.read_options()
        common.game_over, common.game_pause = True, False
        common.current_x, common.current_y = 0, 0
        common.current_block, common.current_frames = 0, 0
        common.current_score, common.current_lines = 0, 0
        common.current_level = common.options["level"]
        common.next_block, common.next_frame = 0, 0

    def update_game_values(self):
        self.score_label2.set_label(str(common.current_score))
        self.level_label2.set_label(str(common.current_level))
        self.line_label2.set_label(str(common.current_lines))
        
    def read_options(self):
        pass
        
    def keyboard_event_handler(self, widget, event, *args):
        #print "Key press event"
        if common.game_over or common.game_pause:
            return False

        dropbonus = 0
        key = event.keyval
        if key == ord('x') or key == ord('X'):
            self.gtkTetris.move_block(0,0,1)
            event.keyval = 0
            return True
        elif key == ord('w') or key == ord('W'):
            self.gtkTetris.move_block(0,0,-1)
            event.keyval = 0
            return True
        elif key == ord('s') or key == ord('S'):
            self.gtkTetris.move_down()
            event.keyval = 0
            self.update_game_values()
            return True
        elif key == ord('a') or key == ord('A'):
            self.gtkTetris.move_block(-1,0,0)
            event.keyval = 0
            return True
        elif key == ord('d') or key == ord('D'):
            self.gtkTetris.move_block(1,0,0)
            event.keyval = 0
            return True
        elif key == ord(' '):
            while (self.gtkTetris.move_down()):
                dropbonus += 1
            common.current_score += dropbonus*(common.current_level+1)
            self.update_game_values()
            event.keyval = 0
            return True
            
        return False

    def game_start_stop(self, menu_item, *args):
        #print "activate Start Game Menu" 
        self.game_play = not self.game_play
        menu_item.set_sensitive(False)
        if self.game_play:
            self.menu_game_stop.set_sensitive(True)
            self.menu_game_quick.set_sensitive(False)
            self.menu_game_start.set_sensitive(False)
            self.Start_stop_button.set_sensitive(True)
            self.Start_stop_button_label.set_label(self.start_stop_str[1])
            self.Pause_button.set_sensitive(True)
            self.Pause_button.grab_default()
            # New Tetris.....Game init.....
            self.gtkTetris = tetris.Tetris(self)
            self.gtkTetris.game_init()
            #gtkTetris.make_noise()
            self.gtkTetris.from_virtual()
            self.gtkTetris.move_block(0,0,0)
            common.current_level = common.options["level"]
            self.update_game_values()
            self.timer = gobject.timeout_add(self.level_speeds[common.current_level],self.game_loop)
        else:
            #print self.game_play
            self.game_over_init()

    def game_over_init(self):
        common.game_over = True
        self.game_play = False
        style = common.game_area.get_style()
        rectangle = common.game_area.get_allocation()
        common.game_area.window.draw_rectangle(style.black_gc,True,0,0,
                                                rectangle.width,rectangle.height)

        style = common.next_block_area.get_style()
        rectangle = common.next_block_area.get_allocation()
        common.next_block_area.window.draw_rectangle(style.black_gc,True,0,0,
                                                    rectangle.width,rectangle.height)

        self.Pause_button.clicked()
        self.Start_stop_button_label.set_label(self.start_stop_str[0])
        self.menu_game_quick.set_sensitive(True)
        self.menu_game_start.set_sensitive(True)
        self.menu_game_stop.set_sensitive(False)
        self.Start_stop_button.set_sensitive(True)
        self.Start_stop_button.grab_default()
        self.Pause_button_label.set_label(self.pause_str[0])
        self.Pause_button.set_sensitive(False)
        
        gobject.source_remove(self.timer)

    def game_loop(self):
        #print "-----------------Game Loop----------------------"
        if not common.game_over:
            self.timer = gobject.timeout_add(self.level_speeds[common.current_level],self.game_loop)
            self.gtkTetris.move_down()
            
        return False

    def game_set_pause(self, *args):
        #print "activate Pause Menu" 
        if common.game_over:
            self.menu_game_pause.set_active(False)
            return
        
        common.game_pause = not common.game_pause
        if common.game_pause:
            gobject.source_remove(self.timer)
            self.Pause_button_label.set_label(self.pause_str[1])
        else:
            self.timer = gobject.timeout_add(self.level_speeds[common.current_level],self.game_loop)
            self.Pause_button_label.set_label(self.pause_str[0])

    def show_new_game(self, *args):
        print "show_new_game" 

    def game_show_next_block(self, *args):
        #print "game_show_next_block"
        common.options["shw_nxt"] = not common.options["shw_nxt"]
        if not common.game_over:
            if not common.options["shw_nxt"]:
                self.gtkTetris.draw_block(0,0,common.next_block,common.next_frame,True,True)
            else:
                self.gtkTetris.draw_block(0,0,common.next_block,common.next_frame,False,True)

    def save_options(self, *args):
        print "save_options"

    def show_help(self, *args):
        print "show_help" 

    def show_highscore_wrapper(self, *args):
        print "show_highscore_wrapper" 

    def show_about(self, *args):
        print "show_about"

    def game_area_expose_event(self, *args):
        #print "game_area_expose_event"
        if not common.game_over:
            self.gtkTetris.from_virtual()
            self.gtkTetris.move_block(0,0,0)
        else:
            style = common.game_area.get_style()
            rectangle = common.game_area.get_allocation()
            common.game_area.window.draw_rectangle(style.black_gc,True,0,0,
                                                   rectangle.width,rectangle.height)

        return False

    def next_block_area_expose_event(self, *args):
        #print "next_block_area_expose_event"
        style = common.next_block_area.get_style()
        rectangle = common.next_block_area.get_allocation()
        common.next_block_area.window.draw_rectangle(style.black_gc, True,0,0,
                                                   rectangle.width,rectangle.height)
        if (not common.game_over and common.options["shw_nxt"]):
            self.gtkTetris.draw_block(0,0,common.next_block,common.next_frame,False,True)

        return False

    def game_set_pause_b(self, *args):
        if common.game_pause:
            self.menu_game_pause.set_active(False)
        else:
            self.menu_game_pause.set_active(True)

    def label_box(self, parent, label, text):
        # create box for label
        box1 = gtk.HBox(False, 0)
        box1.set_border_width(2)
        # get style of button
        style = parent.get_style()
        
        # create label for button
        label.set_text(text)
        
        box1.pack_start(label, True, True, 3)
        label.show()
        
        return box1
        
    def set_gtk_color_style(self, widget, red, green, blue):
        style = gtk.Style()
        colormap = gtk.gdk.colormap_get_system()
        #print colormap
        color = colormap.alloc_color(red,green,blue,writeable=True)
        widget.modify_fg(gtk.STATE_NORMAL, color)
        widget.set_style(style)
        
    def main(self):
        #print "------------------Main-------------------------"
        accel_group = gtk.AccelGroup()
        # Main Window
        main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        main_window.set_resizable(False)
        main_window.set_title("GTK Tetris")
        main_window.connect("key-press-event", self.keyboard_event_handler)
        main_window.connect("destroy", gtk.main_quit)
        
        # vertical box
        v_box = gtk.VBox(False, 0)
        main_window.add(v_box)
        v_box.show()
        
        # menu stuff
        menu_bar = gtk.MenuBar()
        menu_bar.show()
        v_box.pack_start(menu_bar, False, False, 0)
        
        # Game sub-menu
        menu_game = gtk.MenuItem("_Game", True)
        menu_game.show()
        menu_bar.add(menu_game)
        
        menu_game_menu = gtk.Menu()
        menu_game.set_submenu(menu_game_menu)
        
        self.menu_game_quick = gtk.MenuItem("Start Game", True)
        self.menu_game_quick.show()
        menu_game_menu.add(self.menu_game_quick)
        self.menu_game_quick.connect("activate", self.game_start_stop)
        self.menu_game_quick.add_accelerator("activate", accel_group,
                                        ord('G'), gtk.gdk.CONTROL_MASK,
                                        gtk.ACCEL_VISIBLE)

        self.menu_game_stop = gtk.MenuItem("Stop Game", True)
        self.menu_game_stop.show()
        menu_game_menu.add(self.menu_game_stop)
        self.menu_game_stop.connect("activate", self.game_start_stop)
        self.menu_game_stop.add_accelerator("activate", accel_group,
                                        ord('O'), gtk.gdk.CONTROL_MASK,
                                        gtk.ACCEL_VISIBLE)
        self.menu_game_stop.set_sensitive(False)

        self.menu_game_pause = gtk.CheckMenuItem("Pause", True)
        self.menu_game_pause.show()
        menu_game_menu.add(self.menu_game_pause)
        self.menu_game_pause.connect("activate", self.game_set_pause)
        self.menu_game_pause.add_accelerator("activate", accel_group,
                                        ord('P'), gtk.gdk.CONTROL_MASK,
                                        gtk.ACCEL_VISIBLE)

        separatormenuitem1 = gtk.MenuItem()
        separatormenuitem1.show()
        menu_game_menu.add(separatormenuitem1)
        separatormenuitem1.set_sensitive(False)
        
        self.menu_game_quit = gtk.MenuItem("Quit", True)
        self.menu_game_quit.show()
        menu_game_menu.add(self.menu_game_quit)
        self.menu_game_quit.connect("activate", gtk.main_quit)
        self.menu_game_quit.add_accelerator("activate", accel_group,
                                        ord('X'), gtk.gdk.CONTROL_MASK,
                                        gtk.ACCEL_VISIBLE)        
        
        # Settings sub-menu
        menu_settings = gtk.MenuItem("_Settings", True)
        menu_settings.show()
        menu_bar.add(menu_settings)
        
        menu_settings_menu = gtk.Menu()
        menu_settings.set_submenu(menu_settings_menu)
        
        self.menu_game_start = gtk.MenuItem("Level Settings", True)
        self.menu_game_start.show()
        menu_settings_menu.add(self.menu_game_start)
        self.menu_game_start.connect("activate", self.show_new_game)

        self.menu_game_show_next_block = gtk.CheckMenuItem("Show next block", True)
        self.menu_game_show_next_block.show()
        menu_settings_menu.add(self.menu_game_show_next_block)
        self.menu_game_show_next_block.connect("activate", self.game_show_next_block)
        if common.options["shw_nxt"]:
            self.menu_game_show_next_block.set_active(True)
        self.menu_game_show_next_block.add_accelerator("activate", accel_group,
                                        ord('N'), gtk.gdk.CONTROL_MASK,
                                        gtk.ACCEL_VISIBLE)        

        separator1 = gtk.MenuItem()
        separator1.show()
        menu_settings_menu.add(separator1)
        separator1.set_sensitive(False)
        
        self.menu_save_options = gtk.MenuItem("Save Settings", True)
        self.menu_save_options.show()
        menu_settings_menu.add(self.menu_save_options)
        self.menu_save_options.connect("activate", self.save_options)

        # Help sub-menu
        menu_help = gtk.MenuItem("_Help", True)
        menu_help.show()
        menu_bar.add(menu_help)
        menu_help.set_right_justified(True)
        
        menu_help_menu = gtk.Menu()
        menu_help.set_submenu(menu_help_menu)
        
        help1 = gtk.MenuItem("Help", True)
        help1.show()
        menu_help_menu.add(help1)
        help1.connect("activate", self.show_help)
        # How to set F1 shortcut????????????????????????//
        help1.add_accelerator("activate", accel_group,
                                ord('H'), gtk.gdk.CONTROL_MASK,
                                gtk.ACCEL_VISIBLE)

        high_scores1 = gtk.MenuItem("High-scores", True)
        high_scores1.show()
        menu_help_menu.add(high_scores1)
        high_scores1.connect("activate", self.show_highscore_wrapper)

        separator2 = gtk.MenuItem()
        separator2.show()
        menu_help_menu.add(separator2)
        separator2.set_sensitive(False)
        
        about1 = gtk.MenuItem("About", True)
        about1.show()
        menu_help_menu.add(about1)
        about1.connect("activate", self.show_about)
        
        # horizontal box
        h_box = gtk.HBox(False, 1)
        h_box.show()
        v_box.pack_start(h_box, False, False, 0)
        
        # game_border
        game_border = gtk.Frame()
        game_border.set_shadow_type(gtk.SHADOW_IN)
        h_box.pack_start(game_border, False, False, 1)
        game_border.show()
        
        # Global game_area
        common.game_area = gtk.DrawingArea()
        common.game_area.show()
        common.game_area.set_size_request(common.MAX_X*common.BLOCK_WIDTH,
                                          common.MAX_Y*common.BLOCK_HEIGHT)
        common.game_area.connect("expose_event", self.game_area_expose_event)
        common.game_area.set_events(gtk.gdk.EXPOSURE_MASK)
        game_border.add(common.game_area)
        
        # right side
        right_side = gtk.VBox(False, 0)
        h_box.pack_start(right_side, False, False, 0)
        right_side.show()
        
        # next_block_border
        next_block_border = gtk.Frame()
        next_block_border.set_shadow_type(gtk.SHADOW_IN)
        right_side.pack_start(next_block_border, False, False, 0)
        next_block_border.show()
        # Global next block area
        common.next_block_area = gtk.DrawingArea()
        common.next_block_area.show()
        common.next_block_area.set_size_request(4*common.BLOCK_WIDTH,
                                                4*common.BLOCK_HEIGHT)
        common.next_block_area.connect("expose_event", self.next_block_area_expose_event)
        common.next_block_area.set_events(gtk.gdk.EXPOSURE_MASK)
        next_block_border.add(common.next_block_area) 
        
        # the score, level, lines
        self.score_label1 = gtk.Label("Score:")
        self.score_label1.set_justify(gtk.JUSTIFY_RIGHT)
        self.score_label1.show()
        right_side.pack_start(self.score_label1, False, False, 3)
        
        self.score_label2 = gtk.Label("0")
        self.set_gtk_color_style(self.score_label2, 0xffff, 0, 0)
        self.score_label2.set_justify(gtk.JUSTIFY_RIGHT)
        self.score_label2.show()
        right_side.pack_start(self.score_label2, False, False, 3)
        
        self.level_label1 = gtk.Label("Level:")
        self.level_label1.set_justify(gtk.JUSTIFY_RIGHT)
        self.level_label1.show()
        right_side.pack_start(self.level_label1, False, False, 3)
        
        dummy = str(common.current_level)
        
        self.level_label2 = gtk.Label(dummy)
          # ???????????????????????????????????????????????????
        self.set_gtk_color_style(self.level_label2, 0,0,0)
          #??????????????????????????????????????????
        self.level_label2.set_justify(gtk.JUSTIFY_RIGHT)
        self.level_label2.show()
        right_side.pack_start(self.level_label2, False, False, 3)

        self.line_label1 = gtk.Label("Lines:")
        self.line_label1.set_justify(gtk.JUSTIFY_RIGHT)
        self.line_label1.show()
        right_side.pack_start(self.line_label1, False, False, 3)
        
        self.line_label2 = gtk.Label("0")
        self.line_label2.set_justify(gtk.JUSTIFY_RIGHT)
        self.line_label2.show()
        right_side.pack_start(self.line_label2, False, False, 3)
        
        # the game buttons
        
        # Start_stop
        self.Start_stop_button = gtk.Button()
        self.Start_stop_button.show()
        self.Start_stop_button.connect("clicked", self.game_start_stop)
        self.Start_stop_button_label = gtk.Label(self.start_stop_str[0])
        box2 = self.label_box(right_side, self.Start_stop_button_label,
                              self.start_stop_str[0])
        box2.show()
        self.Start_stop_button.add(box2)
        right_side.pack_start(self.Start_stop_button, False, False, 3)
        self.Start_stop_button.set_flags(gtk.CAN_DEFAULT)
        self.Start_stop_button.grab_default()
        
        # Pause
        self.Pause_button = gtk.Button()
        self.Pause_button.show()
        self.Pause_button.connect("clicked", self.game_set_pause_b)
        self.Pause_button_label = gtk.Label(self.pause_str[0])
        box1 = self.label_box(right_side, self.Pause_button_label, 
                              self.pause_str[0])
        box1.show()
        self.Pause_button.add(box1)
        right_side.pack_start(self.Pause_button, False, False, 3)
        self.Pause_button.set_flags(gtk.CAN_DEFAULT)
        self.Pause_button.set_sensitive(False)
        
        main_window.add_accel_group(accel_group)
        main_window.show()
        
        # Block pixmap
        common.blocks_pixmap,mask = gtk.gdk.pixmap_create_from_xpm_d(common.game_area.window,
                                                                     None, common.blocks_xpm)
        
        gtk.main()

if __name__ == "__main__":
    myBlock = MyBlock()
    myBlock.main()

















