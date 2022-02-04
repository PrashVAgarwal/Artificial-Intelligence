import time
from copy import deepcopy
import random

prevboard = []
curboard = []
color = 0

with open("input.txt", 'r') as inf:
    color = int(inf.readline().strip())        #has value 1 for black and 2 for white

    for i in range(5):
        line = inf.readline().strip('\n')
        prevboard.append([int(x) for x in line])

    

    for i in range(5):
        line = inf.readline().strip('\n')
        curboard.append([int(x) for x in line])

    #print(color,prevboard,curboard)

#to calculate liberty of a particular stone and it returns a bool value
def liberty(a, b, board):
    allies = []
    st = []
    st.append((a, b))
    
    while len(st) != 0:
        s = st.pop()
        allies.append(s)
        i=s[0]
        j=s[1]

        neigh = []
        if i > 0:
            neigh.append((i-1, j))
        if i < len(board) - 1:
            neigh.append((i+1, j))
        if j > 0:
            neigh.append((i, j-1))
        if j < len(board) - 1:
            neigh.append((i, j+1))

        group = []
        for stone in neigh:
            if board[stone[0]][stone[1]] == board[a][b]:
                group.append(stone)

    
        for stone in group:
            if stone not in allies and stone not in st:
                st.append(stone)

    for stone in allies:
        i = stone[0]
        j = stone[1]
        neigh = []
        if i > 0:
            neigh.append((i-1, j))
        if i < len(board) - 1:
            neigh.append((i+1, j))
        if j > 0:
            neigh.append((i, j-1))
        if j < len(board) - 1:
            neigh.append((i, j+1))
        
        for item in neigh:
            if board[item[0]][item[1]] == 0:
                return True
    return False



#to remove the captured stones
def remove(color,board):
    extra = []
    for i in range(5):
        for j in range(5):
            if board[i][j] == color:
                if liberty(i,j,board) == False:
                    extra.append((i,j))

    for stone in extra:
        board[stone[0]][stone[1]] = 0
    
    return board



def possiblepos(i, j, color, board):
    if(i<0 or i>len(board)-1 or j<0 or j>len(board)-1 or board[i][j] !=0):
        return False

    temp = deepcopy(board)
    temp[i][j] = color

    if liberty(i,j,temp):
        return True

    temp = remove(3-color, temp)
    if liberty(i,j,temp):
        return True
    else:
        for i in range(5):
            for j in range(5):
                if temp[i][j] != prevboard[i][j]:
                    return True
        return False
        
    

def vacant(board, color):
    vacantpos = []
    for i in range(5):
        for j in range(5):
            #print(possiblepos(i,j,color,board))
            if possiblepos(i,j,color,board):
                vacantpos.append((i,j))
    #print(vacantpos)
    random.shuffle(vacantpos)
    return vacantpos


def finetune(board,movelist):
    badmoves=[]
    temp = deepcopy(board)
    for move in movelist:
        temp[move[0]][move[1]] = color
        opponentlist = vacant(temp,3-color)
        for mov in opponentlist:
            temp[mov[0]][mov[1]] = 3-color
            k = []
            for i in range(5):
                for j in range(5):
                    if temp[i][j] == color and not liberty(i,j,temp):
                        k.append((i,j))
            temp[mov[0]][mov[1]] = 0
            if move in k and move not in badmoves:
                badmoves.append(move)
        temp[move[0]][move[1]] = 0
    
    for t in badmoves:
        movelist.remove(t)
    return movelist


def bestmove():
    move = []
    stime = time.time()
    #print(stime)
    move = alphabeta(curboard, color, 5, float('-inf'), float('inf'), stime, max = True)
    #print(move)
    return ((move[0][0],move[0][1]))


