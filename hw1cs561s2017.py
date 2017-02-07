import os, sys, copy

#inputFilePath = sys.argv[1]
inputFilePath = os.path.dirname(os.path.realpath(__file__)) + "/SampleTestCases/input1.txt"
outputFilePath = os.path.dirname(os.path.realpath(__file__)) + "/SampleTestCases/output.txt"

s = dict()
for i in range(-5999,6000):
    s[i] = str(i)
s[-6000],s[6000] = '-Infinity','Infinity'

def convertBoard(boardState):
    state = dict()
    for i in range(0,8):
        for j in range(0,8):
            if boardState[i][j] == 'X':
                state[(i,j)] = 1
            elif boardState[i][j] == 'O':
                state[(i,j)] = -1
    return state

def readInput(filePath):
    player,depth = -1,0
    boardState = []
    with open(inputFilePath,'r') as f:
        lines = f.readlines()
        plyr = lines[0].strip()
        if plyr == 'X':
            player = 1
        depth = int(lines[1].strip())
        for i in range(2,10):
            boardState.append(list(lines[i]))
    state = convertBoard(boardState)
    return (player,depth,state)

def outputState(filePath,state):
    with open(filePath,'w') as doc:
        for i in range(0,8):
            line = ''
            for j in range(0,8):
                if (i,j) not in state:
                    line = line + '*'
                elif state[(i,j)] == 1:
                    line = line + 'X'
                elif state[(i,j)] == -1:
                    line = line + 'O'
            print line
            doc.write(line + '\n')
        
# piece location
#     1 2 3
#     4 X 5
#     6 7 8

def addToMoves(moves,i,j,direction):
    if (i,j) not in moves:
        moves[(i,j)] = [direction]
    else:
        moves[(i,j)].append(direction)
    return moves

def getMoves(player,state):
    moves = dict()
    for i in range(0,8):
        for j in range(0,8):
            if (i,j) not in state:
                if i+1<8 and j+1<8 and ((i+1,j+1) in state) and state[(i+1,j+1)] == player*-1:#location 1
                    p,q = i,j
                    while p+1<8 and q+1<8 and ((p+1,q+1) in state) and state[(p+1,q+1)] == player*-1:
                        p,q = p+1,q+1
                    if p+1<8 and q+1<8 and ((p+1,q+1) in state) and state[(p+1,q+1)] == player:
                        addToMoves(moves,i,j,1)
                if i+1<8 and ((i+1,j) in state) and state[(i+1,j)] == player*-1:#location 2
                    p,q = i,j
                    while p+1<8 and ((p+1,q) in state) and state[(p+1,q)] == player*-1:
                        p = p+1
                    if p+1<8 and ((p+1,q) in state) and state[(p+1,q)] == player:
                        addToMoves(moves,i,j,2)
                if i+1<8 and j-1>=0 and ((i+1,j-1) in state) and state[(i+1,j-1)] == player*-1:#location 3
                    p,q = i,j
                    while p+1<8 and q-1>=0 and ((p+1,q-1) in state) and state[(p+1,q-1)] == player*-1:
                        p,q = p+1,q-1
                    if p+1<8 and q-1>=0 and ((p+1,q-1) in state) and state[(p+1,q-1)] == player:
                        addToMoves(moves,i,j,3)
                if j+1<8 and ((i,j+1) in state) and state[(i,j+1)] == player*-1:#location 4
                    p,q = i,j
                    while q+1<8 and ((p,q+1) in state) and state[(p,q+1)] == player*-1:
                        q = q+1
                    if q+1<8 and ((p,q+1) in state) and state[(p,q+1)] == player:
                        addToMoves(moves,i,j,4)
                if j-1>=0 and ((i,j-1) in state) and state[(i,j-1)] == player*-1:#location 5
                    p,q = i,j
                    while q-1>=0 and ((p,q-1) in state) and state[(p,q-1)] == player*-1:
                        q = q-1
                    if q-1>=0 and ((p,q-1) in state) and state[(p,q-1)] == player:
                        addToMoves(moves,i,j,5)
                if i-1>=0 and j+1<8 and ((i-1,j+1) in state) and state[(i-1,j+1)] == player*-1:#location 6
                    p,q = i,j
                    while p-1>=0 and q+1<8 and ((p-1,q+1) in state) and state[(p-1,q+1)] == player*-1:
                        p,q = p-1,q+1
                    if p-1>=0 and q+1<8 and ((p-1,q+1) in state) and state[(p-1,q+1)] == player:
                        addToMoves(moves,i,j,6)
                if i-1>=0 and ((i-1,j) in state) and state[(i-1,j)] == player*-1:#location 7
                    p,q = i,j
                    while p-1>=0 and ((p-1,q) in state) and state[(p-1,q)] == player*-1:
                        p = p-1
                    if p-1>=0 and ((p-1,q) in state) and state[(p-1,q)] == player:
                        addToMoves(moves,i,j,7)
                if i-1>=0 and j-1>=0 and ((i-1,j-1) in state) and state[(i-1,j-1)] == player*-1:#location 8
                    p,q = i,j
                    while p-1>=0 and q-1>=0 and ((p-1,q-1) in state) and state[(p-1,q-1)] == player*-1:
                        p,q = p-1,q-1
                    if p-1>=0 and q-1>=0 and ((p-1,q-1) in state) and state[(p-1,q-1)] == player:
                        addToMoves(moves,i,j,8)
    return moves

