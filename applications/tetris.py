

import pyb
import os

def show_matrix(matrix, raw = False):
    res = [" "*(5*(len(matrix[0]))+1)]
    for y, line in enumerate(matrix):
        li = "%4d|" % y
        for x,c in enumerate(line):
            li += "%4d|" % c
        res.append(li)
    if not raw:
        res="\n".join(res)
    return res


class Stone:

    SHAPES = [
        [[0,0],[0,0]],  # Dummy shape 
        [[1, 1, 1],
         [0, 1, 0]],

        [[0, 2, 2],
         [2, 2, 0]],

        [[3, 3, 0],
         [0, 3, 3]],

        [[4, 0, 0],
         [4, 4, 4]],

        [[0, 0, 5],
         [5, 5, 5]],

        [[6, 6, 6, 6]],

        [[7, 7],
         [7, 7]]
    ]
    COLORS = ( (0,0,0), (1,0,0), (0,1,0), (0,0,1), (1,1,0), (0,1,1), (1,0,1), (1,1,1) )
    
    DEBUG = False
        
    def __init__(self, width , height, x=None, y=None, shape_nr = None):
        self.size = width , height
        self.shape_nr = shape_nr
        if not shape_nr:
            self.shape_nr = (pyb.rng()%(len(self.SHAPES)-1))+1
        self.shape = self.SHAPES[self.shape_nr]
        if x is None:
            x = pyb.rng()%(self.size[0]-len(self.shape[0]))
        if y is None:
            y = pyb.rng()%self.size[1]
        self.coord = x, y
        self.color = self.COLORS[self.shape_nr]
        self.last_coord = (0,0)
        
    def rotate(self, board):
        collide = False
        new_shape = [ [ self.shape[y][x] for y in range(len(self.shape)) ] for x in range(len(self.shape[0]) - 1, -1, -1) ]
        if self.check_collision(board, self.coord, new_shape):
            collide= True
        else:
            self.shape = new_shape
        return collide
    
    def move(self, direction, board):
        collide = False
        new_coord = list(c+d for c,d in zip(self.coord, direction))
        if new_coord[0]<0:
            new_coord[0] = 0
        if (new_coord[0]+ len(self.shape[0])>= self.size[0]):
            new_coord[0]=  self.size[0]- len(self.shape[0])
        if self.check_collision(board, new_coord, self.shape):
            collide= True
        else:
            self.last_coord = self.coord
            self.coord = new_coord
        return collide
    
    def draw(self, disp, color=None, coord=None):
        if color is None:
            color = self.color
        if coord is None:
            coord = self.coord
        for y, li in enumerate(self.shape):
            for x, p in enumerate(li):
                if p != 0:
                    disp.pixel((coord[0]+x, coord[1]+y), color)

    @staticmethod
    def shape2color(shape_nr):
        return Stone.COLORS[shape_nr]
    

    def check_collision(self, board, coord = None, shape=None):
        if not coord:
            coord = self.coord
        if not shape:
            shape =self.shape
        for y, line in enumerate(shape):
            for x, p in enumerate(line):
                pcoord=(coord[0]+x, coord[1]+y)
                #print(x,y,pcoord[0], pcoord[1], p)
                if not (0 <= pcoord[0] < self.size[0]) or not (0 <= pcoord[1] < self.size[1]):
                    if self.DEBUG:
                        print("Collision with edges (%2d, %2d)" % pcoord)
                    return True
                bp = board.pixel(coord=pcoord)
                if (p != 0)  and  (bp != 0):
                    if self.DEBUG:
                        print("Collision with backgroud (%2d, %2d) = %d and %d" % (pcoord[0], pcoord[1], p, bp))
                    return True
        return False
        
    def __str__(self):
        col = "(%d, %d, %d)" % self.color
        res = ["Shape with nr %d @ (%d, %d) col %s" % (self.shape_nr, self.coord[0], self.coord[1], col) ]
        res.extend(show_matrix(self.shape, True))
        return "\n".join(res)
        
        
class Board:
    
    DEBUG = False
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [ [ 0 for y in range(self.height)] for x in range(self.width) ]
        #self.board.extend([ 1 for x in range(self.height)])
        print("Board size %dx%d" % (len(self.board),len(self.board[0])))

    def add(self, shape):
        shape.draw(self, color=shape.shape_nr)
        
    def pixel(self, coord, color=None):
        if color is not None:
            if isinstance(color, (tuple,list)):
                raise ValueError("No tuple on board allowed", color)
            self.board[coord[0]][coord[1]] = color
        else:
            return self.board[coord[0]][coord[1]]
    
    def copy_line(self, from_y, to_y):
        if self.DEBUG:
            print("Copy line %d -> %d" % (from_y, to_y))
        for x in range(self.width):
            val = self.pixel((x,from_y)) if from_y>0 else 0
            self.pixel((x,to_y), val)

    def remove_full_line(self):
        full_lines = []
        for y in range(self.height-1, -1, -1):
            line_full = True
            for x in range(self.width):
                if self.pixel((x,y)) == 0:
                    break
            else:
                full_lines.append(y)
        if self.DEBUG:
            print(full_lines)
        shift_cnt = 0
        if len(full_lines)>0:
            for y in range(self.height-1, -1, -1):
                from_y = y-shift_cnt
                while from_y in full_lines:
                    shift_cnt+=1
                    from_y = y-shift_cnt
                if shift_cnt > 0:
                    self.copy_line(from_y, y)
        return len(full_lines)>0

    def to_term(self):
        res = []
        print("   |"+"|".join(( " %2d" % i for i in range(self.width))))
        print("-"+("-"*(4*self.width+3)))
        for y in range(self.height):
            l="%2d |" % y
            for x in range(self.width):
                val = self.pixel((x,y))
                l += ("   |" if val == 0 else " %1d |" % val)
            print(l)
            print("-"+("-"*(4*self.width+3)))
        return 


