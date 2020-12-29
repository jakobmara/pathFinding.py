import pygame as pg
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


    def getElement(self,coord):
        return self.board_matrix[coord[0]][coord[1]]

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
        print(f"rows: {self.rows}, cols: {self.cols}")

    def createIntro(self):
        self.board.fill(BLACK)
        titleFont = pg.font.Font('freesansbold.ttf', 32)
        bodyFont = pg.font.Font("freesansbold.ttf", 16)

        text = titleFont.render("INTRO",True,GREEN)
        textRect = text.get_rect()
        textRect.center = (BOARD_SIZE[0] // 2, 200)
        explanationStr1 = "The dialogue boxes gives you control of where to set the spawn/destination points,"
        explanationStr2 = "they also allow you to modify the parameters for the pathfinding algorithm."


        explainText = bodyFont.render(explanationStr1,True,GREEN)
        explainText2 = bodyFont.render(explanationStr2,True,GREEN)

        explainRect = explainText.get_rect()
        explainRect2 = explainText2.get_rect()

        explainRect.center = (BOARD_SIZE[0] // 2, 350)
        explainRect2.center = (BOARD_SIZE[0] // 2, 375)


        startText = titleFont.render("Start Pathfinding",True,YELLOW)
        startRect = startText.get_rect()
        startRect.center = (BOARD_SIZE[0] // 2, 600)
        print(f"rectangle: {startRect}")

        self.board.blit(text,textRect)
        self.board.blit(explainText,explainRect)
        self.board.blit(explainText2,explainRect2)
        self.board.blit(startText,startRect)
    def createControls(self):
        controlFont = pg.font.Font("freesansbold.ttf", 20)
        spawnText = controlFont.render("Start",True,BLACK,RED)
        self.spawnRect = spawnText.get_rect()
        self.spawnRect.center = (1124, 150) #1124 should be inbetween board and border


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
        smallRect = (pos[1]*32,pos[0]*32,32,32)
        print(f"grid location: {pos} rect: {smallRect}")
        
        # If an obstacle is placed the matrix is updated to reflect current state
        if color == GRAY:
            self.board_matrix[pos[0]][pos[1]] = 1
        else:
            self.board_matrix[pos[0]][pos[1]] = 0

        pg.draw.rect(self.board,color,smallRect)
    

    def drawPath(self, game,arr):
        print("DRAWING...")
        for x in arr[1:len(arr) -1]:
            self.updateBoard(x,YELLOW)
            game.time.delay(250)
            game.display.flip()
        print("Done")

    def drawPath2(self, game,actualPath,extra):
        print("DRAWING...")
        
        for x in extra[1:len(extra) -1]:
            print("drawing error")
            self.updateBoard(x.coord,BLUE)
            game.time.delay(10)
            game.display.flip()
        print(f"drawing path:")
        # my attempt at doing both in 1
        for y in actualPath[1:len(actualPath) -1]:
            self.updateBoard(y,YELLOW)
            game.time.delay(250)
            game.display.flip()
        print("Done")