def placePiece(player,move,directions,state):
    res = copy.copy(state)
    res[(move[0],move[1])] = player
    for direct in directions:
        i,j = move[0],move[1]
        if direct == 1:
            while i+1<8 and j+1<8 and ((i+1,j+1) in state) and state[(i+1,j+1)] == player*-1:
                    i,j = i+1,j+1
                    res[(i,j)] = player
        elif direct == 2:
            while i+1<8 and ((i+1,j) in state) and state[(i+1,j)] == player*-1:
                    i = i+1
                    res[(i,j)] = player
        elif direct == 3:
            while i+1<8 and j-1>=0 and ((i+1,j-1) in state) and state[(i+1,j-1)] == player*-1:
                    i,j = i+1,j-1
                    res[(i,j)] = player
        elif direct == 4:
            while j+1<8 and ((i,j+1) in state) and state[(i,j+1)] == player*-1:
                    j = j+1
                    res[(i,j)] = player
        elif direct == 5:
            while j-1>=0 and ((i,j-1) in state) and state[(i,j-1)] == player*-1:
                    j = j-1
                    res[(i,j)] = player
        elif direct == 6:
            while i-1>=0 and j+1<8 and ((i-1,j+1) in state) and state[(i-1,j+1)] == player*-1:
                    i,j = i-1,j+1
                    res[(i,j)] = player
        elif direct == 7:
            while i-1>=0 and ((i-1,j) in state) and state[(i-1,j)] == player*-1:
                    i = i-1
                    res[(i,j)] = player
        elif direct == 8:
            while i-1>=0 and j-1>=0 and ((i-1,j-1) in state) and state[(i-1,j-1)] == player*-1:
                    i,j = i-1,j-1
                    res[(i,j)] = player
    return res
    
weights = [[99,-8,8,6,6,8,-8,99],[-8,-24,-4,-3,-3,-4,-24,-8],[8,-4,7,4,4,7,-4,8],[6,-3,4,0,0,4,-3,6],
           [6,-3,4,0,0,4,-3,6],[8,-4,7,4,4,7,-4,8],[-8,-24,-4,-3,-3,-4,-24,-8],[99,-8,8,6,6,8,-8,99]]

def evaluateState(player,state):
    val = 0
    for pos,s in state.iteritems(): 
        val += s*weights[pos[0]][pos[1]]
    return val*player

def getLocation(move):
    col = ['a','b','c','d','e','f','g','h']
    return col[move[1]] + str(move[0]+1)

logs = []
pl = 1
def play(dad,node,player,depth,maxDepth,state,minmax,alpha,beta):
    val = minmax*-6000
    if depth == maxDepth:
        val = evaluateState(pl,state)
        logs.append(node+','+str(depth)+','+s[val]+','+s[alpha]+','+s[beta])
        return (val,state)
    res = copy.copy(state)
    moves = getMoves(player,state)
    if dad == 'pass' and len(moves) == 0:
        val = evaluateState(pl,state)
        logs.append(node+','+str(depth)+','+s[val]+','+s[alpha]+','+s[beta])
        return (val,state)
    logs.append(node+','+str(depth)+','+s[val]+','+s[alpha]+','+s[beta])
    if len(moves) == 0: ### Pass the move
        (result,st) = play(node,'pass',player*-1,depth+1,maxDepth,copy.copy(state),minmax*-1,alpha,beta)
        if minmax == 1:
            val = max(val,result)
            if val >= beta:
                logs.append(node+','+str(depth)+','+s[val]+','+s[alpha]+','+s[beta])
                return (val,res)
            alpha = max(alpha,val)
        elif minmax == -1:
            val = min(val,result)
            if val<= alpha:
                logs.append(node+','+str(depth)+','+s[val]+','+s[alpha]+','+s[beta])
                return (val,res)
            beta = min(beta,val)
        logs.append(node+','+str(depth)+','+s[val]+','+s[alpha]+','+s[beta])
    else:
        for move,directions in sorted(moves.iteritems()):
            cur = placePiece(player,move,directions,state)
            (result,st) = play(node,getLocation(move),player*-1,depth+1,maxDepth,copy.copy(cur),minmax*-1,alpha,beta)
            if minmax == 1:
                if val < result:
                    val,res = result, copy.copy(cur)
                if val >= beta:
                    logs.append(node+','+str(depth)+','+s[val]+','+s[alpha]+','+s[beta])
                    return (val,res)
                alpha = max(alpha,val)
            elif minmax == -1:
                if val > result:
                    val,res = result, copy.copy(cur)
                if val <= alpha:
                    logs.append(node+','+str(depth)+','+s[val]+','+s[alpha]+','+s[beta])
                    return (val,res)
                beta = min(beta,val)
            logs.append(node+','+str(depth)+','+s[val]+','+s[alpha]+','+s[beta])
    return (val,res)

(player, depth, state) = readInput(inputFilePath)
pl = player
(val,resState) = play('null','root',player,0,depth,state,1,-6000,6000)

outputState(outputFilePath,resState)
with open(outputFilePath,'a') as doc:
    doc.write('Node,Depth,Value,Alpha,Beta\n')
    for log in logs:
        doc.write(log+'\n')
