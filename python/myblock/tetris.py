#/usr/bin/env python

import common
import random

class Tetris:
    """tetris class interface"""
    def __init__(self, myblock, *args):
        self.virtual = [ [0]*common.MAX_X for y in range(common.MAX_Y) ]
        self.blocks = 7
        self.gui = myblock
        self.line_score = [40,100,300,1200]
        self.block_frames = [1,2,2,2,4,4,4]
        self.block_data = [ 
                              [
                                  [(0,1,0,1),(0,0,1,1)]
                              ],
                              [
                                  [(0,1,1,2),(1,1,0,0)],
                                  [(0,0,1,1),(0,1,1,2)]
                              ],
                              [
                                  [(0,1,1,2),(0,0,1,1)],
                                  [(1,1,0,0),(0,1,1,2)]
                              ],
                              [
                                  [(1,1,1,1),(0,1,2,3)],
                                  [(0,1,2,3),(2,2,2,2)]
                              ],
                              [
                                  [(1,1,1,2),(2,1,0,0)],
                                  [(0,1,2,2),(1,1,1,2)],
                                  [(0,1,1,1),(2,2,1,0)],
                                  [(0,0,1,2),(0,1,1,1)]
                              ],
                              [
                                  [(0,1,1,1),(0,0,1,2)],
                                  [(0,1,2,2),(1,1,1,0)],
                                  [(1,1,1,2),(0,1,2,2)],
                                  [(0,0,1,2),(2,1,1,1)]
                              ],
                              [
                                  [(1,0,1,2),(0,1,1,1)],
                                  [(2,1,1,1),(1,0,1,2)],
                                  [(1,0,1,2),(2,1,1,1)],
                                  [(0,1,1,1),(1,0,1,2)]
                              ],
                          ]

    def game_init(self):
        #print "-----------Tetris Game Init-----------------------"
        common.game_over = False
        common.game_pause = False
        common.current_score = 0
        common.current_level = common.options["level"]
        common.current_lines = 0
        self.new_block()
        self.move_block(0,0,0)
        self.gui.update_game_values()

    def do_random(self, max):
        number = random.randint(0, max-1)
        #print number
        return number

    def new_block(self):
        #print "------------- New block-----------"
        common.current_block = common.next_block
        common.current_frame = common.next_frame
        common.next_block = self.do_random(self.blocks)
        common.next_frame = self.do_random(self.block_frames[common.next_block])
        common.current_x = int(common.MAX_X/2)-1
        #print "current_x = %d" %common.current_x
        common.current_y = 0
        
        valid = self.valid_position(common.current_x, common.current_y,
                                    common.current_block, common.current_frame)
        if not valid:
            common.game_over = True
            self.gui.game_over_init()
            return
            
        # Make the block start at top
        valid = self.valid_position(common.current_x, common.current_y - 2,
                                    common.current_block, common.current_frame)
                                    
        if valid:
            common.current_y -=2
        else:
            valid = self.valid_position(common.current_x, common.current_y - 1,
                                        common.current_block, common.current_frame)
            if valid:
                common.current_y -=1
 
        if common.options["shw_nxt"]:
            self.draw_block(0,0,common.current_block,common.current_frame,True,True)
            self.draw_block(0,0,common.next_block,common.next_frame,False,True)

    def valid_position(self, x, y, block, frame):
        for temp in range(4):
            row = y + self.block_data[block][frame][1][temp]
            col = x + self.block_data[block][frame][0][temp]
            if col not in range(common.MAX_X) or row not in range(common.MAX_Y) or self.virtual[row][col] != 0 :
                return False
                
        return True
            
    def draw_block(self, x, y, block, frame, clear, next):
        #print "draw_block"
        for temp in range(4):
            cols = x + self.block_data[block][frame][0][temp]
            rows = y + self.block_data[block][frame][1][temp]
            if clear:
                color_index = 0
            else:
                color_index = block+1
            self.set_block(cols, rows, color_index, next)

    def set_block(self,x,y,color,next):
        if next:
            area = common.next_block_area
        else:
            area = common.game_area
        style = area.get_style()
        area.window.draw_drawable(style.black_gc, common.blocks_pixmap,
                                  color*common.BLOCK_WIDTH,0,
                                  x*common.BLOCK_WIDTH,y*common.BLOCK_HEIGHT,
                                  common.BLOCK_WIDTH,common.BLOCK_HEIGHT)

    def move_block(self, x, y, f):
        #print "move_block"
        last_block = common.current_block
        last_frame = common.current_frame
        
        if f != 0:
            #print "upupupupup"
            frame = self.block_frames[common.current_block] + common.current_frame + f
            common.current_frame = frame%self.block_frames[common.current_block]
            
        valid = self.valid_position(common.current_x + x, common.current_y + y,
                                    common.current_block, common.current_frame)
        if valid:
            self.draw_block(common.current_x,common.current_y,last_block,last_frame,True,False)
            common.current_x += x
            common.current_y += y
            self.draw_block(common.current_x,common.current_y,
                            common.current_block, common.current_frame,False,False)
        else:
            common.current_block = last_block
            common.current_frame = last_frame


    def from_virtual(self):
        for y in range(common.MAX_Y):
            for x in range(common.MAX_X):
                self.set_block(x,y,self.virtual[y][x], False)

    def to_virtual(self):
        for temp in range(4):
            y = common.current_y+self.block_data[common.current_block][common.current_frame][1][temp]
            x = common.current_x+self.block_data[common.current_block][common.current_frame][0][temp]
            self.virtual[y][x] = common.current_block+1
        
    def move_down(self):
        #print "move down"
        valid = self.valid_position(common.current_x, common.current_y + 1,
                                    common.current_block, common.current_frame)

        if not valid:
            self.to_virtual()
            lines = self.check_lines()
            if lines > 0:
                self.from_virtual()
                common.current_lines += lines
                num = int(common.current_lines/10)
                if num > common.current_level:
                        common.current_level = int(common.current_lines/10)
                if common.current_level > 19:
                    common.current_level = 19
                common.current_score += self.line_score[lines-1]*(common.current_level+1)
                
            self.new_block()
            self.move_block(0,0,0)
            return False
        else:
            self.move_block(0,1,0)
            return True
        
    def check_lines(self):
        lines = 0
        for y in range(common.MAX_Y):
            line = True
            for x in range(common.MAX_X):
                if self.virtual[y][x] == 0 :
                    line = False
                
            if line:
                lines += 1
                for temp in range(y,0,-1):
                    self.virtual[temp] = self.virtual[temp-1]
                self.virtual[0] = [0]*common.MAX_X
                self.from_virtual()

        return lines


