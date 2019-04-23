'''
Zachary Chuba
10 December 2018
CS 100 H01
Tictactoe AI
'''
triplets = ((0, 4, 8), (2, 4, 6),                 # these are diagonals
                (0, 1, 2), (3, 4, 5), (6, 7, 8),  # these are rows
                (0, 3, 6), (1, 4, 7), (2, 5, 8))  # these are columns

def __isDraw(board): #From the ttt Class
    '''return True if the game is a draw,
    else return False'''
    draw = True
    for triplet in triplets:
        xCount = oCount = 0
        for index in triplet:
            xCount += board[index].count('X')
            oCount += board[index].count('O')
        if xCount == 0 or oCount == 0:
            draw = False
            break
    return draw
    
def testMove(board, position, side):
    '''
    Returns board with a given side added at a given index
    Is also used to reverse prior test cases (accepts '-' input)
    '''
    board.insert(position, side)
    board.pop(position+1)
    return board
    
def moveValue(board):
        '''
        Given a board returns a value of board
        - if favorable to x, + if favorable o
        If magnitude is greater, it is more favorable
        '''
        
        totalValue = 0
        for triplet in triplets:
            numX = 0
            numO = 0
            for i in range(3):
                if board[triplet[i]] == 'X':
                    numX += 1
                elif board[triplet[i]] == 'O':
                    numO += 1
            if numX == numO == 0:
                totalValue += 1 #it is winnable
            if numX == 1 and numO == 0:
                totalValue -= 5 
            if numX == 2 and numO == 0:
                totalValue -= 10
            if numX == 3:
                totalValue = -10000
                break
            if numO == 1 and numX == 0:
                totalValue += 5 
            if numO == 2 and numX == 0:
                totalValue += 10
            if numO == 3:
                totalValue = 10000
                break
            if numO > 0 and numX > 0:
                totalValue += 0 #blocked -> no change
        return totalValue
        
def __winner(board): #from the ttt Class
    '''return 'X' if X won, 'O' if O won, else '-' '''
    for triplet in triplets:
        if board[triplet[0]] == board[triplet[1]] == board[triplet[2]] != '-':
            return board[triplet[0]]
    return '-'
    

def gameOver(board):
    '''
    Returns if the game is over or not, given board
    '''
    return __isDraw(board) or __winner(board) != '-'

def aiSolution(board, player, maxDepth = 9, _depth = 0, _initBoard = None):
    '''
    Returns tuple(A static choice of the AI's move, and a list of tuples
    of all equivalent moves and values)
    Params:
    Board - ttt board
    Player - the player whose turn it is
    [maxDepth] - how thorough / perfect you want the ai to be 1<=maxDepth<=9
    [_depth] non interface variable -- do not change!
    [_initBoard] non interface variable -- do not change!
    '''
    
    if _initBoard == None: #saving the initial board in case it fails the still playable condition, so it can give valid return
        _initBoard = board
        
    if gameOver(_initBoard): #passing already completed board the first time
        boardValue = moveValue(board)
        bestMoves = playableMoves(_initBoard)
        newBestMoves = []
        for move in bestMoves: #making best moves a tuple -- this only matters for invalid inputs (like an already won game)
            newBestMoves.append((move, None))
        return [-1, boardValue], newBestMoves

    legalMoves = playableMoves(board)
    if player == 'X':
        bestMove = [-1, 10000] #No position, defaults to worst possible outcome
        bestMoves = []
    else:
        bestMove = [-1, -10000]#No position, defaults to worst possible outcome
        bestMoves = []
    if gameOver(board) or _depth == maxDepth: #Stop at this point
        boardValue = moveValue(board)
        return [-1, boardValue] #No position assigned, defaults to the value at that time
        
    
    for legalMove in legalMoves:
        #I did not use a copy board because it loses depth the way I coded it
        #Instead I reverted changes
        board = testMove(board, legalMove, whoseTurn(board))
        move = aiSolution(board, whoseTurn(board), maxDepth, _depth+1, _initBoard)
        if 'tuple' in str(type(move)): #catches miss-matching return statement
            move = move[0]
        board = testMove(board, legalMove, '-')
        move.insert(0, legalMove)
        move.pop(1)
        if player == 'X':
            if move[1] <= bestMove[1]: #So I can randomly select
                if move[1] < bestMove[1]: #In case there is a better move
                    bestMove = [move[0], move[1]]
                if len(bestMoves) > 0 and bestMoves[-1][1] > bestMove[1]: #No longer the best moves
                    bestMoves = []
                bestMoves.append((move[0], move[1]))
        else:
            if move[1] >= bestMove[1]: #So I can randomly select
                if move[1] > bestMove[1]: #In case there is a better move
                    bestMove = [move[0], move[1]]
                if len(bestMoves) > 0 and bestMoves[-1][1] < bestMove[1]: #No longer the best moves
                    bestMoves = []
                bestMoves.append((move[0], move[1]))
    
    return bestMove, bestMoves
    
