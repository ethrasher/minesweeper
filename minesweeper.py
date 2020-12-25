# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
import random
import time
import string
import json

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.startTime = time.time()
    data.mode = "startScreen"
    data.width = 600
    data.height = 600
    data.margin = 10
    data.gameOver = None
    stats = {}
    data.finishedTime = 0
    data.textMode = None
    data.TLX = data.margin
    data.TLY = data.margin
    data.BRX = data.width-data.margin
    data.BRY = data.height-data.margin
    data.gridMargin = 40
    data.lock = False
    data.gridTLX = data.margin + data.gridMargin
    data.gridTLY = data.margin + data.gridMargin+ 90
    data.gridBRX = data.width-data.margin-data.gridMargin
    data.gridBRY = data.height-data.margin-data.gridMargin
    data.rows = 10
    data.cols = 10
    data.numOfBombs = 10
    data.red = 0
    data.green = 0
    data.blue = 0
    data.rowString = ""
    data.colString = ""
    data.bombString = ""
    data.redString = ""
    data.greenString = ""
    data.blueString = ""

def printBoard(data):
    for row in range (data.rows):
        print(data.board[row])
    print()

def createBoard(data):
    data.board = []
    for row in range (0, data.rows):
        data.board.append([])
        for col in range (0, data.cols):
            data.board[row].append(0)

def createFlip(data):
    data.flipped = []
    for row in range (0, data.rows):
        data.flipped.append([])
        for col in range (0, data.cols):
            data.flipped[row].append(False)

def setBombs(data):
    for bomb in range (data.numOfBombs):
        row = random.randint(0, data.rows-1)
        col = random.randint(0, data.cols-1)
        while (data.bombs.count((row, col)) != 0):
            row = random.randint(0, data.rows-1)
            col = random.randint(0, data.cols-1)
        data.bombs.append((row, col))
        data.board[row][col] = -1

        for newrow in range (-1, 2):
            for newcol in range (-1, 2):
                if (newrow == 0 and newcol == 0):
                    continue
                if (row+newrow >= 0 and row+newrow<data.rows):
                    if (col+newcol >= 0 and col+newcol < data.cols):
                        if (data.board[row+newrow][col+newcol] != -1):
                            data.board[row+newrow][col+newcol] += 1

def mousePressed(event, data):
    # use event.x and event.y
    if (data.gameOver == None and data.mode == "Play"):
        gridWidth = data.gridBRX - data.gridTLX
        gridHeight = data.gridBRY - data.gridTLY
        boxWidth = gridWidth/data.cols
        boxHeight = gridHeight/data.rows
        for row in range (data.rows):
            for col in range (data.cols):
                if (data.flipped[row][col]!=True):
                    clickInBox(data, row, col, event.x, event.y, data.gridTLX+boxWidth*col, data.gridTLY+boxHeight*row, data.gridTLX+boxWidth*col+boxWidth, data.gridTLY+boxHeight*row+boxHeight)
        if (numOfFlipped(data)+data.numOfBombs == data.rows*data.cols):
            data.gameOver = True
            youWin(data)
    if (data.width/9 *7<=event.x and data.TLY+70<=event.y and data.BRX-20>=event.x and data.TLY+100>=event.y):
        finishedInputs(data)
    if (data.TLX+20<=event.x and data.TLY+70<=event.y and data.width/9 *2>=event.x and data.TLY+100>=event.y):
        data.lock = True
        return
    data.lock = False
    if (data.mode == "startScreen"):
        x = event.x; y=event.y;

        if (x>=data.width/2 and y>=data.TLY+145 and x<=data.width*3/4 and y<=data.TLY+180):
            data.textMode = "Row"
        if (x>=data.width/2 and y>=data.TLY+195 and x<=data.width*3/4 and y<=data.TLY+230):
            data.textMode = "Col"
        if (x>=data.width/2 and y>=data.TLY+245 and x<=data.width*3/4 and y<=data.TLY+280):
            data.textMode = "Bombs"

        if (x>=data.width/2 and y>=data.TLY+345 and x<=data.width*3/4 and y<=data.TLY+380):
            data.textMode = "Red"
        if (x>=data.width/2 and y>=data.TLY+395 and x<=data.width*3/4 and y<=data.TLY+430):
            data.textMode = "Green"
        if (x>=data.width/2 and y>=data.TLY+445 and x<=data.width*3/4 and y<=data.TLY+480):
            data.textMode = "Blue"

        if (x>=data.width/2-50 and y>=data.TLY+500 and x<=data.width/2+50 and y<=data.TLY+550):
            finishedInputs(data)

