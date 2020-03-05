from random import choice
import pyglet

window = pyglet.window.Window(width=400, height = 450, caption="GameWindow")

Im1 = pyglet.image.load('avocado.png')
Im2 = pyglet.image.load('banana-juice.png')
Im3 = pyglet.image.load('coconut.png')
Im4 = pyglet.image.load('fruit.png')
Im5 = pyglet.image.load('watermelon.png')

def InitializeGrid(board):
    #Initialize Grid by reading in from file
    #Initialize Grid by random value
    for i in range (8):
        for j in range(8):
            board[i][j] = choice(['A','B','C','D','E'])
    #print("Initializing grid")

def Initialize(board):
    #Initialize game
    #Initialize grid
        # Set up the grid with an initial arrangement of letters
    InitializeGrid(board)
    #Initialize score
    global score
    score = 0
    #Initialize turn number
    global turn
    turn = 1

def ContinueGame(current_score, goal_score=100):
    #Return false if game should end, true if game is not over
        # If score is greater than goal score, return false
        # Otherwise, return true
    if (current_score >= goal_score):
        return False
    else:
        return True

def SwapPieces(board, move):

    #Swap objects in two positions
    temp = board[move[0]][move[1]]
    board[move[0]][move[1]]= board[move[2]][move[3]]
    board[move[2]][move[3]] = temp

@window.event
def on_draw():
    window.clear()
    for i in range(7,-1,-1):
        #Draw each row
        y=50+(50*i)
        for j in range(8):
            #draw each piece, first getting position
            x = 50 * j
            if board[i][j] == 'A':
                Im1.blit(x,y)
            elif board[i][j] == 'B':
                Im2.blit(x,y)
            elif board[i][j] == 'C':
                Im3.blit(x,y)
            elif board[i][j] == 'D':
                Im4.blit(x,y)
            elif board[i][j] == 'E':
                Im5.blit(x,y)
    label = pyglet.text.Label('Turn: '+str(turn)+'   Score:  '+str(score),
                              font_name='Arial',
                              font_size=18,
                              x=20,y=10)
    label.draw()

def RemovePieces(board):
    #Remove 3-in-a-row and 3-in-a-col pieces
    #Create board to store remove-or-not
    remove =   [[0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0]]
    #Go through rows
    for i in range(8):
        for j in range(6):
            if (board[i][j] == board[i][j+1]) and (board[i][j] == board[i][j+2]):
                #three in a row are the same!
                remove[i][j] = 1;
                remove[i][j+1] = 1;
                remove[i][j+2] =1;

    #Go through columns
    for j in range(8):
        for i in range(6):
            if (board[i][j]==board[i+1][j]) and (board[i][j] == board[i+2][j]):
                #three in a row are the same!
                remove[i][j] = 1;
                remove[i+1][j] = 1;
                remove[i+2][j]=1;
    #Eliminate those marked
    global score
    removed_any = False
    for i in range(8):
        for j in range(8):
            if remove[i][j] == 1:
                board[i][j] = 0
                score += 1
                removed_any = True
    return removed_any

def DropPieces(board):
    #Drop pieces to fill in blanks
    for j in range(8):
        #make list of pieces in the column
        listofpieces = []
        for i in range(8):
            if board[i][j] != 0:
                listofpieces.append(board[i][j])
        #copy that list into column
        for i in range(len(listofpieces)):
            board[i][j] = listofpieces[i]
        #fill in remainder of column with 0s
        for i in range(len(listofpieces),8):
            board[i][j] = 0

def FillBlank(board):
    #Fill blanks with random pieces
    for i in range(8):
        for j in range(8):
            if (board[i][j] == 0):
                board[i][j] = choice(['A','B','C','D','E'])

def Update(board, move):
    #Update the board according to move
    SwapPieces(board,move)
    pieces_eliminated = True
    while pieces_eliminated:
        pieces_eliminated = RemovePieces(board)
        DropPieces(board)
        FillBlank(board)

@window.event
def on_mouse_press(x,y,button,modifiers):
    #Get the starting cell
    global startx
    global starty
    startx = x
    starty = y

@window.event
def on_mouse_release(x, y, button, modifiers):
    #Get starting and ending cell and see if they are adjacent
    startcol = startx//50
    startrow = (starty-50)//50
    endcol = x//50
    endrow = (y-50)//50
    #Check whether ending is adjacent to starting and if so, make move.
    if ((startcol == endcol and startrow==endrow - 1) or (startrow==endrow and startcol==endcol+1)or (startcol==endcol and startrow==endrow+1) or (startrow==endrow and startcol==endcol-1)):
        Update(board,[startrow,startcol,endrow,endcol])
        global turn
        turn+=1
        #See if game is over
        if not ContinueGame(score):
            print("You won in", turn,"turns!","Final score was ", score,".")
            pyglet.app.exit()

#State main variables
#Set the user's score to zero
score = 100
#Set any other variables (such as counter for turn number) to initial values
turn = 100
goalscore = 100
board = [[0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0]]
#Initialize
Initialize(board)

pyglet.app.run()

print('Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>')
print('Icons made by <a href="https://www.flaticon.com/authors/vitaly-gorbachev" title="Vitaly Gorbachev">Vitaly Gorbachev</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>')
print('Icons made by <a href="https://www.flaticon.com/authors/monkik" title="monkik">monkik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>')