def alphabeta(board, color, d, alpha, beta, stime, max):
    etime = time.time()
    temp = deepcopy(board)
    movelist = []
    movelist = vacant(temp, color)

    #finetuning our movelist by removing moves that lead to capture of our stones
    movelist = finetune(temp,movelist)
    
    #print(etime-stime)
    # base condition to stop recursion and return the score
    if(len(movelist) == 0 or d==0 or etime-stime > 8):
        black = 0
        white = 0
        for i in range(5):
            for j in range(5):
                if board[i][j] == 1:
                    black+= 1
                if board[i][j] == 2:
                    white+= 1
        white += 2.5

        if color == 1:
            score = black - white
        if color == 2:
            score = white - black

        return ((-5,-5),score)

                        

    # for maximizing player
    elif max:
        
        mx = float('-inf')
        for move in movelist:
            if possiblepos(move[0],move[1], color,temp):
                temp[move[0]][move[1]] = color
                temp = remove(3-color,temp)
            new = alphabeta(temp,3-color,d-1,alpha,beta,stime,False)
            if new[1] > mx:
                mx = new[1]
                best = move
            #print(alpha,new)
            if alpha < new[1]:
                alpha = new[1]
            #alpha = max(new[1],alpha)
            if beta <= alpha:
                break
        return (best,mx)


    #for minimizing player
    else:
        mn = float('inf')
        for move in movelist:
            if possiblepos(move[0],move[1], color,temp):
                temp[move[0]][move[1]] = color
                temp = remove(3-color,temp)
            new = alphabeta(temp,3-color,d-1,alpha,beta,stime,True)
            if new[1] < mn:
                mn = new[1]
                best = move
            beta = min(new[1],beta)
            if beta <= alpha:
                break
        return (best,mn)


def placeswzero(temp):
    zer=[]
    for i in range(5):
        for j in range(5):
            if temp[i][j] == 0:
                zer.append((i,j))
    return zer


def defeated(temp,color):
    c = {}
    
    zer = placeswzero(temp)
    #print(zer)
    for p in zer:
        d=[]
        temp[p[0]][p[1]] = color
        for i in range(5):
            for j in range(5):
                if temp[i][j] == (3-color) and not liberty(i,j,temp):
                    d.append((i,j))
        temp[p[0]][p[1]] = 0
        if len(d)>0:
            c[p] = len(d)
    
    #print(c)
    c = dict(sorted(c.items(), key = lambda item:item[1],reverse=True))
    #print(c)
    return c



def start(color):

    temp = deepcopy(curboard)

#finding an agressive move to play. Here we try to find a move that captures the most stones
#of the opponent. We use this strategy first as we want to have more stones on the board.
    noofstonesdefeated = defeated(temp,color)
    #print(noofstonesdefeated)
    for p in noofstonesdefeated:
        temp2 = deepcopy(temp)
        temp2[p[0]][p[1]] = color
        temp2 = remove(3-color,temp2)
        if prevboard!=temp2:
            return p

 #finetuning our movelist to get good move   
    movelist = vacant(temp, color)
    movelist = finetune(temp,movelist)

    if len(movelist) == 0:
        return None



#finding a safer move to play to avoid capture of our stones that is if the opponent can
#capture our stones in upcoming moves then we need to avoid that scenario. To do that
#we make a list of moves that the opponent can make and find out which of the moves will lead 
#to the max capture of our stones. Then we simply place our stone on that location to block the 
#opponent
    noofstonesdefeated = defeated(temp,3-color)

    for p in noofstonesdefeated:
        if p in movelist:
            return p



#list of good position in the start of the game. Selected these positions as they
#provide good oportunity to capture more territory and place more stones. These places give the
#opportunity to make a group with an eye and capture centre places so more liberty. Also since
#we have a time limit and initially the board is mostly vacant, we can speed up our game using
#this list
    if len(movelist) > 14:
        opt = [(2,2),(1,1),(1,3),(3,1),(3,3),(2,0),(2,4),(0,2),(4,2)]
        for i in opt:
            if i in movelist:
                return i 




    #st= time.time()
    #Here we use the minimax with alpha beta pruning to find the next best move
    m =  bestmove()
    #e=time.time()
    #print(m,e-st,sep=',')
    return m


#print(time.time())
m = start(color)
with open ("output.txt",'w') as outf:
    #print(m)
    if m == None or m == (-5,-5):
        print('PASS',file=outf,end='')
    else:
        print(m[0],m[1],file=outf,sep=',',end='')

    