def chooseRandomBestSolution(bestMoves):
    import random
    
    newList = []
    for moveAndValue in bestMoves:
        newList.append(moveAndValue[0])
    
    return newList[random.randint(0,len(newList)-1)]


def whoseTurn(board):
        '''
        Given a board, returns 'X' if X plays next, else 'O'
        Following rules of ttt
        '''
        if board.count('X') == board.count('O') or board.count('-') == 9:
            return 'X'
        else:
            return 'O'

def playableMoves(board):
    '''
    Returns a list of all the indexes of the tictactoe board with an empty space
    '''
    openSpaces = []
    for i in range(len(board)):
        if board[i] == '-':
            openSpaces.append(i)
    return openSpaces

def checkVariousCases():
    boards = [['O', '-', 'X', 'X', '-', 'O', 'X', 'O', 'X'], #expected output = 4
              ['-', '-', '-', '-', 'X', '-', '-', '-', '-'], #expected output = a corner
              ['O', 'X', '-', '-', 'O', 'X', 'X', '-', '-'], #expected output = 8
              ['X', '-', 'O', 'X', 'X', '-', 'O', '-', '-'], #expected output 1, 5, 7, 8
              ['X', 'X', 'X', 'O', 'O', '-' ,'O', '-', '-'], #any open spot output expected; game already over
              ['-', '-', '-', '-', '-', '-', '-', '-', '-'], #any output expected -- no matter what draw if depth >= 8
              ['X', 'O', 'O', 'O', 'X', '-', 'X', '-', '-']] #expected output = 8
              
    boardsDepth1 = [['-', '-', '-', '-', '-', '-', '-', '-', '-'], #expected output = 4
                    ['O', '-', 'X', 'X', '-', 'O', 'X', 'O', 'X'], #expected output = 4
                    ['X', 'X', 'X', 'O', 'O', '-' ,'O', '-', '-'], #expected output = any open spot game already over
                    ['-', '-', 'X', '-', 'X', '-', '-', '-', 'O']] #expected output = 6
    outPut9 = ['4', '0268', '8', '1578', '578', '012345678', '8']
    outPut1 = ['4', '4', '578', '6']
    for i in range(len(boards)):
        board = boards[i]
        value = aiSolution(board, whoseTurn(board))
        value = chooseRandomBestSolution(value[1])
        if str(value) in outPut9[i]:
            print('{} passed'.format(board))
            continue
        else:
            print('{} failed'.format(board))
            print('{}'.format(value))
            break
    for i in range(len(boardsDepth1)):
        board = boardsDepth1[i]
        value = aiSolution(board, whoseTurn(board), 1)
        value = chooseRandomBestSolution(value[1])
        if str(value) in outPut1[i]:
            print('{} passed'.format(board))
            continue
        else:
            print('{} failed'.format(board))
            print('{}'.format(value))
            break

def playThroughGame():
    boards = [['-', '-', '-', '-', '-', '-', '-', '-', '-'], #empty board
             ['O', '-', 'X', 'X', '-', 'O', 'X', 'O', 'X']]  #1 condition to not lose
    #Should draw 100% of the time
    for board in boards:
        while len(playableMoves(board)) > 0:
            value = chooseRandomBestSolution(aiSolution(board, whoseTurn(board))[1])
            print(whoseTurn(board) + ' plays position ' + str(value), end = ', ')
            board[value] = whoseTurn(board)
        result = __winner(board) if __winner(board) != '-' else 'nobody'
        print('\nResult ' + result + ' wins')


checkVariousCases()
playThroughGame()

#board = ['-', '-', '-', '-', 'X', '-', '-', '-', '-'] 
#value = aiSolution(board, whoseTurn(board))
#print(aiSolution(board, whoseTurn(board)))
#print(chooseRandomBestSolution(value[1]))