def finishedInputs(data):
    if (data.rowString != ""):
        data.rows = int(data.rowString)
    if (data.colString != ""):
        data.cols = int(data.colString)
    if (data.bombString != ""):
        if (int(data.bombString)<data.rows*data.cols):
            data.numOfBombs = int(data.bombString)
        else:
            data.numOfBombs = data.rows*data.cols -1
    if (data.redString != ""):
        data.red = int(data.redString)
    if (data.greenString != ""):
        data.green = int(data.greenString)
    if (data.blueString != ""):
        data.blue = int(data.blueString)
    data.textMode = None
    data.startTime = time.time()
    data.mode = "Play"
    data.startTime = time.time()
    data.gameOver = None
    data.lock = False
    createBoard(data)
    data.bombs = []
    setBombs(data)
    createFlip(data)

def floodFill(data, row, col):
    if (row<0 or col<0 or row>=data.rows or col>=data.cols):
        return
    elif (data.flipped[row][col]==True or data.flipped[row][col]==None):
        return
    elif (data.board[row][col]!=0):
        data.flipped[row][col] = True
        return
    else:
        data.flipped[row][col] = True
        for i in range(-1, 2):
            for j in range (-1, 2):
                floodFill(data, row+i, col+j)
def numOfFlipped(data):
    count = 0
    for row in range (data.rows):
        for col in range (data.cols):
            if (data.flipped[row][col]):
                count+=1
    return count

def clickInBox(data, row, col, x, y, TLX, TLY, BRX, BRY):
    if (data.lock):
        if (TLX<=x and BRX>=x and TLY<=y and BRY>=y):
            if (data.flipped[row][col]==None):
                data.flipped[row][col]=False
            elif (data.flipped[row][col]==False):
                data.flipped[row][col] = None
    else:
        if (TLX<=x and BRX>=x and TLY<=y and BRY>=y):
            if (data.flipped[row][col]==None):
                return
            floodFill(data, row, col)
            if (data.board[row][col] == -1):
                gameOver(data)

def gameOver(data):
    data.gameOver = True
    data.finishedTime = time.time()-data.startTime
    for row in range (data.rows):
        for col in range (data.cols):
            data.flipped[row][col] = True

def youWin(data):
    data.gameOver=False
    data.finishedTime = time.time()-data.startTime
    for row in range (data.rows):
        for col in range (data.cols):
            data.flipped[row][col] = True

def keyPressed(event, data):
    # use event.char and event.keysym
    if (event.keysym.isdigit() or event.keysym == "BackSpace"):
        if (data.textMode == "Row"):
            if (event.keysym == "BackSpace"):
                data.rowString = data.rowString[:-1]
            else:
                data.rowString = data.rowString + event.keysym
        if (data.textMode == "Col"):
            if (event.keysym == "BackSpace"):
                data.colString = data.colString[:-1]
            else:
                data.colString = data.colString + event.keysym
        if (data.textMode == "Bombs"):
            if (event.keysym == "BackSpace"):
                data.bombString = data.bombString[:-1]
            else:
                data.bombString = data.bombString + event.keysym
        if (data.textMode == "Red"):
            if (event.keysym == "BackSpace"):
                data.redString = data.redString[:-1]
            else:
                data.redString = data.redString + event.keysym
        if (data.textMode == "Green"):
            if (event.keysym == "BackSpace"):
                data.greenString = data.greenString[:-1]
            else:
                data.greenString = data.greenString + event.keysym
        if (data.textMode == "Blue"):
            if (event.keysym == "BackSpace"):
                data.blueString = data.blueString[:-1]
            else:
                data.blueString = data.blueString + event.keysym
    if (data.redString != "" and int(data.redString)<=255):
        data.red = int(data.redString)
    if (data.greenString != "" and int(data.greenString)<=255):
        data.green = int(data.greenString)
    if (data.blueString != "" and int(data.blueString)<=255):
        data.blue = int(data.blueString)
    

