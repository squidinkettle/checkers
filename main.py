import pygame, sys
from pygame.locals import *
from pygame import *
import random
import time

pygame.init()
#L4149

# ======= Game Window
board = pygame.image.load('checkerboard.jpg')
size = board.get_rect().size

width = size[0] + 50
height = size[1]
GAME_WINDOW = pygame.display.set_mode((width, height))
pygame.display.set_caption('Checkers')
mousey = 0
mousex = 0


FPSCLOCK = pygame.time.Clock()
FPS = 30

# ===Colors
RED = (255, 0, 0)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

rectangle1 = pygame.draw.rect(GAME_WINDOW, GRAY, (0, 650, 1160, 250))
GAME_WINDOW.fill(BLACK)
alphaSurface = Surface((width, height))
alphaSurface.fill(BLACK)
alphaSurface.set_alpha(255)

#Controls
def for_event():
    global mousex, mousey
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_x:
                pygame.quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mousex, mousey = pygame.mouse.get_pos()


def player_pieces(black, red):
    player1=black
    player2=red
    return player1, player2

class Checkers(object):
    def __init__(self,team,pos):
        self.color = team
        self.pos = (pos[0]+10,pos[1]+10)
        self.movement =1
        self.combo = False
        self.scan = []
        self.queened = False
        self.captured = False
        self.rect = pygame.image.load("%s.png" % (team,))
        self.jumped = False
        self.rect_size =self.rect.get_rect().size
        self.rect_pos = pygame.Rect(pos[0],pos[1],self.rect_size[0],self.rect_size[1])
        self.target = []

    #checks if it can move diagonally
    def radius(self):
        grid = table_grid()

        self.mouvable_pos = []
        if self.color == 'Black' or self.queened == True:
            grid_pos =0
            for x in grid:
                if x.topleft == self.rect_pos.topleft:
                    og_grid_pos =grid_pos
                    grid_pos+=7
                    if grid_pos <=len(grid):
                        self.mouvable_pos.append(grid[grid_pos])
                    grid_pos=og_grid_pos

                    grid_pos-=9
                    if grid_pos >= 0:
                        self.mouvable_pos.append(grid[grid_pos])

                grid_pos+=1
        if self.color == 'Red' or self.queened == True:
            grid_pos = 0
            for x in grid:
                if x.topleft == self.rect_pos.topleft:
                    og_grid_pos = grid_pos
                    grid_pos -= 7
                    if grid_pos >=0:
                        self.mouvable_pos.append(grid[grid_pos])
                    grid_pos = og_grid_pos
                    grid_pos += 9
                    if grid_pos < len(grid):
                        self.mouvable_pos.append(grid[grid_pos])

                grid_pos += 1
        positions = self.mouvable_pos
        return positions

    #checks where it cant move
    def antiRadius(self,pieces):
        positions = self.check_for_other(pieces)
        grid = table_grid()
        self.notmouvable_pos = []
        if positions == []:
            for y in grid:
                self.notmouvable_pos.append(y)
        else:
            for x in grid:
                for y in positions:
                    if x.topleft != y.topleft:
                        self.notmouvable_pos.append(x)
        result = self.notmouvable_pos
        return result

    #Checks for pieces diagonal to targeted piece, returns possible movement
    def check_for_other(self,pieces):
        grid=table_grid()
        possible_positions = self.radius()
        new_pos = []
        right_side = False
        left_side = False
        self.target = []
        for y in pieces:
            for z in possible_positions:
                if z.topleft == y.rect_pos.topleft:
                    possible_positions.remove(z)
                    if y.color != self.color:
                        self.target.append(y)

                        if self.color == 'Black' or self.queened == True:
                            grid_pos = 0
                            for x in grid:
                                if x.topleft == self.rect_pos.topleft:
                                    OGgrid = grid_pos
                                    grid_pos+=14
                                    for o in pieces:
                                        if grid_pos< len(grid) and o.rect_pos.topleft == grid[grid_pos].topleft:
                                            right_side = False
                                            break
                                        else:
                                            right_side = True
                                    if grid_pos<=len(grid) and right_side == True:
                                        new_pos.append(grid[grid_pos])
                                    grid_pos=OGgrid
                                    grid_pos -=18
                                    for o in pieces:
                                        if grid_pos>= 0 and o.rect_pos.topleft == grid[grid_pos].topleft:
                                            left_side = False
                                            break
                                        else:
                                            left_side =True
                                    if grid_pos>=0 and left_side == True:
                                        new_pos.append(grid[grid_pos])

                                else:
                                    grid_pos +=1
                        if self.color == 'Red' or self.queened == True:
                            grid_pos = 0
                            for x in grid:
                                if x.topleft == self.rect_pos.topleft:
                                    OGgrid = grid_pos
                                    grid_pos -= 14
                                    for o in pieces:
                                        if grid_pos >=0 and o.rect_pos.topleft == grid[grid_pos].topleft:
                                            right_side = False
                                            break
                                        else:
                                            right_side = True
                                    if grid_pos >=0 and right_side == True:
                                        new_pos.append(grid[grid_pos])
                                    grid_pos = OGgrid
                                    grid_pos += 18
                                    for o in pieces:
                                        if grid_pos<len(grid) and o.rect_pos.topleft == grid[grid_pos].topleft:
                                            left_side = False
                                            break
                                        else:
                                            left_side = True
                                    if grid_pos <len(grid) and left_side == True:
                                        new_pos.append(grid[grid_pos])

                                else:
                                    grid_pos += 1








        for i in new_pos:
             possible_positions.append(i)


        return possible_positions

    #updates position
    def update(self,new_pos):

        self.rect_pos =pygame.Rect(new_pos[0],new_pos[1],self.rect_size[0],self.rect_size[1])
        self.pos = (new_pos[0]+10,new_pos[1]+10)

    #checks if it can capture a piece
    def capture_piece(self):
        global player1_turn, player2_turn
        possible_targets = self.target
        grid = table_grid()

        if self.color == 'Black' or self.queened == True:
            grid_pos = 0
            for x in grid:
                if x.topleft == self.rect_pos.topleft:
                    OGgrid = grid_pos
                    grid_pos +=9
                    for y in possible_targets:
                        if grid_pos < len (grid) and y.rect_pos.topleft == grid[grid_pos].topleft and self.jumped==True:
                            if player1 == True:
                                player1_turn = 1
                            else:
                                player2_turn = 1
                            y.captured = True
                            self.jumped=False
                    grid_pos = OGgrid
                    grid_pos -=7
                    for z in possible_targets:
                        if grid_pos >=0 and z.rect_pos.topleft == grid[grid_pos].topleft and self.jumped == True:
                            if player1 == True:
                                player1_turn = 1
                            else:
                                player2_turn = 1
                            z.captured = True
                            self.jumped = False
                grid_pos+=1
        if self.color == 'Red' or self.queened == True:
            grid_pos = 0
            for x in grid:
                if x.topleft == self.rect_pos.topleft:
                    OGgrid = grid_pos
                    grid_pos -=9
                    for y in possible_targets:
                        if grid_pos >=0  and y.rect_pos.topleft == grid[grid_pos].topleft and self.jumped == True:
                            if player1 == True:
                                player1_turn = 1
                            else:
                                player2_turn = 1
                            y.captured = True
                            self.jumped = False
                    grid_pos = OGgrid
                    grid_pos +=7
                    for z in possible_targets:
                        if grid_pos < len (grid) and z.rect_pos.topleft == grid[grid_pos].topleft and self.jumped == True:
                            if player1 == True:
                                player1_turn = 1
                            else:
                                player2_turn = 1
                            z.captured = True
                            self.jumped = False
                grid_pos+=1

    #checks if self.captured is true, if it is, it deletes from the piece list
    def check_if_captured(self,pieces):
        if self.captured == True:
            for x in pieces:
                if x == self:
                    pieces.remove(x)

        return pieces

    #checks if it has reached the opposite end of the board
    def check_if_crowned(self):
        grid = table_grid()
        if self.queened == False:
            black_zone = [x for x in grid [::8]]
            red_zone = [x for x in grid [7::8]]
            if self.color == 'Black':
                for x in black_zone:
                    if self.rect_pos.topleft == x.topleft:
                        self.queened = True
            else:
                for x in red_zone:
                    if self.rect_pos.topleft== x.topleft:
                        self.queened = True
        if self.queened == True:
            if self.color == 'Black':
                self.rect = pygame.image.load('queenedBlack.png')
            else:
                self.rect = pygame.image.load('queenedRed.png')

    def extra_turn(self):
        global player1
        self.movement += 1
        if self.movement >1:
            self.movement = 1


    def end_turn(self):
        global player1
        if self.movement == 0:
            if player1 == True:
                player1 = False
            else:
                player1 = True