class Tetris:
    
    UP, DOWN, LEFT, RIGHT = range(4)
    
    DEBUG = False
    
    def __init__(self, display, button, t_inc=100):
        self._display = display
        self._button = button
        self._b_dir = ( (0,-1), (0,1), (-1,0), (1,0) )
        self._loc = self._display.width()/2, self._display.height()/2
        self._fg = (1,0,0)
        self._bg = (0,0,0)
        self._display.start()
        self._gameover = False
        self._board = None
        self._move_inc_time_ms = t_inc
        self._move_y_to_move_in_ration = 2
        self._rotation_to_move_in_ration = 2
     
    def redraw(self):
        if self.DEBUG:
            print("Redraw display")
        self._display.clear()
        for x in range(self._display.width()):
            for y in range(self._display.height()):
                color = Stone.shape2color(self._board.pixel((x,y)))
                self._display.pixel((x,y), color)
    
    
    def run_game(self):
        self._gameover = False
        self._board = Board(self._display.width(), self._display.height() )
        keys = [0 for i in range(len(self._button)+1)] # last element is count of scans
        while not self._gameover:
            stone = Stone(self._display.width(), self._display.height(), y=0)
            if stone.check_collision(self._board):
                # Game is finished when a new introduced stone collides with 
                # a stone on the board.
                self._gameover = True
            collide_y  = False
            stone.draw(self._display)
            pyb.delay(100)
            for i in range(len(keys)):
                keys[i] = 0
            free_fall = False
            move_y_cnt=0
            roatation_cnt=0
            next_move_time = pyb.millis()+self._move_inc_time_ms
            while not ( collide_y or self._gameover):
                if pyb.millis()>next_move_time:
                    stone.draw(self._display, self._bg)
                    #
                    # Y moves
                    #
                    move_y_cnt = (move_y_cnt+1)%self._move_y_to_move_in_ration
                    if move_y_cnt == 0:
                        if free_fall:
                            while not collide_y:
                                collide_y = stone.move(self._b_dir[Tetris.DOWN], self._board)
                        else:
                            collide_y = stone.move(self._b_dir[Tetris.DOWN], self._board)
                        if collide_y: 
                            break
                    #
                    # Rotations
                    #
                    roatation_cnt = (roatation_cnt+1)%self._rotation_to_move_in_ration
                    if roatation_cnt == 0:
                        if keys[self.UP] >= keys[-1]>>1:
                            stone.rotate(self._board)
                    #
                    # X moves 
                    #
                    direction = (0, 0)
                    for d in (self.LEFT, self.RIGHT):
                        if keys[d] >= keys[-1]>>1:
                            direction = (self._b_dir[d][0], direction[1])
                            break
                    collide_x = stone.move(direction, self._board)
                    stone.draw(self._display)
                    #
                    # Free free_fall
                    #
                    if keys[self.DOWN] >= keys[-1]>>1: 
                        free_fall = True
                        if self.DEBUG:
                            print("Set free fall %d/%d" % (keys[self.DOWN], keys[-1]))
                    #
                    # Cleanup prepare next move update
                    #
                    for i in range(len(keys)):
                        keys[i] = 0
                    next_move_time = pyb.millis()+self._move_inc_time_ms
                else:
                    # Capture Keys
                    for i, key in enumerate(self._button):
                        keys[i] += 1 if key.value()==0 else 0
                    keys[-1] += 1
                    pyb.delay(10)
            if collide_y:
                stone.draw(self._display)
                self._board.add(stone)
                if self._board.remove_full_line():
                    self.redraw()
        
    def run(self, t_inc=100):
        self._move_inc_time_ms = t_inc
        while True:
            self.wait_for_button_press()
            self.run_game()
    
    def wait_for_button_press(self):
        self._display.clear()
        self._display.text("Push", (0,0),(1,0,0))
        self._display.text("key", (4,8),(1,0,0))
        self._display.text("to", (8,16),(1,0,0))
        self._display.text("s", (-1,24),(1,0,0))
        self._display.text("t", (6,24),(1,0,0))
        self._display.text("a", (12,24),(1,0,0))
        self._display.text("r", (19,24),(1,0,0))
        self._display.text("t", (26,24),(1,0,0))
        wait_for_button = True
        while wait_for_button:
            pyb.delay(100)
            for b,d in zip(self._button, self._b_dir):
                if b.value()==0:
                    wait_for_button= False
        self._display.clear()
    