def timerFired(data):
    currentTime = time.time()-data.startTime
    maxTime = 600
    if (int(currentTime)>=maxTime):
        gameOver(data)

def redrawAll(canvas, data):
    # draw in canvas
    if (data.mode == "Play"):
        color = rgbString(data.red, data.green, data.blue)
        inverseColor = rgbString(255-data.red, 255-data.green, 255-data.blue)
        if (data.lock):
            temp=color
            color=inverseColor
            inverseColor=temp
        canvas.create_rectangle(data.TLX, data.TLY, data.BRX, data.BRY, fill = color)
        if (data.gameOver == None):
            canvas.create_text(data.width/2-2, data.TLY + 43, text = "Minesweeper", fill = "grey21", font = "Helvetica 50 bold")
            canvas.create_text(data.width/2, data.TLY + 40, text = "Minesweeper", fill = "black", font = "Helvetica 50 bold")
        elif (data.gameOver == True):
            canvas.create_text(data.width/2, data.TLY + 40, text = "Game Over", fill = "black", font = "Helvetica 50 bold")
        else:
            canvas.create_text(data.width/2, data.TLY + 40, text = "You Win!", fill = "black", font = "Helvetica 50 bold")
        canvas.create_rectangle(data.width/9 *7, data.TLY+70, data.BRX-20, data.TLY+100, fill="black", outline = "white", width = 3)
        canvas.create_text(data.width/8 *7, data.TLY + 85, fill = "white", font = "Helvetica 20 bold", text = "Reset")
        canvas.create_rectangle(data.TLX+20,  data.TLY+70, data.width/9 *2, data.TLY+100, fill=inverseColor, outline = "white", width = 3)
        canvas.create_text(data.width/8 *1, data.TLY + 85, fill = "white", font = "Helvetica 20 bold", text = "Lock")
        drawTime(canvas, data)
        drawBoard(canvas, data)
    elif (data.mode == "startScreen"):
        drawStartScreen(canvas, data)

