import pygame as pg
import time
BOARD_SIZE = (1024, 1024)
YELLOW = (255,255,0)
GRAY = (105,105,105)
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = ( 0, 0, 255)
class Board:
    cols = BOARD_SIZE[0] // 32
    rows = BOARD_SIZE[1] // 32
    SIZE = (1024,1024)
    def __init__(self,board):
        self.board = board
        # TODO: turn this into listcomp
        row = []
        self.spawnRect, self.destRect, self.visRect, self.resetRect = None, None, None, None
        self.board_matrix = [ [0] * self.cols for i in range(self.rows)]

    # Creates board part of application
    def createBoard(self):
        self.board.fill(BLACK)
        # resets the matrix incase reset button's been pressed
        self.board_matrix = [ [0] * self.cols for i in range(self.rows)]

        y = 0
        x = 0
        for _ in range(self.cols+1):
            
            pg.draw.line(self.board,WHITE,[0,y],[BOARD_SIZE[0],y],1)
            y+= 32
            
            pg.draw.line(self.board,WHITE,[x,0],[x,BOARD_SIZE[0]],1)
            x+= 32
        # I should proll update the screen here.... as of now I do it in the driver code

    # Creates opening screen
    def createIntro(self):
        self.board.fill(BLACK)
        titleFont = pg.font.Font('freesansbold.ttf', 32)
        bodyFont = pg.font.Font("freesansbold.ttf", 16)

        text = titleFont.render("INTRO",True,GREEN)
        textRect = text.get_rect()
        textRect.center = (BOARD_SIZE[0] // 2, 200)
        explanationStr1 = "The dialogue boxes gives you control of where to set the spawn/destination points,"
        explanationStr2 = "they also allow you to modify the parameters for the pathfinding algorithm."
        explanationStr3 = "The Red square represents the starting locaiton, the green square represents the destination."
        explanationStr4 = "The yellow squares represent the shortest path to and from, the blue squares represent the different squares that were explored."

        explainText = bodyFont.render(explanationStr1,True,GREEN)
        explainText2 = bodyFont.render(explanationStr2,True,GREEN)
        explainText3 = bodyFont.render(explanationStr3,True,GREEN)
        explainText4 = bodyFont.render(explanationStr4,True,GREEN)

        explainRect = explainText.get_rect()
        explainRect2 = explainText2.get_rect()
        explainRect3 = explainText3.get_rect()
        explainRect4 = explainText4.get_rect()


        explainRect.center = (BOARD_SIZE[0] // 2, 350)
        explainRect2.center = (BOARD_SIZE[0] // 2, 375)
        explainRect3.center = (BOARD_SIZE[0] // 2, 400)
        explainRect4.center = (BOARD_SIZE[0] // 2, 425)


        startText = titleFont.render("Start Pathfinding",True,YELLOW)
        startRect = startText.get_rect()
        startRect.center = (BOARD_SIZE[0] // 2, 600)

        self.board.blit(text,textRect)
        self.board.blit(explainText,explainRect)
        self.board.blit(explainText2,explainRect2)
        self.board.blit(explainText3,explainRect3)
        self.board.blit(explainText4,explainRect4)
        self.board.blit(startText,startRect)
    
    # Function creates the side pannel of the application
    def createControls(self):
        controlFont = pg.font.Font("freesansbold.ttf", 25)
        spawnText = controlFont.render("Start",True,BLACK,RED)
        self.spawnRect = spawnText.get_rect()
        self.spawnRect.center = (1124, 150) #1124 should be inbetween board and EOS

        destText = controlFont.render("Destination",True,BLACK,GREEN)
        self.destRect = destText.get_rect()
        self.destRect.center = (1124, 300)

        visText = controlFont.render("Visualize Path",True,BLACK,YELLOW)
        self.visRect = visText.get_rect()
        self.visRect.center = (1124,450)

        resetText = controlFont.render("Reset",True,BLACK,YELLOW)
        self.resetRect = resetText.get_rect()
        self.resetRect.center = (1124,600)

        self.board.blit(spawnText,self.spawnRect)
        self.board.blit(destText,self.destRect)
        self.board.blit(visText,self.visRect)
        self.board.blit(resetText,self.resetRect)
    
    def updateBoard(self,pos,color):
        # Adding slight offset allows for the white lines to stay on board
        smallRect = (pos[1]*32+1,pos[0]*32+1,31,31)
        
        # If an obstacle is placed the matrix is updated to reflect current state
        if color == GRAY:
            self.board_matrix[pos[0]][pos[1]] = 1
        else:
            self.board_matrix[pos[0]][pos[1]] = 0

        pg.draw.rect(self.board,color,smallRect)
    
    def drawPath(self,actualPath,extra):
        
        # Drawing explored Nodes
        for x in extra[1:len(extra) -1]:
            # In pygame need to interact with event queue so it doesn't think program's locked up
            pg.event.pump()
            self.updateBoard(x.coord,BLUE)
            pg.time.delay(10)
            pg.display.flip()
        
        # Drawing path
        for y in actualPath[1:len(actualPath) -1]:
            pg.event.pump()
            self.updateBoard(y,YELLOW)
            pg.time.delay(20)
            pg.display.flip()
        
