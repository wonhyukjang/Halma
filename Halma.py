import copy
import heapq
import math

B_init = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3),
          (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)]

W_init = [(15, 15), (15, 14), (15, 13), (15, 12), (15, 11), (14, 15), (14, 14), (14, 13), (14, 12), (14, 11),
          (13, 15), (13, 14), (13, 13), (13, 12), (12, 15), (12, 14), (12, 13), (11, 14), (11, 15)]

weight_B = []

for i in range(16):
    dummy = []
    for j in range(16):
        dummy.append((i + j) * 30)
    weight_B.append(dummy)

for i in range(2):
    for j in range(5):
        weight_B[i][j] = 0
for i in range(1):
    for j in range(4):
        weight_B[i + 2][j] = 0
    for t in range(3):
        weight_B[i + 3][t] = 0
    for z in range(2):
        weight_B[i + 4][z] = 0
b_adjacent = [(5,0),(5,1),(4,2),(3,3),(2,4),(1,5),(0,5)]
w_adjacent = [(10,14),(10,15),(11,13),(12,12),(13,11),(14,10),(15,10)]

weight_W = [weight_B[::-1][i][::-1] for i in range(16)]

weight_B[10][15] = 720
weight_B[15][15] = 1000

for i in range(10):
    weight_B[15][i] = 0
for i in range(9):
    weight_B[14][i] = 0
for i in range(8):
    weight_B[13][i] = 0

for i in range(10):
    weight_B[i][15] = 0
for i in range(9):
    weight_B[i][14] = 0
for i in range(8):
    weight_B[i][13] = 0

weight_W[15][6] = 0
weight_W[15][10] = 0
weight_W[15][9] = 0
weight_W[15][8] = 0
weight_W[15][7] = 0

weight_W[6][1] = 0
weight_W[7][1] = 0
weight_W[8][1] = 0
weight_W[9][1] = 0
weight_W[10][1] = 0

weight_W[0][0] = 1000

for i in range(11):
    weight_W[i+5][0] = 0

for i in range(10):
    weight_W[i+6][1] = 0

for i in range(9):
    weight_W[i+7][2] = 0

for i in range(11):
    weight_W[0][i+5] = 0

for i in range(10):
    weight_W[1][i+6] = 0

for i in range(9):
    weight_W[2][i+7] = 0


def showBoard(board):
    for i in range(16):
        for j in range(16):
            if j == 15:
                print('{:>4s}'.format(str(board[i][j])))
            else:
                print('{:>4s}'.format(str(board[i][j])), end="")


class Board():
    def __init__(self, board, value, player):
        self.board = board
        self.value = value
        self.player = player


