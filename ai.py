class Frontier():
    def __init__(self):
        self.frontier = []


    def newFrontier(self,state):
        self.frontier.append(state)

    def giveFrontier(self):
        return self.frontier[len(self.frontier)-1]

class TicTacToe():
    def __init__(self,initialturn):
        self.initialturn = bool(initialturn)
        self.sol = dict()
        self.frontier = Frontier()
        self.initialstate = [[' ','#',' ','#',' '],['#','#','#','#','#'],[' ','#',' ','#',' '],['#','#','#','#','#'],[' ','#',' ','#',' ']]
        self.height = len(self.initialstate)
        self.width = max(len(value) for value in self.initialstate)



    def printboard(self,state):

        for i in range(self.height):
            for j in range(self.width):
                try:
                    if state[i][j] == '#':
                        if i%2 != 0:
                            print('-',end='')
                        else:
                            print('|',end='')
                    else:
                        print(state[i][j], end='')
                except IndexError:
                    print(" ",end='')
            print()
        print()

    def player(self,state):
        countx = 0
        counto = 0
        for i in range(self.height):
            for j in range(self.width):
                if state[i][j] == 'X':
                    countx +=1
                elif state[i][j] == 'O':
                    counto+=1
        if countx > counto:
            return 0
        elif countx == counto:
            if self.initialturn == False:
                return 0
            else:
                return 1
        else:
            return 1

    def actions(self,state):
        actions = []
        for i in range(self.height):
            for j in range(self.width):
                if state[i][j] == ' ':
                    actions.append((i,j))
        return actions


    def result(self,state,action):
        if self.player(state) == 0:
            state[action[0]][action[1]] = "O"
        elif self.player(state) == 1:
            state[action[0]][action[1]] = 'X'

        return state


    def terminal(self,state):

        # Checking for the row

        for i in range(self.height):
            countx = 0
            counto = 0
            for j in range(self.width):
                if state[i][j] == 'X':
                    countx += 1
                elif state[i][j] == 'O':
                    counto += 1
            if countx == 3 or counto == 3:
                return True

        # Checking for the column

        for i in range(self.height):
            countx = 0
            counto = 0
            for j in range(self.width):
                if state[j][i] == "X":
                    countx += 1
                elif state[j][i] == "O":
                    counto += 1
            if countx == 3 or counto == 3:
                return True

        # checking for top left to bottom right
        if (state[0][0] == 'X' and state[2][2] == 'X' and state[4][4] == 'X') or (state[0][0] == 'O' and state[2][2] == 'O' and state[4][4] == 'O'):
            return True

        # checking for top right to bottom left daigonal

        if (state[4][0] == 'X' and state[2][2] == 'X' and state[0][4] == 'X') or (state[4][0] == 'O' and state[2][2] == 'O' and state[0][4] == 'O'):
            return True


        # checking that all the feild are filled or not

        countspace = 0
        for i in range(self.height):
            for j in range(self.width):
                if state[i][j] == ' ':
                    countspace += 1
        if countspace == 0:
            return True


        return False

    def utility(self,state):

        # Checking for the row

        for i in range(self.height):
            countx = 0
            counto = 0
            for j in range(self.width):
                if state[i][j] == 'X':
                    countx += 1
                elif state[i][j] == 'O':
                    counto += 1
            if countx == 3:
                return 1
            elif counto == 3:
                return -1

        # Checking for the column

        for i in range(self.height):
            countx = 0
            counto = 0
            for j in range(self.width):
                if state[j][i] == "X":
                    countx += 1
                elif state[j][i] == "O":
                    counto += 1
            if countx == 3:
                return 1
            elif counto == 3:
                return -1

        # checking for top left to bottom right
        if state[0][0] == 'X' and state[2][2] == 'X' and state[4][4] == 'X':
            return 1
        elif state[0][0] == 'O' and state[2][2] == 'O' and state[4][4] == 'O':
            return -1


        # checking for top right to bottom left daigonal

        if state[4][0] == 'X' and state[2][2] == 'X' and state[0][4] == 'X':
            return 1
        elif state[4][0] == 'O' and state[2][2] == 'O' and state[0][4] == 'O':
            return -1


        return 0

    def playerturn(self,state):
        userinput = input('Your turn :- ')
        useraction = (int(userinput[0]),int(userinput[2]))
        if not isinstance(useraction,tuple):
            print('Please provide valid input as row,column')
        else:
            return self.result(state,useraction)





    def aiturn(self):
        state = self.frontier.giveFrontier().copy()
        minvalue = 10000
        bestaction = None
        for action in self.actions(state):
            board = self.result(self.frontier.giveFrontier(),action)
            value =  self.minimax(board,True)
            board[action[0]][action[1]] = " "
            if value < minvalue:
                minvalue = value
                bestaction = action

        self.frontier.newFrontier(self.result(self.frontier.giveFrontier(),bestaction))

    def minimax(self,board,ismax):
        if self.terminal(board):
            return self.utility(board)

        if ismax:
            v = -10000
            for action in self.actions(board):
                v = max(v,self.minimax(self.result(board,action),False))
                board[action[0]][action[1]] = ' '
            return v
        elif not ismax:
            v = 10000
            for action in self.actions(board):
                v = min(v,self.minimax(self.result(board,action),True))
                board[action[0]][action[1]] = ' '
            return v

    def startgame(self):
        self.frontier.newFrontier(self.initialstate)
        while self.terminal(self.frontier.giveFrontier()) == False:
            if self.player(self.frontier.giveFrontier()) == 1:
                self.frontier.newFrontier(self.playerturn(self.frontier.giveFrontier()))
                self.printboard(self.frontier.giveFrontier())

            elif self.player(self.frontier.giveFrontier()) == 0:
                self.aiturn()
                self.printboard(self.frontier.giveFrontier())

print()
print('Welcome to the TicTacToe Game ')
print()
print("You are going to be (X) player and AI going to be (O) player ")
print()
print("You have to select the positon where you want to play by providing row and column")
print("row start from 0,2,4 and column always be either 0,2,4")
print()
print('please select turn :- press 1 for your initial turn and press 0 for ai initial turn')
initialturn = int(input("Ans :- "))
tictactoe = TicTacToe(initialturn)
tictactoe.startgame()