def table_grid():
    global mousex,mousey
    height = 68
    width = 68
    added = 68
    base_horizontal = 28
    base_vertical = 27
    margin = 0
    square_pos = []
    yes = 0
    for column in range(51 + margin, 560, width + margin):
        yes += 1
        for row in range(27 + margin, 560, height + margin):
            if yes%2 == 0:
                square = pygame.draw.rect(GAME_WINDOW, RED, [column, row, width, height])
                square_pos.append(square)
            else:
                square = pygame.draw.rect(GAME_WINDOW, BLACK, [column, row, width, height])
                square_pos.append(square)
            yes += 1


    return square_pos

def setup_red():
    grid1 = table_grid()
    x1=1
    y1=2
    x2=8
    y2=11
    red_pos=[]
    for x in range(12):
        par = False
        if par ==False:
            for x in grid1[x1:y1:1]:
                red_pos.append(x.topleft)
            x1+=16
            y1+=16
            par = True
        if par == True:
            for x in grid1[x2:y2:2]:
                red_pos.append(x.topleft)
            x2+=16
            y2+=16
    return red_pos

def setup_black():
    grid1 = table_grid()
    x1=5
    y1=8
    x2=14
    y2=15
    black_pos=[]
    for x in range(12):
        par = False
        if par ==False:
            for x in grid1[x1:y1:2]:
                black_pos.append(x.topleft)
            x1+=16
            y1+=16
            par = True
        if par == True:
            for x in grid1[x2:y2:1]:
                black_pos.append(x.topleft)
            x2+=16
            y2+=16

    return black_pos