class Halma():
    # Create initial Min, Max value
    MIN_VALUE = -1231234245
    MAX_VALUE = 1231234245
    maxDepth = 100
    PRUNE = 0
    GAME = 0
    time_To_Return = 0
    done = 0
    OUT_INIT = 0
    FINISH = 0
    # save game Log
    game_Log = {"move": [], "evaluation": MIN_VALUE}

    def initial_State(self, board, player):
        if player == 'B':
            for i in range(2):
                for j in range(5):
                    if board[i][j] == 'B':
                        return True

            for i in range(4):
                if board[2][i] == 'B':
                    return True
            for i in range(3):
                if board[3][i] == 'B':
                    return True
            for i in range(2):
                if board[4][i] == 'B':
                    return True

        elif player == 'W':
            for i in range(2):
                for j in range(5):
                    if board[i + 14][j + 11] == 'W':
                        return True

            for i in range(4):
                if board[13][i + 12] == 'W':
                    return True
            for i in range(3):
                if board[12][i + 13] == 'W':
                    return True
            for i in range(2):
                if board[11][i + 14] == 'W':
                    return True
        return False

    def terminal_State(self, board, player):
        correct = 0
        if player == 'B':
            for i in range(2):
                for j in range(5):
                    if board[i + 14][j + 11] == 'B':
                        correct += 1

            for i in range(4):
                if board[13][i + 12] == 'B':
                    correct += 1
            for i in range(3):
                if board[12][i + 13] == 'B':
                    correct += 1
            for i in range(2):
                if board[11][i + 14] == 'B':
                    correct += 1

        elif player == 'W':
            for i in range(2):
                for j in range(5):
                    if board[i][j] == 'W':
                        correct += 1

            for i in range(4):
                if board[2][i] == 'W':
                    correct += 1
            for i in range(3):
                if board[3][i] == 'W':
                    correct += 1
            for i in range(2):
                if board[4][i] == 'W':
                    correct += 1
        if correct == 19:
            return True
        return False

    def score(self, board, player, target):
        correct = 0
        if player == 'B':
            for i in range(2):
                for j in range(5):
                    if board[i + 14][j + 11] == 'B':
                        correct += 1

            for i in range(4):
                if board[13][i + 12] == 'B':
                    correct += 1
            for i in range(3):
                if board[12][i + 13] == 'B':
                    correct += 1
            for i in range(2):
                if board[11][i + 14] == 'B':
                    correct += 1

        elif player == 'W':
            for i in range(2):
                for j in range(5):
                    if board[i][j] == 'W':
                        correct += 1

            for i in range(4):
                if board[2][i] == 'W':
                    correct += 1
            for i in range(3):
                if board[3][i] == 'W':
                    correct += 1
            for i in range(2):
                if board[4][i] == 'W':
                    correct += 1
        if correct == target:
            return True
        return False

    # Heuristic Function
    # Heuristic is calculated by their weight.
    # Thus, Heuristic(board) = all position of B's weight - all position of W's weight
    def evaluation(self, board, player):
        b_value = 0
        w_value = 0
        for i in range(16):
            for j in range(16):
                if board[i][j] == 'B':
                    b_value -= (15 - i)**2 + (15 - j)**2
                elif board[i][j] == 'W':
                    w_value -= i**2 + j**2
        return w_value - b_value if player == 'B' else b_value - w_value

    # Alpha-Beta Function
    def alphaBeta_Search(self, board, currentDepth, alpha, beta, player, times):
        if self.initial_State(board, player):
            moves = self.generateValidGrid(board, player, "max")
            max_value = moves[1][0]
            target_idx = 0
            for idx in range(1, len(moves[1])):
                if max_value <= moves[1][idx]:
                    max_value = moves[1][idx]
                    target_idx = idx
            player_Log = {'sequences': [moves[2][target_idx]]}
            return player_Log

        sequences = []
        v = self.maxValue(board, sequences, alpha, beta, currentDepth, player, times, 0)
        return v

    # Change player's turn
    def reversePlayer(self, player):
        if player == 'W':
            return 'B'
        else:
            return 'W'

    # Max-Value Function
    def maxValue(self, board, sequences, alpha, beta, currentDepth, player, times, cost):
        player_Log = {"eval": self.MIN_VALUE, 'sequences': sequences, "move": [], "previous": board, "alpha": alpha, "beta": beta}
        mode = "max"
        if self.terminal_State(board, player) or currentDepth == Halma.maxDepth:
            if self.terminal_State(board, player):
                Halma.done = 1
            player_Log['eval'] = self.evaluation(board, player) + cost
            player_Log['move'] = board
            player_Log['alpha'] = alpha
            player_Log['beta'] = beta
            self.game_Log['move'].append(player_Log)
            return player_Log

        movesPack = self.generateValidGrid(board, player, mode)
        moves = movesPack[0]
        cost = movesPack[1]
        seq = movesPack[2]

        for i in range(len(moves)):
            if self.terminal_State(moves[i], player):
                player_Log['eval'] = self.MAX_VALUE
                new_sequences = sequences.copy()
                new_sequences.append(seq[i])
                player_Log['sequences'] = new_sequences
                return player_Log

        v = self.MIN_VALUE

        # If no moves left, return minValue Function
        if len(moves) == 0:
            return player_Log

        for i in range(len(moves)):
            newMove = Board(moves[i], v, player)
            new_sequences = sequences.copy()
            new_sequences.append(seq[i])

            minLog = self.minValue(newMove.board, new_sequences, alpha, beta, currentDepth + 1, self.reversePlayer(player),
                                   times, cost[i])
            if player_Log['eval'] <= minLog['eval']:
                player_Log['eval'] = minLog['eval']
                player_Log['sequences'] = minLog['sequences']
                alpha = max(minLog['alpha'], player_Log['eval'])
                player_Log['alpha'] = alpha
                if alpha >= minLog['beta']:
                    break
                else:
                    player_Log['eval'] = minLog['eval']
                    player_Log['sequences'] = minLog['sequences']
                    player_Log['alpha'] = alpha

        return player_Log

    # Min-Value Function

    def minValue(self, board, sequences, alpha, beta, currentDepth, player, times, cost):
        player_Log = {"eval": self.MAX_VALUE, "sequences": sequences, "move": [], "previous": board, 'alpha': alpha, 'beta': beta}
        mode = "min"
        if self.terminal_State(board, player) or currentDepth == Halma.maxDepth:
            if self.terminal_State(board, player):
                Halma.done = 1
            player_Log['eval'] = self.evaluation(board, self.reversePlayer(player)) + cost
            player_Log['move'] = board
            self.game_Log['move'].append(player_Log)
            return player_Log

        movesPack = self.generateValidGrid(board, player, mode)
        moves = movesPack[0]
        cost = movesPack[1]
        seq = movesPack[2]

        for i in range(len(moves)):
            if self.terminal_State(moves[i], player):
                player_Log['eval'] = self.MIN_VALUE
                new_sequences = sequences.copy()
                new_sequences.append(seq[i])
                player_Log['sequences'] = new_sequences
                return player_Log

        v = 0
        if len(moves) == 0:
            return player_Log

        # Generate valid board
        for i in range(len(moves)):
            start = 1
            newMove = Board(moves[i], v, player)
            new_sequences = sequences.copy()
            new_sequences.append(seq[i])

            maxLog = self.maxValue(newMove.board, new_sequences, alpha, beta, currentDepth + 1, self.reversePlayer(player),
                                   times, cost[i])

            if player_Log['eval'] >= maxLog['eval']:
                player_Log['eval'] = maxLog['eval']
                player_Log['sequences'] = maxLog['sequences']
                beta = min(maxLog['beta'], player_Log['eval'])
                player_Log['beta'] = beta
                if beta <= maxLog['alpha']:
                    break
                else:
                    player_Log['eval'] = maxLog['eval']
                    player_Log['sequences'] = maxLog['sequences']
                    player_Log['beta'] = beta

        return player_Log

    def checkFirst(self, board, color):
        if color == 'W':
            for i in range(2):
                for j in range(5):
                    if board[i+14][j+11] == 'W':
                        return True
                    else:
                        continue

            for i in range(1):
                for j in range(4):
                    if board[i+13][j+12] == 'W':
                        return True
                    else:
                        continue
                for t in range(3):
                    if board[i+12][t+13] == 'W':
                        return True
                    else:
                        continue
                for z in range(2):
                    if board[i+11][z+14] == 'W':
                        return True
                    else:
                        continue
        if color == 'B':
            for i in range(2):
                for j in range(5):
                    if board[i][j] == 'B':
                        return True
                    else:
                        continue
            for i in range(1):
                for j in range(4):
                    if board[i + 2][j] == 'B':
                        return True
                    else:
                        continue
                for t in range(3):
                    if board[i + 3][t] == 'B':
                        return True
                    else:
                        continue
                for z in range(2):
                    if board[i + 4][z] == 'B':
                        return True
                    else:
                        continue
        return False

    def find(self, board, color):
        if color == 'B':
            for i in range(16):
                for j in range(16):
                    if board[i][j] == color:
                        if (i,j) not in W_init:
                            return (i,j)
                        else:
                            continue 
        elif color == 'W':
            for i in range(16):
                for j in range(16):
                    if board[i][j] == color:
                        if (i,j) not in B_init:
                            return (i,j)
                        else:
                            continue 
        return ()

    def lastPosition(self, board, color):
        if color == 'B':
            if self.score(board, color, 18):
                return self.find(board, color)
        elif color == 'W':
            if self.score(board, color, 18):
                return self.find(board, color)

                            
    def generateValidGrid(self, board, color, mode):
        validGrid = []
        flag = 0
        terminal_Flag = 0
        sequences = []
        output_Flag = 0
        finish_Flag = 0
        last_Flag = 0

        MAX_VALUE = 12345
        if self.checkFirst(board, color):
            flag = 1

        last_Position = self.lastPosition(board, color)
        
        for i in range(16):
            for j in range(16):
                visited = []
                if color == 'W':
                    idx1 = 15 - i
                    idx2 = 15 - j
                else:
                    idx1 = i
                    idx2 = j

                if last_Position != None:
                    if color == 'B':
                        if last_Position not in b_adjacent:
                            last_Flag = 1
                    else:
                        if last_Position not in w_adjacent:
                            last_Flag = 1
                    last_Flag = 1


                if board[idx1][idx2] == color:
                    count = 0
                    # One of the piece in initial state
                    if last_Flag  == 1:
                        if idx1 != last_Position[0] and idx2 != last_Position[1]:
                            continue
                    if flag == 0:
                        jumpList = []
                        skipCord = []
                        if self.goalPosition(idx1, idx2, color):
                            x_Pos, y_Pos = self.checkGoalInit(idx1, idx2, color)
                            terminal_Flag = 1
                        else:
                            if last_Flag != 1:
                                x_Pos, y_Pos = self.checkInit(idx1, idx2, color)
                            else:
                                x_Pos, y_Pos = self.checkLast(idx1,idx2,color)

                        for t in range(len(x_Pos)):
                            dummyX = idx1 + x_Pos[t]
                            dummyY = idx2 + y_Pos[t]
                            if self.checkValid(dummyX, dummyY, color):
                                if board[dummyX][dummyY] != '.':
                                    dummyX += x_Pos[t]
                                    dummyY += y_Pos[t]
                                    if self.checkValid(dummyX, dummyY, color):
                                        if board[dummyX][dummyY] == '.':
                                            if terminal_Flag == 1:
                                                if self.goalPosition(dummyX, dummyY, color) == False:
                                                    continue

                                            if (dummyX, dummyY) not in visited:
                                                visited.append((dummyX, dummyY))
                                            else:
                                                continue

                                            newBoard = copy.deepcopy(board)
                                            newBoard[dummyX][dummyY] = color
                                            newBoard[idx1][idx2] = '.'
                                            count += 1

                                            sequence = "J " + str(idx2) + "," + str(idx1) + " " + str(dummyY) + "," + str(
                                                dummyX)
                                            jumpList.append([dummyX, dummyY, sequence])
                                            skipCord.append([-1 * x_Pos[t], -1 * y_Pos[t]])
                                            sequences.append(sequence)
                                        else:
                                            continue
                                    else:
                                        continue
                                # Can move, but can't jump
                                else:
                                    if (dummyX, dummyY) not in visited:
                                        visited.append((dummyX, dummyY))
                                    else:
                                        continue

                                    newBoard = copy.deepcopy(board)
                                    newBoard[dummyX][dummyY] = color
                                    newBoard[idx1][idx2] = '.'
                                    count += 1
                                    sequence = 'E ' + str(idx2) + ',' + str(idx1) + ' ' + str(dummyY) + ',' + str(dummyX)
                                    sequences.append(sequence)
                            else:
                                continue

                            jumpCost = (abs(dummyX - idx1) + abs(dummyY - idx2))

                            if color[0] == 'B':
                                if dummyX - idx1 >= 0 or dummyY - idx2 >= 0:
                                    if finish_Flag == 0:
                                        if (dummyX, dummyY) in W_init:
                                            if (idx1, idx2) not in W_init:
                                                finish_Flag = 1
                                                validGrid = []
                                                jumpCost = self.MAX_VALUE
                                            else:
                                                jumpCost = -1
                                                if dummyY -1 == idx2 and dummyX +1 == idx1:
                                                    jumpCost = self.MAX_VALUE - 1000
                                                elif dummyY +1 == idx2 and dummyX - 1 == idx1:
                                                    jumpCost = self.MAX_VALUE - 1000                                            
                                    else:
                                        if (dummyX, dummyY) in W_init:
                                            if (idx1, idx2) not in W_init:
                                                jumpCost = self.MAX_VALUE
                                            else:
                                                continue
                                    if finish_Flag == 1:
                                        if (dummyX, dummyY) in W_init:
                                            if (idx1, idx2) not in W_init:
                                                heapq.heappush(validGrid, (
                                                    self.evaluation(newBoard, color) + jumpCost, jumpCost, count, newBoard, sequence))
                                            else:
                                                continue
                                        else:
                                            continue
                                    else:
                                        heapq.heappush(validGrid, (
                                            self.evaluation(newBoard, color) + jumpCost, jumpCost, count, newBoard, sequence))

                            if color[0] == 'W':
                                if dummyX - idx1 <= 0 or dummyY - idx2 <= 0:
                                    if finish_Flag == 0:                                        
                                        if (dummyX, dummyY) in B_init:
                                            if (idx1, idx2) not in B_init:
                                                finish_Flag = 1
                                                validGrid = []
                                                jumpCost = self.MAX_VALUE
                                            else:
                                                jumpCost = -1
                                                if dummyY -1 == idx2 and dummyX +1 == idx1:
                                                    jumpCost = self.MAX_VALUE - 1000
                                                elif dummyY +1 == idx2 and dummyX - 1 == idx1:
                                                    jumpCost = self.MAX_VALUE - 1000                                                
                                    else:                                        
                                        if (dummyX, dummyY) in B_init:
                                            if (idx1, idx2) not in B_init:
                                                jumpCost = self.MAX_VALUE
                                            else:
                                                continue                                
                                    if finish_Flag == 1:
                                        if (dummyX, dummyY) in B_init:
                                            if (idx1, idx2) not in B_init:
                                                heapq.heappush(validGrid, (
                                                    self.evaluation(newBoard, color) + jumpCost, jumpCost, count, newBoard, sequence))
                                            else:
                                                continue
                                        else:
                                            continue
                                    else:
                                        heapq.heappush(validGrid, (
                                            self.evaluation(newBoard, color) + jumpCost, jumpCost, count, newBoard, sequence))
                                        
                            while len(jumpList) > 0:
                                jumpList2 = []
                                skipCord2 = []
                                for q in range(len(jumpList)):
                                    if self.goalPosition(jumpList[q][0], jumpList[q][1], color):
                                        x, y = self.checkGoalInit(jumpList[q][0], jumpList[q][1], color)
                                        terminal_Flag = 1
                                    else:
                                        x, y = self.checkInit(jumpList[q][0], jumpList[q][1], color)
                                    cord = [[l, s] for l, s in zip(x, y)]
                                    cord = [x for x in cord if x != skipCord[q]]
                                    origin_seq = jumpList[q][2]
                                    for t in range(len(cord)):
                                        dummyX = jumpList[q][0] + cord[t][0]
                                        dummyY = jumpList[q][1] + cord[t][1]
                                        if self.checkValid(dummyX, dummyY, color):
                                            if board[dummyX][dummyY] != '.':
                                                dummyX += cord[t][0]
                                                dummyY += cord[t][1]
                                                if self.checkValid(dummyX, dummyY, color):
                                                    if board[dummyX][dummyY] == '.':
                                                        if terminal_Flag == 1:
                                                            if self.goalPosition(dummyX, dummyY, color) == False:
                                                                continue

                                                        if (dummyX, dummyY) not in visited:
                                                            visited.append((dummyX, dummyY))
                                                        else:
                                                            continue

                                                        newBoard = copy.deepcopy(board)
                                                        newBoard[dummyX][dummyY] = color
                                                        newBoard[idx1][idx2] = '.'
                                                        count += 1
                                                        for z in range(len(jumpList2)):
                                                            if jumpList2[z] == [dummyX, dummyY]:
                                                                if skipCord2[z] == [-1 * cord[t][0], -1 * cord[t][1]]:
                                                                    continue

                                                        j_seq = origin_seq + '\n'
                                                        j_seq += "J " + str(jumpList[q][1]) + "," + str(
                                                            jumpList[q][0]) + " " + str(
                                                            dummyY) + "," + str(dummyX)
                                                        jumpList2.append([dummyX, dummyY, j_seq])
                                                        skipCord2.append([-1 * cord[t][0], -1 * cord[t][1]])
                                                        jumpCost = (abs(dummyX - idx1) + abs(dummyY - idx2))

                                                        if color[0] == 'B':
                                                            if dummyX - idx1 >= 0 or dummyY - idx2 >= 0:
                                                                if finish_Flag == 0:
                                                                    if (dummyX, dummyY) in W_init:
                                                                        if (idx1, idx2) not in W_init:
                                                                            finish_Flag = 1
                                                                            validGrid = []
                                                                            jumpCost = self.MAX_VALUE
                                                                        else:
                                                                            jumpCost = -1
                                                                            if dummyY -1 == idx2 and dummyX +1 == idx1:
                                                                                jumpCost = self.MAX_VALUE - 1000
                                                                            elif dummyY +1 == idx2 and dummyX - 1 == idx1:
                                                                                jumpCost = self.MAX_VALUE - 1000                                            
                                                                else:
                                                                    if (dummyX, dummyY) in W_init:
                                                                        if (idx1, idx2) not in W_init:
                                                                            jumpCost = MAX_VALUE
                                                                        else:
                                                                            continue
                                                                if finish_Flag == 1:
                                                                    if (dummyX, dummyY) in W_init:
                                                                        if (idx1, idx2) not in W_init:
                                                                            heapq.heappush(validGrid, (
                                                                                self.evaluation(newBoard, color) + jumpCost, jumpCost, count,
                                                                                newBoard,
                                                                                j_seq))

                                                                        else:
                                                                            continue
                                                                    else:
                                                                        continue
                                                                else:
                                                                    heapq.heappush(validGrid, (
                                                                        self.evaluation(newBoard, color) + jumpCost, jumpCost, count,
                                                                        newBoard,
                                                                        j_seq))
                                                                    
                                                        if color[0] == 'W':
                                                            if dummyX - idx1 <= 0 or dummyY - idx2 <= 0:
                                                                if finish_Flag == 0:                                        
                                                                    if (dummyX, dummyY) in B_init:
                                                                        if (idx1, idx2) not in B_init:
                                                                            finish_Flag = 1
                                                                            validGrid = []
                                                                            jumpCost = self.MAX_VALUE
                                                                        else:
                                                                            jumpCost = -1
                                                                            if dummyY -1 == idx2 and dummyX +1 == idx1:
                                                                                jumpCost = self.MAX_VALUE - 1000
                                                                            elif dummyY +1 == idx2 and dummyX - 1 == idx1:
                                                                                jumpCost = self.MAX_VALUE - 1000                                                
                                                                else:                                        
                                                                    if (dummyX, dummyY) in B_init:
                                                                        if (idx1, idx2) not in B_init:
                                                                            jumpCost = self.MAX_VALUE
                                                                        else:
                                                                            continue                                
                                                                if finish_Flag == 1:
                                                                    if (dummyX, dummyY) in B_init:
                                                                        if (idx1, idx2) not in B_init:
                                                                            heapq.heappush(validGrid, (
                                                                                self.evaluation(newBoard, color) + jumpCost, jumpCost, count,
                                                                                newBoard,
                                                                                j_seq))
                                                                        else:
                                                                            continue
                                                                    else:
                                                                        continue
                                                                else:
                                                                    heapq.heappush(validGrid, (
                                                                        self.evaluation(newBoard, color) + jumpCost, jumpCost, count,
                                                                        newBoard,
                                                                        j_seq))
                                                    else:
                                                        continue
                                                else:
                                                    continue
                                            else:
                                                continue
                                        else:
                                            continue
                                jumpList = copy.deepcopy(jumpList2)
                                skipCord = copy.deepcopy(skipCord2)
                        terminal_Flag = 0

                    if flag == 1:
                        jumpList = []
                        skipCord = []

                        x_Pos, y_Pos = self.checkInit(idx1, idx2, color)

                        # If position in initial Position, only check move in initial position
                        if len(x_Pos) > 3:
                            continue


                        for t in range(len(x_Pos)):
                            dummyX = idx1 + x_Pos[t]
                            dummyY = idx2 + y_Pos[t]
                            # Check if we can get to position by jump

                            if self.checkValid(dummyX, dummyY, color):
                                if board[dummyX][dummyY] != '.':
                                    dummyX += x_Pos[t]
                                    dummyY += y_Pos[t]
                                    if self.checkValid(dummyX, dummyY, color):
                                        if board[dummyX][dummyY] == '.':

                                            if (dummyX, dummyY) not in visited:
                                                visited.append((dummyX, dummyY))
                                            else:
                                                continue

                                            if output_Flag == 0:
                                                if self.checkPosition(dummyX, dummyY, color) == False:
                                                    output_Flag = 1
                                                    validGrid = []
                                            newBoard = copy.deepcopy(board)
                                            newBoard[dummyX][dummyY] = color
                                            newBoard[idx1][idx2] = '.'
                                            count += 1

                                            sequence = "J " + str(idx2) + "," + str(idx1) + " " + str(dummyY) + "," + str(
                                                dummyX)
                                            jumpList.append([dummyX, dummyY, sequence])
                                            skipCord.append([-1 * x_Pos[t], -1 * y_Pos[t]])

                                        else:
                                            continue
                                    else:
                                        continue
                                # Can move, but can't jump
                                else:
                                    if output_Flag == 0:
                                        if self.checkPosition(dummyX, dummyY, color) == False:
                                            output_Flag = 1
                                            validGrid = []


                                    if (dummyX, dummyY) not in visited:
                                        visited.append((dummyX, dummyY))
                                    else:
                                        continue

                                    newBoard = copy.deepcopy(board)
                                    newBoard[dummyX][dummyY] = color
                                    newBoard[idx1][idx2] = '.'
                                    count += 1
                                    sequence = 'E ' + str(idx2) + ',' + str(idx1) + ' ' + str(dummyY) + ',' + str(dummyX)
                            else:
                                continue

                            jumpCost = (abs(dummyX - idx1) + abs(dummyY - idx2))
                            if color[0] == 'B':
                                if dummyX - idx1 >= 0 or dummyY - idx2 >= 0:
                                    if output_Flag == 1:
                                        if self.checkPosition(dummyX, dummyY, color) == False:
                                            heapq.heappush(validGrid, (
                                                self.evaluation(newBoard, color) + jumpCost, jumpCost, count, newBoard, sequence))
                                        else:
                                            continue
                                    else:
                                        heapq.heappush(validGrid, (
                                            self.evaluation(newBoard, color) + jumpCost, jumpCost, count, newBoard, sequence))

                            if color[0] == 'W':
                                if dummyX - idx1 <= 0 or dummyY - idx2 <= 0:
                                    if output_Flag == 1:
                                        if self.checkPosition(dummyX, dummyY, color) == False:
                                            heapq.heappush(validGrid, (
                                                self.evaluation(newBoard, color) + jumpCost, jumpCost, count, newBoard, sequence))
                                        else:
                                            continue
                                    else:
                                        heapq.heappush(validGrid, (
                                            self.evaluation(newBoard, color) + jumpCost, jumpCost, count, newBoard, sequence))

                            while len(jumpList) > 0:
                                jumpList2 = []
                                skipCord2 = []
                                for w in range(len(jumpList)):
                                    x, y = self.checkInit(jumpList[w][0], jumpList[w][1], color)

                                    cord = [[l, s] for l, s in zip(x, y)]
                                    cord = [x for x in cord if x != skipCord[w]]
                                    origin_seq = jumpList[w][2]
                                    for t in range(len(cord)):

                                        dummyX = jumpList[w][0] + cord[t][0]
                                        dummyY = jumpList[w][1] + cord[t][1]
                                        # Check if we can get to position by jump
                                        if self.checkValid(dummyX, dummyY, color):
                                            if board[dummyX][dummyY] != '.':
                                                dummyX += cord[t][0]
                                                dummyY += cord[t][1]
                                                if self.checkValid(dummyX, dummyY, color):
                                                    if board[dummyX][dummyY] == '.':

                                                        if (dummyX, dummyY) not in visited:
                                                            visited.append((dummyX, dummyY))
                                                        else:
                                                            continue
                                                        if output_Flag == 0:
                                                            if self.checkPosition(dummyX, dummyY, color) == False:
                                                                output_Flag = 1
                                                            validGrid = []

                                                        newBoard = copy.deepcopy(board)
                                                        newBoard[dummyX][dummyY] = color
                                                        newBoard[idx1][idx2] = '.'
                                                        count += 1
                                                        for v in range(len(jumpList2)):
                                                            if jumpList2[v] == [dummyX, dummyY]:
                                                                if skipCord2[v] == [-1 * cord[t][0], -1 * cord[t][1]]:
                                                                    continue

                                                        j_seq = origin_seq + '\n'
                                                        j_seq += "J " + str(jumpList[w][1]) + "," + str(
                                                            jumpList[w][0]) + " " + str(
                                                            dummyY) + "," + str(dummyX)
                                                        jumpList2.append([dummyX, dummyY, j_seq])
                                                        skipCord2.append([-1 * cord[t][0], -1 * cord[t][1]])
                                                        jumpCost = (abs(dummyX - idx1) + abs(dummyY - idx2))

                                                        if output_Flag == 1:
                                                            if self.checkPosition(dummyX, dummyY, color) == False:
                                                                heapq.heappush(validGrid, (
                                                                    self.evaluation(newBoard, color) + jumpCost, jumpCost, count,
                                                                    newBoard,
                                                                    j_seq))
                                                            else:
                                                                continue
                                                        else:
                                                            heapq.heappush(validGrid, (
                                                                self.evaluation(newBoard, color) + jumpCost, jumpCost, count,
                                                                newBoard,
                                                                j_seq))

                                                    else:
                                                        continue
                                                else:
                                                    continue
                                            else:
                                                continue
                                        else:
                                            continue
                                jumpList = copy.deepcopy(jumpList2)
                                skipCord = copy.deepcopy(skipCord2)
        heapq.heapify(validGrid)
        return ([[x[3] for x in validGrid], [x[1] for x in validGrid], [x[4] for x in validGrid]])



    def checkPosition(self, x, y, color):
        if color == 'B':
            if (x, y) in B_init:
                return True
            return False

        else:
            if (x, y) in W_init:
                return True
            return False

    def playHalma(self, board, alpha, beta, currentDepth, player, time):
        # showBoard(board)
        return self.alphaBeta_Search(board, 0, alpha, beta, player, time)

    # Check move is valid in the board
    def checkValid(self, dummyX, dummyY, color):
        if dummyX < 0 or dummyY < 0:
            return False
        if dummyX >= 16 or dummyY >= 16:
            return False
        return True

    def checkInit(self, x, y, color):
        if color == 'B':
            if self.checkPosition(x, y, color):
                return ([1, 1, 0], [1, 0, 1])
            else:
                return ([-1, 1, -1, 1, -1, 1, 0, 0], [-1, 1, 1, -1, 0, 0, -1, 1])
        elif color == 'W':
            if self.checkPosition(x, y, color):
                return ([-1, -1, 0], [-1, 0, -1])
            else:
                return ([-1, 1, -1, 1, -1, 1, 0, 0], [-1, 1, 1, -1, 0, 0, -1, 1])

    def checkLast(self, x, y, color):
        if color == 'B':
            return ([1,0,1], [1,1,0])
        elif color == 'W':
            return ([-1,-1,0],[-1,0,-1])
    def goalPosition(self, x, y, color):
        if color == 'B':
            if (x, y) in W_init:
                return True
            return False
        else:
            if (x, y) in B_init:
                return True
            return False

    def initPosition(self, x, y, color):
        if color == 'B':
            if (x, y) in B_init:
                return True
            return False
        else:
            if (x, y) in W_init:
                return True
            return False

    def checkGoalInit(self, x, y, color):
        x_Pos = [-1, 1, -1, 1, -1, 1, 0, 0]
        y_Pos = [-1, 1, 1, -1, 0, 0, -1, 1]

        x_Valid_Pos = []
        y_Valid_Pos = []

        if color == 'B':
            if self.goalPosition(x, y, color):
                for b, c in zip(x_Pos, y_Pos):
                    if self.goalPosition(x + b, y + c, color):
                        x_Valid_Pos.append(b)
                        y_Valid_Pos.append(c)
                return ([int(x) for x in x_Valid_Pos], [int(y) for y in y_Valid_Pos])
            else:
                return ([-1, 1, -1, 1, -1, 1, 0, 0], [-1, 1, 1, -1, 0, 0, -1, 1])

        elif color == 'W':
            if self.goalPosition(x, y, color):
                for b, c in zip(x_Pos, y_Pos):
                    if self.goalPosition(x + b, y + c, color):
                        x_Valid_Pos.append(b)
                        y_Valid_Pos.append(c)
                return ([int(x) for x in x_Valid_Pos], [int(y) for y in y_Valid_Pos])
            else:
                return ([-1, 1, -1, 1, -1, 1, 0, 0], [-1, 1, 1, -1, 0, 0, -1, 1])



    def main(self):
        import time

        start = time.monotonic()

        # Read Input from txt file
        f = open("input.txt", 'r')

        # Check the mode
        mode = f.readline().rstrip()

        # Check who start first
        color = f.readline().rstrip()

        # Check length of the game
        time = float(f.readline().rstrip())


        # Read initial position of the game
        board = []

        for i in range(16):
            board.append([x for x in f.readline().rstrip()])

        # Play Halma
        self.maxDepth = 10
        if time >= 200:
            self.maxDepth = 50
        elif time>=50 and time < 100:
            self.maxDepth = 30
        elif time>=25 and time < 50:
            self.maxDepth = 10

        result = self.playHalma(board, self.MIN_VALUE, self.MAX_VALUE, 0, color[0], time)
        # print(result)
        f = open('output.txt', 'w')
        print(result['sequences'][0], end="", file=f)
        f.close()

halma = Halma()
halma.main()
