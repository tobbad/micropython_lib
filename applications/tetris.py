

import pyb


class Stone:

    SHAPES = [
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
    COLORS = ( (1,0,0), (0,1,0), (0,0,1), (1,1,0), (0,1,1), (1,0,1), (1,1,1) )
        
    def __init__(self, width , height, x=None, y=None):
        self.size = width , height
        self.shape_nr = pyb.rng()%len(self.SHAPES)
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
        if not color:
            color = self.color
        if not coord:
            coord = self.coord
        for y, li in enumerate(self.shape):
            for x, p in enumerate(li):
                if p != 0:
                    disp.pixel((coord[0]+x, coord[1]+y), color)
    
    def check_collision(self, board, coord = None, shape=None):
        if not coord:
            coord = self.coord
        if not shape:
            shape =self.shape
        for y, line in enumerate(shape):
            for x, p in enumerate(line):
                coord=(coord[0]+x, coord[1]+y)
                if not (0 <= coord[0] < self.size[0]) or not (0 <= coord[1] < self.size[1]):
                    print("Collision with edges (%2d, %2d)" % coord)
                    return True
                bp = board.pixel(coord=coord)
                if p and bp:
                    print(p,bp)
                    print("Collision with backgroud (%2d, %2d) = %d and %d" % (coord[0], coord[1], p, bp))
                    return True
        return False
        
        
class Board:
    
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._board = [ [ 0 for x in range(self._width)] for y in range(self._height) ]
        #self._board.extend([ 1 for x in range(self._width)])
        print("Board size %dx%d" % (len(self._board),len(self._board[0])))

    def add(self, shape):
        shape.draw(self, color=shape.shape_nr)
        
    def pixel(self, coord, color=None):
        if color:
            if isinstance(color, (tuple,list)):
                raise ValueError("No tuble on board allowed")
            self._board[coord[0]][coord[1]] = color
        else:
            return self._board[coord[0]][coord[1]]


class Tetris:
    
    UP, DOWN, LEFT, RIGHT = 0,1,2,3
    
    def __init__(self, display, button):
        self._display = display
        self._button = button
        self._b_dir = ( (0,-1), (0,1), (-1,0), (1,0) )
        self._loc = self._display.width()/2, self._display.height()/2
        self._fg = (1,0,0)
        self._bg = (0,0,0)
        self._display.start()
        self._gameover = False
        self._board = None
        
    def run_game(self):
        self._gameover = False
        self._board = Board(self._display.width(), self._display.height() )
        while not self._gameover:
            stone = Stone(self._display.width(), self._display.height(), y=0)
            if stone.check_collision(self._board):
                # Game is finished when a new introduced stone collides with 
                # a stone on the board.
                self._gameover = True
            collide  = False
            while not ( collide or self._gameover):
                stone.draw(self._display)
                pyb.delay(100)
                stone.draw(self._display, self._bg)
                direction = self._b_dir[Tetris.DOWN]
                if self._button[self.UP].value() == 0:
                    collide = stone.rotate(self._board)
                for d in (self.LEFT, self.RIGHT):
                    if self._button[d].value() == 0:
                        direction = (self._b_dir[d][0], direction[1])
                        break
                collide |= stone.move(direction, self._board)
            if collide:
                stone.draw(self._display)
                self._board.add(stone)
        
    def run(self):
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
    