def selection(pieces):
    global mousex, mousey
    global player1
    global player1_turn
    global player2_turn

    grid = table_grid()
    result=None
    piece = None
    selected = False
    possible_movement=[]
    old_position = 0


    for x in pieces:
        if x.rect_pos.collidepoint(mousex,mousey):
            if player1 == True and x.color == 'Black':
                x.jumped = False
                piece = x
                OGposition = x.pos
                selected = True
                possible_movement = x.check_for_other(pieces)
                notpossible_movement = x.antiRadius(pieces)
                grid_pos = 0
                for y in grid:
                    if y.topleft == x.rect_pos.topleft:
                        old_position = grid_pos
                    grid_pos+=1
                grid_pos = old_position
            elif player1 == False and x.color == 'Red':
                x.jumped = False
                piece = x
                OGposition = x.pos
                selected = True
                possible_movement = x.check_for_other(pieces)
                notpossible_movement = x.antiRadius(pieces)
                grid_pos = 0
                for y in grid:
                    if y.topleft == x.rect_pos.topleft:
                        old_position = grid_pos
                    grid_pos += 1
                grid_pos = old_position
            else:
                selected = False
                piece = None
                mousey, mousex = (0, 0)

    events = pygame.event.get()
    while selected:



        mousey, mousex = (0, 0)
        for_event()

        pos = pygame.mouse.get_pos()
        piece.pos = (pos[0]-25,pos[1]-15)


        for z in possible_movement:
            if z.collidepoint(mousex,mousey):
                counting = 0

                for o in pieces:
                    if o == piece:
                        new_pos = (z.topleft[0]+10,z.topleft[1]+10)
                        piece.pos = new_pos
                        o.pos = z.topleft
                        o.update(z.topleft)
                        piece.update(z.topleft)
                        pieces[counting] = piece
                        if player1 ==True:
                            player1_turn = 0
                        else:
                            player2_turn = 0
                        for p in grid:

                            if piece.color == 'Black' or piece.queened == True:
                                OGgrid = grid_pos
                                grid_pos +=14
                                if grid_pos<=len(grid) and grid_pos>=0 and piece.rect_pos.topleft == grid[grid_pos].topleft:
                                    piece.jumped =True
                                grid_pos = OGgrid
                                grid_pos -=18
                                if grid_pos >=0 and piece.rect_pos.topleft ==grid[grid_pos].topleft:
                                    piece.jumped = True
                                grid_pos = OGgrid


                            if piece.color == 'Red' or piece.queened == True:
                                OGgrid = grid_pos
                                grid_pos -= 14
                                if grid_pos >=0 and piece.rect_pos.topleft == grid[grid_pos].topleft:
                                    piece.jumped = True
                                grid_pos = OGgrid
                                grid_pos += 18
                                if grid_pos< len(grid) and piece.rect_pos.topleft == grid[grid_pos].topleft:
                                    piece.jumped = True

                                grid_pos = OGgrid


                    counting+=1

                selected = False

                mousey,mousex = (0,0)
                return pieces
            else:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP and z.collidepoint(mousex, mousey) == 0:
                        if event.button == 1:
                            pass


        for y in notpossible_movement:
            if y.collidepoint(mousex,mousey):

                piece.pos= OGposition

                selected = False
                mousex,mousey = (0,0)
        table_grid()
        GAME_WINDOW.blit(piece.rect, piece.pos)
        for x in pieces:
            GAME_WINDOW.blit(x.rect, x.pos)
        pygame.display.update()


    return pieces