def drawStartScreen(canvas, data):
    canvas.create_rectangle (data.TLX, data.TLY, data.BRX, data.BRY, fill = "white", outline = "white")
    canvas.create_text(data.width/2-2, data.TLY + 43, text = "Minesweeper", fill = "grey21", font = "Helvetica 50 bold")
    canvas.create_text(data.width/2, data.TLY + 40, text = "Minesweeper", fill = "black", font = "Helvetica 50 bold")
    canvas.create_text(data.width/10, data.TLY+150, anchor = NW, text="Rows:", fill = "black", font = "helvetica 20 bold")
    canvas.create_text(data.width/10, data.TLY+200, anchor = NW, text="Columns:", fill = "black", font = "helvetica 20 bold")
    canvas.create_text(data.width/10, data.TLY+250, anchor = NW, text="Number of Bombs:", fill = "black", font = "helvetica 20 bold")
    if (data.textMode == "Row"):
        canvas.create_rectangle(data.width/2, data.TLY+145, data.width*3/4, data.TLY+180, fill = "white", outline = "black", width = 3)
    else:
        canvas.create_rectangle(data.width/2, data.TLY+145, data.width*3/4, data.TLY+180, fill = "white", outline = "black")
    if (data.textMode == "Col"):
        canvas.create_rectangle(data.width/2, data.TLY+195, data.width*3/4, data.TLY+230, fill = "white", outline = "black", width = 3)
    else:
        canvas.create_rectangle(data.width/2, data.TLY+195, data.width*3/4, data.TLY+230, fill = "white", outline = "black")
    if (data.textMode == "Bombs"):
        canvas.create_rectangle(data.width/2, data.TLY+245, data.width*3/4, data.TLY+280, fill = "white", outline = "black", width = 3)
    else:
        canvas.create_rectangle(data.width/2, data.TLY+245, data.width*3/4, data.TLY+280, fill = "white", outline = "black")
    canvas.create_text(data.width/10, data.TLY+350, anchor = NW, text="Red", fill = "black", font = "helvetica 20 bold")
    canvas.create_text(data.width/10, data.TLY+400, anchor = NW, text="Green", fill = "black", font = "helvetica 20 bold")
    canvas.create_text(data.width/10, data.TLY+450, anchor = NW, text="Blue", fill = "black", font = "helvetica 20 bold")
    if (data.textMode == "Red"):
        canvas.create_rectangle(data.width/2, data.TLY+345, data.width*3/4, data.TLY+380, fill = "white", outline = "black", width = 3)
    else:
        canvas.create_rectangle(data.width/2, data.TLY+345, data.width*3/4, data.TLY+380, fill = "white", outline = "black")
    if (data.textMode == "Green"):
        canvas.create_rectangle(data.width/2, data.TLY+395, data.width*3/4, data.TLY+430, fill = "white", outline = "black", width = 3)
    else:
        canvas.create_rectangle(data.width/2, data.TLY+395, data.width*3/4, data.TLY+430, fill = "white", outline = "black")
    if (data.textMode == "Blue"):
        canvas.create_rectangle(data.width/2, data.TLY+445, data.width*3/4, data.TLY+480, fill = "white", outline = "black", width = 3)
    else:
        canvas.create_rectangle(data.width/2, data.TLY+445, data.width*3/4, data.TLY+480, fill = "white", outline = "black")
    color = rgbString(data.red, data.green, data.blue)
    canvas.create_rectangle(data.width*8/10, data.TLY+395, data.width*9/10, data.TLY+430, fill = color, outline = "black")

    canvas.create_rectangle(data.width/2-50, data.TLY+500, data.width/2+50, data.TLY+550, fill="grey77", outline = "black")
    canvas.create_text(data.width/2, data.TLY+525, text = "Done", fill = "black", font = "Helvetica 20 bold")

    canvas.create_text(data.width/2+5, data.TLY+150, anchor= NW, text = data.rowString, fill = "black", font = "Helvetica 20 bold")
    canvas.create_text(data.width/2+5, data.TLY+200, anchor= NW, text = data.colString, fill = "black", font = "Helvetica 20 bold")
    canvas.create_text(data.width/2+5, data.TLY+250, anchor= NW, text = data.bombString, fill = "black", font = "Helvetica 20 bold")
    canvas.create_text(data.width/2+5, data.TLY+350, anchor= NW, text = data.redString, fill = "black", font = "Helvetica 20 bold")
    canvas.create_text(data.width/2+5, data.TLY+400, anchor= NW, text = data.greenString, fill = "black", font = "Helvetica 20 bold")
    canvas.create_text(data.width/2+5, data.TLY+450, anchor= NW, text = data.blueString, fill = "black", font = "Helvetica 20 bold")

