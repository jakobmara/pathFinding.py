import pygame as pg
from node import Node
from board import Board
import math
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BOARD_SIZE = (1024, 1024)
SCREEN_SIZE= (1224,1024)
YELLOW = (255,255,0)
GRAY = (105,105,105)

def main():
    is_placing_spawn = False
    is_placing_dest = False

    screen = pg.display.set_mode(BOARD_SIZE)
    pg.display.set_caption("Pathfinding Visualization")
    clock = pg.time.Clock()
    startCoords = [None,None]
    destCoords = [None,None]
    inGame = False
    pg.init()
    myBoard = Board(screen)

    myBoard.createIntro()
    pg.display.flip()
    inMenu = True

    while inMenu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                inMenu = False
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if pos[0] >= 378 and pos[0] <=378 + 269:
                    if pos[1] >= 583 and pos[1] <= 583+34:
                        inGame = True
                        inMenu = False
    screen = pg.display.set_mode(SCREEN_SIZE)
    myBoard.createBoard()
    myBoard.createControls()
    pg.display.flip()
    clicked = False
    while inGame:
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                inGame = False
            
            # These 2 if statements are used to see if user is holding down on button
            if event.type == pg.MOUSEBUTTONDOWN:
                clicked = True
            
            if event.type == pg.MOUSEBUTTONUP:
                clicked = False
            
            # if user is holding down on button
            if clicked:
                pos = pg.mouse.get_pos()
                
                if pos[0] <= 1024:
                    
                    # they are in format: y, x (row, col)
                    gridCoord =[pos[1]//32,pos[0]//32]
                    if is_placing_spawn:
                        print(f"placing spawn12")
                        myBoard.updateBoard(gridCoord,RED)
                        startCoords = gridCoord #this could proll be in a class so that i wouldn't have to use as many global
                        is_placing_spawn = False
                    elif is_placing_dest:
                        myBoard.updateBoard(gridCoord,GREEN)
                        is_placing_dest = False
                        destCoords = gridCoord

                    else:
                        myBoard.updateBoard(gridCoord,GRAY)
                    pg.display.flip()
                
                elif rect_pressed(myBoard.spawnRect,pos):
                    is_placing_spawn = True
                    print("Start")
                
                elif rect_pressed(myBoard.destRect,pos):
                    is_placing_dest = True
                    print("Dest")

                elif rect_pressed(myBoard.visRect,pos):
                    print(f"visualizing...")
                    #need to make sure both are pressed before this works maybe use tkinter to alert?
                    final_node, other = visualize_path(myBoard.board_matrix,startCoords,destCoords)
                    path = construct_path(final_node)
                    myBoard.drawPath(pg,path,other)

                elif rect_pressed(myBoard.resetRect,pos):
                    print(f"resetting...")
                    myBoard.createBoard()
                    myBoard.createControls()

                    is_placing_dest = False
                    is_placing_spawn = False
                    pg.display.flip()


        clock.tick(60)
def visualize_path(board_mat,start,dest):
    open_list = []
    closed_list = []
    start_node = Node(None,start)
    open_list.append(start_node)
    while len(open_list) != 0:
        min_f = open_list[0].f
        min_coord = open_list[0].coord
        minInd = 0
        iters = 0
        for x in open_list:
            if x.f < min_f:
                min_f = x.f
                min_coord = x.coord
                minInd = iters
            iters += 1
        
        cur_node = open_list.pop(minInd)

        sucessors = gen_sucessors(board_mat, cur_node)

        for neighbor in sucessors:
            is_valid = True
            # Goal is found
            if neighbor.coord == dest:
                return neighbor, closed_list + open_list
            
            # Using Euclid distance Herustic
            neighbor.h = math.sqrt(((neighbor.coord[0] - dest[0]) ** 2) + ((neighbor.coord[1] - dest[1]) ** 2))
            neighbor.f = neighbor.g + neighbor.h
            
            # have a dictionary that contains the node as the key and the f as the value
            for x in closed_list:
                if x.coord == neighbor.coord:
                    if x.f <= neighbor.f:
                        is_valid = False
                    
            if is_valid:
                open_list.append(neighbor)
        
        closed_list.append(cur_node)

#generates valid neighbors for nodes
def gen_sucessors(board_mat,node):
    directions = [[0,1],[1,0],[-1,0],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]
    neighbors = []
    up, left, right, down = False, False, False, False
    for x in directions:
        resultant = [ node.coord[0] + x[0], node.coord[1] + x[1] ]
        # checks to see if coord falls within current board
        if (resultant[0] >= 0 and resultant[0] < 32) and (resultant[1] >= 0 and resultant[1] < 32):
            if board_mat[resultant[0]][resultant[1]] != 1:
                if x == [0,1]:
                    right = True
                elif x == [0,-1]:
                    left = True
                elif x == [1,0]:
                    up = True
                elif x == [-1,0]:
                    down = True
            
            #this adds another check for diagnols to enforce rules
                if x in [[1,1], [1,-1], [-1,-1], [-1,1]]:

                    if x == [1,1] and (up != False or right != False):
                        neighbors.append(Node(node,resultant))
                    elif x == [1,-1] and (up != False or left != False):
                        neighbors.append(Node(node,resultant))
                    elif x == [-1,-1] and (down != False or left != False):
                        neighbors.append(Node(node,resultant))
                    elif x == [-1,1] and (down != False or right != False):
                        neighbors.append(Node(node,resultant))
                else:
                    neighbors.append(Node(node,resultant))
    return neighbors

def construct_path(finalNode):
    path = []
    temp = finalNode
    while temp != None:
        path.append(temp.coord)
        print(temp) 
        temp = temp.parent
    return path[::-1]

#draws the final path to get from start to desination


#TODO use this function to check if player pressed on board
#checks to see if the rectangle passed was clicked on 
def rect_pressed(rect,coords):
    return coords[0] > rect[0] and coords[0] < rect[0] + rect[2] \
    and coords[1] > rect[1] and coords[1] < rect[1] + rect[3]


main()