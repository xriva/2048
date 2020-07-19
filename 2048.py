#from msvcrt import getch
import random
import tkinter as tk
import tkinter.messagebox
import tkinter.font 
fgcolors=[
    '#000000','#000000','#f9f6f2','#f9f6f2',
    '#f9f6f2','#f9f6f2','#f9f6f2','#f9f6f2',
    '#f9f6f2','#f9f6f2','#f9f6f2','#f9f6f2',
    '#f9f6f2','#f9f6f2','#f9f6f2','#f9f6f2'
]
bgcolors = [
    '#eee4da','#ede0c8','#f2b179','#f59563',
    '#f67c5f','#f65e3b','#edcf72','#edcc61',
    '#edc850','#edc53f','#edc22e','#3c3a32',
    '#3c3a32','#3c3a32','#3c3a32','#3c3a32'   # TODO update color for higher numbers
]
bgMap=dict(zip([2**(i+1) for i in range(16)], bgcolors))
bgMap[0] = '#eee4da'
fgMap=dict(zip([2**(i+1) for i in range(16)], fgcolors))
fgMap[0] = '#000000'


def genNum(board):
    target = 2 if random.random()<0.9 else 4

    pos=[]
    for i in range(4):
        for j in range(4):
            if board[i][j]==0:
                pos.append((i,j))
    if len(pos)==0:
        return False

    r,c = random.choice(pos)
    print('Choice:', len(pos), (r,c))

    board[r][c]=target
    return True

def printBoard(board):
    for row in board:
        print(" ".join(['%5d'%cell for cell in row]))

    for i in range(4):
        for j in range(4):
            x = board[i][j]
            boardLabel[i][j].config(text=('%d'%(x) if x>0 else ''), width=3,
                    font=font1 if x<1024 else font2, # TODO: auto-resizing
                    fg=fgMap[x], bg=bgMap[x], borderwidth=1, relief='ridge')

def movePoint(board, vector, top):
    a = None
    b = None
    for i in range(top,4):
        r,c=vector[i]
        if board[r][c]>0:
            if a is None:
                a = (r,c)
            else:
                b = (r,c)
                break

    if a is not None and b is not None and board[a[0]][a[1]]==board[b[0]][b[1]]:
        r,c = vector[top]
        board[r][c] = 2*board[a[0]][a[1]]
        if (r,c)!=a:
            board[a[0]][a[1]] = 0 
        board[b[0]][b[1]] = 0 
        print(a, '+', b, '->', (r,c))
        return True
    elif a is not None:
        r,c = vector[top]
        board[r][c] = board[a[0]][a[1]]
        if (r,c)!=a:
            board[a[0]][a[1]] = 0 
            return True

    return False


def moveVector(board, vector):
    hasMoved=False
    for i in range(4):
        if movePoint(board, vector, i):
            hasMoved=True
    return hasMoved

def moveBoard(board, key):
    hasMoved=False
    if key in ['Left','Right']:
        for i in range(4):
            if key=='Left':
                vector=[(i, j) for j in range(4)]
            else:
                vector=[(i, 3-j) for j in range(4)]
            if moveVector(board,vector):
                hasMoved=True
    else:
        for j in range(4):
            if key=='Up':
                vector=[(i, j) for i in range(4)]
            else:
                vector=[(3-i, j) for i in range(4)]
            if moveVector(board,vector):
                hasMoved=True
        
    return hasMoved

def emptyBoard(board):
    for i in range(4):
        for j in range(4):
            if board[i][j]>0:
                return False
    return True

def endGame(board):
    for i in range(4):
        for j in range(4):
            if board[i][j]==0:
                return False
    for i in range(4):
        for j in range(3):
            if board[i][j]==board[i][j+1]:
                return False
    for j in range(4):
        for i in range(3):
            if board[i][j]==board[i+1][j]:
                return False
    return True

def copyBoard(src, dst):
    print('copy board')
    for i in range(4):
        for j in range(4):
            dst[i][j]=src[i][j]

def keyPress(event):
    print("Key pressed", event, event.keysym)
    if event.keysym=='q':
        global root
        root.quit()
    elif event.keysym in ['Up','Down','Left','Right']:
        copyBoard(board, saved)
        if moveBoard(board, event.keysym) or emptyBoard(board):
            if not genNum(board):
                print("Game Over!")
                tk.messagebox.showerror('End', 'Game Over!')
            printBoard(board)
        elif endGame(board):
            print("Game Over!")
            tk.messagebox.showerror('End', 'Game Over!')

    elif event.keysym=='u':
        copyBoard(saved, board)
        printBoard(board)

root = tk.Tk()
root.title('2048')
frame = tk.Frame(root, width=200, height=200)
frame.bind('<Left>', keyPress)
frame.bind('<Right>', keyPress)
frame.bind('<Up>', keyPress)
frame.bind('<Down>', keyPress)
frame.bind('q', keyPress)
frame.bind('u', keyPress)

font1=tk.font.Font(family='Arial', size=48)
font2=tk.font.Font(family='Arial Narrow', size=36)

board = []
boardLabel = []
for i in range(4):
    board.append([0,0,0,0])
    boardLabel.append([])
    for j in range(4):
        L = tk.Label(frame, anchor='center',  text=str(board[i][j]))
        L.grid(row=i,column=j,sticky='nsew')
        boardLabel[i].append(L)

saved=[]
for i in range(4):
    saved.append([0,0,0,0])

printBoard(board)

frame.focus_set()
frame.pack()
root.mainloop()