def drawTime(canvas, data):
    canvas.create_text(data.width/2 -25, data.TLY + 80, text = "Time:", fill = "black", font = "Helvetica 20 bold")
    currentTime = time.time()-data.startTime
    if (data.gameOver == None):
        minutes = int(currentTime//60)
        seconds = int((currentTime%60)*100)/100
    else:
        minutes = int(data.finishedTime//60)
        seconds = int((data.finishedTime%60)*100)/100
    canvas.create_text(data.width/2 + 30, data.TLY+70, text = minutes, fill = "black", font = "Helvetica 20 bold", anchor = NE)
    canvas.create_text(data.width/2 + 32, data.TLY+70, text = ":", fill = "black", font = "Helvetica 20 bold", anchor = NW)
    canvas.create_text(data.width/2 + 42, data.TLY+70, text = seconds, fill = "black", font = "Helvetica 20 bold", anchor = NW)

def drawBoard(canvas, data):
    gridWidth = data.gridBRX - data.gridTLX
    gridHeight = data.gridBRY - data.gridTLY
    boxWidth = gridWidth/data.cols
    boxHeight = gridHeight/data.rows
    for row in range (data.rows):
        for col in range (data.cols):
            if (data.flipped[row][col]==True):
                drawFlippedBox(canvas, data, row, col, data.gridTLX+boxWidth*col, data.gridTLY+boxHeight*row, data.gridTLX+boxWidth*col+boxWidth, data.gridTLY+boxHeight*row+boxHeight)
            elif (data.flipped[row][col]==False):
                drawUnflippedBox(canvas, data, row, col, data.gridTLX+boxWidth*col, data.gridTLY+boxHeight*row, data.gridTLX+boxWidth*col+boxWidth, data.gridTLY+boxHeight*row+boxHeight)
            else:
                drawLockedBox(canvas, data, row, col, data.gridTLX+boxWidth*col, data.gridTLY+boxHeight*row, data.gridTLX+boxWidth*col+boxWidth, data.gridTLY+boxHeight*row+boxHeight)

def drawUnflippedBox(canvas, data, row, col, TLX, TLY, BRX, BRY):
    mainColor = rgbString(data.red, data.green, data.blue)
    lightest = rgbString(min(data.red+50,255), min(data.green+50, 255), min(data.blue+50, 255))
    darkest = rgbString(max(data.red-50,0), max(data.green-50,0), max(data.blue-50,0))
    lighter = rgbString(min(data.red+25,255), min(data.green+25, 255), min(data.blue+25, 255))
    darker = rgbString(max(data.red-25,0), max(data.green-25,0), max(data.blue-25,0))
    miniWidth = (BRX-TLX)/2
    miniHeight = (BRY-TLY)/2

    canvas.create_polygon(TLX,TLY,TLX+miniWidth/2, TLY+miniHeight/2, BRX-miniWidth/2, TLY+miniHeight/2, BRX, TLY, fill = lightest)
    canvas.create_polygon(BRX, TLY, BRX-miniWidth/2, TLY+miniHeight/2, BRX-miniWidth/2, BRY-miniHeight/2, BRX, BRY,  fill = lighter)
    canvas.create_polygon(BRX, BRY, BRX-miniWidth/2, BRY-miniHeight/2, TLX+miniWidth/2, BRY-miniHeight/2, TLX, BRY, fill = darkest)
    canvas.create_polygon(TLX, BRY, TLX+miniWidth/2, BRY-miniHeight/2, TLX+miniWidth/2, TLY+miniHeight/2, TLX, TLY, fill = darker)
    canvas.create_rectangle(TLX+miniWidth/2, TLY+miniHeight/2, BRX-miniWidth/2, BRY-miniHeight/2, fill = mainColor, outline = mainColor)

def drawLockedBox(canvas, data, row, col, TLX, TLY, BRX, BRY):
    red = 255-data.red; green = 255-data.green; blue = 255-data.blue;
    mainColor = rgbString(red, green, blue)
    lightest = rgbString(min(red+50,255), min(green+50, 255), min(blue+50, 255))
    darkest = rgbString(max(red-50,0), max(green-50,0), max(blue-50,0))
    lighter = rgbString(min(red+25,255), min(green+25, 255), min(blue+25, 255))
    darker = rgbString(max(red-25,0), max(green-25,0), max(blue-25,0))
    miniWidth = (BRX-TLX)/2
    miniHeight = (BRY-TLY)/2

    canvas.create_polygon(TLX,TLY,TLX+miniWidth/2, TLY+miniHeight/2, BRX-miniWidth/2, TLY+miniHeight/2, BRX, TLY, fill = lightest)
    canvas.create_polygon(BRX, TLY, BRX-miniWidth/2, TLY+miniHeight/2, BRX-miniWidth/2, BRY-miniHeight/2, BRX, BRY,  fill = lighter)
    canvas.create_polygon(BRX, BRY, BRX-miniWidth/2, BRY-miniHeight/2, TLX+miniWidth/2, BRY-miniHeight/2, TLX, BRY, fill = darkest)
    canvas.create_polygon(TLX, BRY, TLX+miniWidth/2, BRY-miniHeight/2, TLX+miniWidth/2, TLY+miniHeight/2, TLX, TLY, fill = darker)
    canvas.create_rectangle(TLX+miniWidth/2, TLY+miniHeight/2, BRX-miniWidth/2, BRY-miniHeight/2, fill = mainColor, outline = mainColor)

def drawFlippedBox(canvas, data, row, col, TLX, TLY, BRX, BRY):
    currentNum = data.board[row][col]
    canvas.create_rectangle(TLX, TLY, BRX, BRY, fill = "white")
    centerX = (BRX+TLX)/2
    centerY = (BRY+TLY)/2
    if (currentNum == -1):
        drawBomb(canvas, data, TLX, TLY, BRX, BRY)
    else:
        canvas.create_text(centerX, centerY, text = currentNum, fill = "blue2", font = "Helvetica 20 bold")

def drawBomb (canvas, data, TLX, TLY, BRX, BRY):
    miniWidth = BRX-TLX
    miniHeight = BRY-TLY
    centerX = (TLX+BRX)/2
    centerY = TLY + miniHeight*16/24
    bTLX = TLX+miniWidth/5
    bBRX = BRX-miniWidth/5
    bTLY = TLY+miniHeight/2
    bBRY = BRY-miniHeight/12
    if (bBRY-bTLY==bBRX-bTLX):
        pass
    elif (bBRY-bTLY<bBRX-bTLX):
        ideal = bBRY-bTLY
        bTLX = centerX-ideal/2
        bBRX = centerX+ideal/2
    else:
        ideal = bBRX-bTLX
        bTLY = centerY-ideal/2
        bBRY = centerY+ideal/2
    rTLX = bTLX + (bBRX-bTLX)/4
    rTLY = bTLY - (bBRY-bTLY)/10
    rBRX = bBRX - (bBRX-bTLX)/4
    rBRY = centerY
    #canvas.create_oval(BRX-miniWidth/4, TLY+miniHeight/7, centerX, TLY+miniHeight/2, fill = "white", outline = "grey", width = 3)
    canvas.create_rectangle(rTLX, rTLY, rBRX, rBRY, fill = "black")
    canvas.create_oval(bTLX, bTLY, bBRX, bBRY, fill = "black")
    bombheight = bBRY-bTLY
    octorad = min((BRX-TLX)/3, (BRY-TLY)/3)
    pointer = bTLY-rTLY
    canvas.create_polygon(
                            centerX-octorad/6, rTLY, centerX-(octorad/2), rTLY,
                            centerX-octorad/2, rTLY-octorad/3, centerX-octorad/2-bombheight/4, (rTLY-octorad/3 + rTLY-octorad*2/3)/2,
                            centerX-octorad/2, rTLY-octorad*2/3, (centerX-octorad/2), (rTLY-octorad),
                            centerX-octorad/6, rTLY-octorad, centerX, rTLY-octorad-bombheight/4,
                            centerX+octorad/6, rTLY-octorad, (centerX+octorad/2), (rTLY-octorad),
                            centerX+octorad/2, rTLY-octorad*2/3, centerX+octorad/2+bombheight/4, (rTLY-octorad/3 + rTLY-octorad*2/3)/2,
                            centerX+octorad/2, rTLY-octorad/3, (centerX+octorad/2), rTLY, 
                            centerX+octorad/6, rTLY, centerX, rTLY+bombheight/4,
                            fill="red")



def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

####################################
# use the run function as-is
####################################

def run(width=600, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)