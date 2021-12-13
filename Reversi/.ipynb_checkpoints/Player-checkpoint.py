from random import choice
from Board import Board
import numpy as np

class Player:

    def check_valid_move(self,sub_board,current_player):
        directions = (
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        )
        
        #----------------get around chess step------------------
        sub_valid_moves_loc = []
        sub_valid_moves_loc.clear()
        
        
        non_zeros = np.argwhere(np.array(sub_board) != 0.0)
        

        for ele in non_zeros:
            non_zero_row = ele[0]
            non_zero_col = ele[1]

            for d in directions:
                this_row, this_col = non_zero_row + d[0], non_zero_col + d[1]
                if (
                    0 <= this_row < 8 and 0 <= this_col < 8
                    and sub_board[this_row][this_col] == 0
                    # and (this_row, this_col) not in self.__valid_moves_loc
                ):
                    sub_valid_moves_loc.append((this_row, this_col))
        
        sub_valid_moves_loc = set(sub_valid_moves_loc)
        
        #----------------get around chess step------------------
        
        
        #--------------get available move--------------------
        
        valid_moves = []

        for row, col in sub_valid_moves_loc:
            for idx, d in enumerate(directions):
                this_row, this_col = row + d[0], col + d[1]
                if (
                    0 <= this_row < 8 and 0 <= this_col < 8 
                    and sub_board[this_row][this_col] == -current_player
                ):
                    while True:
                        this_row += d[0]
                        this_col += d[1]
                        if 0 <= this_row < 8 and 0 <= this_col < 8:
                            if sub_board[this_row][this_col] == current_player:
                                valid_moves.append((row, col))
                                break
                            elif sub_board[this_row][this_col] == -current_player:
                                continue
                            else:
                                break
                        else:
                            break
        valid_moves = np.array(valid_moves)
        return valid_moves
        
    def chess(self,action,sub_board,current_player):
        
        directions = (
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        )
        
        #----------------get around chess step------------------
        sub_valid_moves_loc = []
        sub_valid_moves_loc.clear()
        
        row, col = action
        
        sub_board[row][col] = current_player
        
        non_zeros = np.argwhere(np.array(sub_board) != 0.0)
        

        for ele in non_zeros:
            non_zero_row = ele[0]
            non_zero_col = ele[1]

            for d in directions:
                this_row, this_col = non_zero_row + d[0], non_zero_col + d[1]
                if (
                    0 <= this_row < 8 and 0 <= this_col < 8
                    and sub_board[this_row][this_col] == 0
                    # and (this_row, this_col) not in self.__valid_moves_loc
                ):
                    sub_valid_moves_loc.append((this_row, this_col))
        
        sub_valid_moves_loc = set(sub_valid_moves_loc)
        
        #----------------get around chess step------------------
        
        
        #--------------get available move--------------------
        
        valid_moves = []

        for row, col in sub_valid_moves_loc:
            for idx, d in enumerate(directions):
                this_row, this_col = row + d[0], col + d[1]
                if (
                    0 <= this_row < 8 and 0 <= this_col < 8 
                    and sub_board[this_row][this_col] == -current_player
                ):
                    while True:
                        this_row += d[0]
                        this_col += d[1]
                        if 0 <= this_row < 8 and 0 <= this_col < 8:
                            if sub_board[this_row][this_col] == current_player:
                                valid_moves.append((row, col))
                                break
                            elif sub_board[this_row][this_col] == -current_player:
                                continue
                            else:
                                break
                        else:
                            break
        valid_moves = np.array(valid_moves)
        
        
        
        
        
        # return valid_moves
        
        #--------------get available move--------------------
        
    
        #--------------filp-------------------

        
        
        
        flip_d = []
        flip_d.clear()
        
        for d in directions:
            explot_row,explot_col = action
            while True:
                explot_row += d[0]
                explot_col += d[1]
                # print(d,explot_row,explot_col)
                if explot_row < 0 or explot_row >=8 or explot_col < 0 or explot_col >= 8 or sub_board[explot_row][explot_col] == 0:
                    break
                elif sub_board[explot_row][explot_col] == current_player:
                    
                    flip_d.append(d)
                elif sub_board[explot_row][explot_col] == -current_player:
                    continue
                    
        eat = 0
        for d in flip_d:
            this_row, this_col = action
            while True:
                this_row += d[0]
                this_col += d[1]

                if 0 <= this_row < 8 and 0 <= this_col < 8 :
                    if sub_board[this_row][this_col] == -current_player:
                        eat += 1
                        sub_board[this_row][this_col] = current_player
                    else:
                        break
                else:
                    break
            # self.__valid_moves[1] = self.compute_available_move(1)
            # self.__valid_moves[-1] = self.compute_available_move(-1)
        
        
        
        
        
        #--------------filp-------------------
        
        return valid_moves,sub_board,eat
            

    def move(self, board_inf):
        
        
        sub_board = [[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  1., -1.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                     [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]]
        
        # sub_valid_move,sub_board = self.chess([2,2],sub_board,-1) #sub_valid_moves_loc,sub_board,chose_player
        
#         # print(a,len(a),b)
#         print('\n')
#         for line in c:
#             print(line)
            
#         print('\n')
        
#         a,b,c = self.chess([4,5],sub_board,1) #sub_valid_moves_loc,sub_board,chose_player
        
#         # print(a,len(a),b)
#         print('\n')
#         for line in c:
#             print(line)
            
#         print('\n')
        
        
        # for i in range(5):
        #     print(board_inf[i])
        
    
    
        
        # Args:
        #     board_inf:
        #          [0] - valid_moves: 可以下的地方，它會是一個二維的 list ex:[[1,2],[2,2]]
        #          [1] - board_state: 當前棋盤狀況
        #          [2] - player_no  : 你先攻的話就是 1(O),反之 -1(X)
        #          [3] - total_step : 現在下到第幾步 (Hint: 對於黑白棋而言，解尾盤比較重要)
        # return:
        #     your moves: 你要下哪裡，它會是一個一維的 list ex:[1,2]
        
        weight = [
        [100,-10,50,40,40,50,-10,100],
        [-10,-20,20,10,10,20,-20,-10],
        [ 50, 20,40, 3, 3,40, 20, 50],
        [ 40, 10, 3, 0, 0, 3, 10, 40],
        [ 40, 10, 3, 0, 0, 3, 10, 40],
        [ 50, 20,40, 3, 3,40, 20, 50],
        [-10,-20,20,10,10,20,-20,-10],
        [100,-10,50,40,40,50,-10,100]
        ] 
        
#         print(self.check_valid_move(sub_board,1))
        
#         print(self.check_valid_move(sub_board,-1))

#         value = float('-inf')
#         answer = [weight[x][y] for (x,y) in board_inf[0]]
       
#         return board_inf[0][answer.index(max(answer))]


        def check_gold_corner(step):
            if (step[0] == 0 or step[0] == 7) and (step[1] == 0 or step[1] == 7):
                return step
            
            
            
        if board_inf[3] <= 57:
             # = [weight[x][y] for (x,y) in board_inf[0]]
            best_score = float('-inf')
            
            for frist_step in board_inf[0]:
                # score = weight[frist_step[0]][frist_step[1]]
                check_gold_corner(frist_step)
                sub_valid_move,sub_board,eat = self.chess(frist_step,board_inf[1],board_inf[2])
                sub_min = eat
                
                next_valid_move = self.check_valid_move(sub_board,-board_inf[2])
                for second_step in next_valid_move:
                    # score -= weight[second_step[0]][second_step[1]]
                    
                    sub_valid_move,sub_board,eat = self.chess(second_step,sub_board,-board_inf[2])
                    sub_max = eat
                    
                    next_valid_move = self.check_valid_move(sub_board,board_inf[2])
                    
                    for third_step in next_valid_move:
                        # score += weight[third_step[0]][third_step[1]]
                        sub_valid_move,sub_board,eat = self.chess(third_step,sub_board,board_inf[2])
                        sub_min += eat
                        if sub_min-sub_max > best_score:
                            best_score = sub_min-sub_max
                            global best_step
                            best_step = list(frist_step)
                            
            
            for val in board_inf[0]:
                if val[0] == best_step[0] and val[1] == best_step[1]:
                    print(best_step)
                    return best_step
            return board_inf[0][0]
                    
        else:
            print(board_inf[0][0])
            return board_inf[0][0]
        
        