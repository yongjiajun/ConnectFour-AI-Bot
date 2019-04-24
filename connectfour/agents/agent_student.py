from connectfour.agents.computer_player import RandomAgent
from connectfour.agents.agent import Agent
import random

class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 1


    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """

        valid_moves = board.valid_moves() #是一个generator，生成有效的点，col从0到6
        vals = [] #分别两个List
        moves = []

        for move in valid_moves: 
            # id就是1或2; move就是(5,1)typle指定哪个点; move[0]就是指5，move[1]就是指1

            next_state = board.next_state(self.id, move[1]) #就是假设move[1]放进去了之后的Board对象
            #print("next_state.board: "+str(next_state.board))
            moves.append( move ) #moves就是收集从第0行到第6行可以出现在棋盘上可添加的步数
            # print (move)
            #print("move[0]: "+str(move[0])+", move[1]: "+str(move[1]))
            a=self.dfMiniMax(next_state, 1) #计算概率的，Mini Max
            #print (a)
            vals.append( a ) #可能是搜集各个点的概率,每次的str(self.dfMiniMax(next_state, 1))值都不同
            #print (a)
            
            #print (self.dfMiniMax(next_state, 1))
            #print (vals)
            # print(board.next_state(2, move[1]).board)
            # print(board.next_state(2, move[1]).last_move)
            # print(board.last_move)
            
            
        
        # print(vals)
        # print(max(vals))
        bestMove = moves[vals.index( max(vals) )] #最大概率点，所对的index也就是柱，对用到moves里面的具体步法
        # print (vals.index( max(vals)))
        print ("best move is: " + str(bestMove))
        # print(board.board)

        # if (self.id == 1):
        #     isplayerone = True
        # else:
        #     isplayerone = False
        # board.update_scores(bestMove[1],abs(bestMove[0]-5),self.id,isplayerone) #如果走了bestMove的update
        
        # print(board.score_array)

        print ()

        return bestMove





    def dfMiniMax(self, board, depth): #利用递归的算法计算出所有步骤所对的分数，此方法要研究
        # Goal return column with maximized scores of all possible next states
        
        if depth == self.MaxDepth: #目前全都是走这一步
            #print (1)
            #print(depth)
            

            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])#
            else:
                next_state = board.next_state(self.id, move[1])
                
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, depth + 1) )

        
        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal





    def evaluateBoardState(self, board): #已经是一个合法的board了
        """
        Your evaluation function should look at the current state and return a score for it. 
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """
        
        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width     7
            board.height    6
            board.last_move
            board.num_to_connect
            board.winning_zones ？可能不需要用到
            board.score_array ？
            board.current_player_score ？

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """

        p1 = self.check_score(board,self.id)
        p2 = self.check_score(board,self.id%2+1)

        print (p1)
        print (p2)
        
        if((p1+p2) != 0):
            return p1/(p1+p2)
        elif ((p1+p2) == 0 and p1 == 0):
            return 0
        else:
            return 0.5



    def check_score(self, board, id):
        score = 0
        #Check center pieces
        center_piece = []
        for row in range(board.height):
            # print(str(row)+" : "+str(board.width))
            center_piece.append(board.get_cell_value(row,board.width//2))
        
        score += 3 * center_piece.count(id)

        #Check how many Horizontally
        for row in range(board.height):
            for col in range(board.width - 3):
                connect = [board.get_cell_value(row, col+i) for i in range(board.num_to_connect)]
                #[0,1,0,2]
                score += self.check_connect(connect,id) 
        # print (score)
        
        #Check how many Vertically
        for col in range(board.width):
            for row in range(board.height - 3):
                connect = [board.get_cell_value(row+i, col) for i in range(board.num_to_connect)]
                score += self.check_connect(connect,id)
        
        #Check how many up diagonal
        for row in range(board.height - 3):
            for col in range(board.width - 3):
                connect = [board.get_cell_value(row + 3 - i, col+i) for i in range(board.num_to_connect)]
                score += self.check_connect(connect,id)
              
        #Check how many down diagonal
        for row in range(board.height - 3):
            for col in range(board.width - 3):
                connect = [board.get_cell_value(row+i, col+i) for i in range(board.num_to_connect)]
                score += self.check_connect(connect,id)

        return score
    
    def check_connect(self,connect,id):
        score = 0
        
        if connect.count(id) == 4:
            score += 100
        elif connect.count(id) == 3 and connect.count(0) == 1:
            score += 10
        elif connect.count(id) == 2 and connect.count(0) == 2:
            score += 5
        elif connect.count(id) == 1 and connect.count(0) == 2:
            score += 1
            

        return score