#shows all pieces in board
def display_pieces(red_pos,black_pos):

    list_red = []
    list_black = []
    for x in black_pos:
        blackP = Checkers('Black',x)
        list_black.append(blackP)

    for x in red_pos:
        redP = Checkers('Red',x)
        list_red.append(redP)

    return list_black, list_red


red_pos = setup_red()
black_pos = setup_black()

list_black, list_red = display_pieces(red_pos,black_pos)
all_pieces = list_red + list_black
player1_turn = 0
player2_turn =0
player1 = True
#Main Loop
while True:
    global mousex, mousey
    global player1
    GAME_WINDOW.blit(board, (25, 0))

    for_event()


    if player1 == True:
        player1_turn +=1
        if player1_turn>1:
            player1_turn = 1
        all_pieces = selection(all_pieces)
        temp_allpieces = all_pieces
        for y in temp_allpieces:
            y.capture_piece()
            all_pieces = y.check_if_captured(all_pieces)
            y.check_if_crowned()

        if player1_turn == 0:
            player1=False



    if player1 == False:
        player2_turn+=1
        if player2_turn >1:
            player2_turn = 1
        all_pieces = selection(all_pieces)
        temp_allpieces = all_pieces
        for y in temp_allpieces:
            y.capture_piece()
            all_pieces = y.check_if_captured(all_pieces)
            y.check_if_crowned()
        if player2_turn == 0:
            player1=True




    for x in all_pieces:
        GAME_WINDOW.blit(x.rect, x.pos)

    pygame.display.update()
    FPSCLOCK.tick(FPS)


#make the extra jumping turn
#make player 1 player 2 turn