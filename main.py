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
    startCoords = [None,None]
    destCoords = [None,None]
    inGame = False
    clicked = False
    inMenu = True
    path_finding_rect =[378,583,269,34]

    screen = pg.display.set_mode(BOARD_SIZE)
    pg.display.set_caption("Pathfinding Visualization")
    clock = pg.time.Clock()
    myBoard = Board(screen)
    pg.init()
    myBoard.createIntro()
    pg.display.flip()
    
    # Intro screen loop
    while inMenu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                inMenu = False
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if rect_pressed(path_finding_rect,pos):
                    inGame = True
                    inMenu = False
    
    # Creating display for real part of application
    screen = pg.display.set_mode(SCREEN_SIZE)
    myBoard.createBoard()
    myBoard.createControls()
    pg.display.flip()
    
    while inGame:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                inGame = False
            
            # These 2 if statements are used to see if user is holding down on button
            if event.type == pg.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pg.MOUSEBUTTONUP:
                clicked = False
            
            #TODO only set clicked to be true or false if within board else check to see if user mouse'd down on buton
            # if user is holding down on button
            if clicked:
                pos = pg.mouse.get_pos()
                # check to see if user is clicking on board
                if pos[0] <= 1024:
                    # they are in format: y, x (row, col)
                    gridCoord =[pos[1]//32,pos[0]//32]
                    
                    if is_placing_spawn:
                        # Checks to see if a spawn has already been placed
                        if startCoords != [None, None]:
                            myBoard.updateBoard(startCoords,BLACK)
                        myBoard.updateBoard(gridCoord,RED)
                        startCoords = gridCoord 
                        is_placing_spawn = False
                    
                    elif is_placing_dest:
                        # Checks to see if a destination has already been placed
                        if destCoords != [None, None]:
                            myBoard.updateBoard(destCoords,BLACK)
                        myBoard.updateBoard(gridCoord,GREEN)
                        is_placing_dest = False
                        destCoords = gridCoord
                    
                    else:
                        # Checks to see if trying to place outside of board
                        if gridCoord[0] < 32 and gridCoord[1] < 32:
                            myBoard.updateBoard(gridCoord,GRAY)
                            pg.display.flip()
                
                elif rect_pressed(myBoard.spawnRect,pos):
                    # Incase user presses both rectangles before placing on board
                    is_placing_spawn = True
                    is_placing_dest = False
                
                elif rect_pressed(myBoard.destRect,pos):
                    # Incase user presses both rectangles before placing on board
                    is_placing_dest = True
                    is_placing_spawn = False

                elif rect_pressed(myBoard.visRect,pos):
                    # More user friendly way to check user placed both spawn and dest in valid positions
                    # would be to use tkinter
                    if startCoords != [None, None] or destCoords != [None, None]:
                        final_node, other = aStar(myBoard.board_matrix,startCoords,destCoords)
                        if final_node != None and other != None:
                            
                            path = construct_path(final_node)
                            myBoard.drawPath(path,other)
                            pg.display.flip()

                elif rect_pressed(myBoard.resetRect,pos):
                    print(f"resetting...")
                    myBoard.createBoard()
                    myBoard.createControls()

                    is_placing_spawn, is_placing_dest= False, False
                    startCoords, destCoords = [None, None], [None, None]
                    pg.display.flip()
        pg.display.update()
        clock.tick(60)

def aStar(board_mat,start,dest):
    open_list = []
    closed_list = {}
    start_node = Node(None,start)
    open_list.append(start_node)
    # go until it's exhausted all options or path has been found
    while len(open_list) != 0:
        min_f = open_list[0].f
        minInd = 0
        iters = 0
        # Finds node with lowest F value in list
        for x in open_list:
            if x.f < min_f:
                min_f = x.f
                minInd = iters
            iters += 1
        
        cur_node = open_list.pop(minInd)
        #maybe add cur_node to closed here
        closed_list[cur_node] = cur_node.f

        # Gets valid neighbours (doesn't include positions with/and or obstructed by obstacles)
        sucessors = gen_sucessors(board_mat, cur_node)

        for neighbor in sucessors:
            is_valid = True
            # Goal is found
            if neighbor.coord == dest:
                combined = []
                # Had to turn the keys into an array like this because it didn't like closed_list.keys() + open_list
                for node in closed_list.keys():
                    combined.append(node)
                return neighbor, combined + open_list
            
            # Using Euclid distance Herustic
            neighbor.h = math.sqrt(((neighbor.coord[0] - dest[0]) ** 2) + ((neighbor.coord[1] - dest[1]) ** 2))
            neighbor.f = neighbor.g + neighbor.h
            
            # Checks to see if node has already been explored
            for nodes in closed_list:
                if nodes.coord == neighbor.coord:
                    if closed_list[nodes] <= neighbor.f:
                        is_valid = False
            
            # Checks to see if a better version already exists in the frontier array
            for nodes in open_list:
                if nodes.coord == neighbor.coord:
                    if nodes.f <= neighbor.f:
                        is_valid = False

            # If hasn't been explored and no better version found at it to frontier
            if is_valid:
                open_list.append(neighbor)
    return None, None
        
# Generates valid neighbors for nodes
def gen_sucessors(board_mat,node):
    directions = [[0,1],[1,0],[-1,0],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]
    neighbors = []
    up, left, right, down = False, False, False, False
    for x in directions:
        resultant = [ node.coord[0] + x[0], node.coord[1] + x[1] ]
        # Checks to see if coord falls within current board
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
            
                # This adds another check for diagnols to enforce rules about obstructed paths
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

# Recursively iterates through nodes to find the coords for each node
def construct_path(finalNode):
    path = []
    temp = finalNode
    while temp != None:
        path.append(temp.coord)
        temp = temp.parent
    return path[::-1]


# Checks to see if the rectangle passed was clicked on by user
def rect_pressed(rect,coords):
    return coords[0] > rect[0] and coords[0] < rect[0] + rect[2] \
    and coords[1] > rect[1] and coords[1] < rect[1] + rect[3]


main()