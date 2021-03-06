from random import choice
import numpy as np

def empty_position( board_state):
    board_state = np.array( board_state)
    valid_moves_loc = []
    directions = ( ( -1, -1), ( -1, 0), ( -1, 1), ( 0, -1), ( 0, 1), ( 1, -1), ( 1, 0), ( 1, 1))
    non_zeros = np.argwhere( board_state != 0)

    for ele in non_zeros:
        row = ele[ 0]
        col = ele[ 1]

        for direction in directions:
            this_row, this_col = row + direction[ 0], col + direction[ 1]

            if ( 0 <= this_row < 8 and 0 <= this_col < 8
               and board_state[ this_row][ this_col] == 0
               and ( this_row, this_col) not in valid_moves_loc):
                valid_moves_loc.append( ( this_row, this_col))
    return valid_moves_loc

def compute_available_move( board_state, empty_list, specific_player):
        valid_moves = []
        directions = ( ( -1, -1), ( -1, 0), ( -1, 1), ( 0, -1), ( 0, 1), ( 1, -1), ( 1, 0), ( 1, 1))

        for ( row, col) in empty_list:

            for idx, direction in enumerate( directions):
                this_row, this_col = row + direction[ 0], col + direction[ 1]

                if ( 0 <= this_row < 8 and 0 <= this_col < 8
                     and board_state[ this_row][ this_col] == -specific_player):

                     while True:
                        this_row += direction[ 0]
                        this_col += direction[ 1]

                        if 0 <= this_row < 8 and 0 <= this_col < 8:

                            if board_state[ this_row][ this_col] == specific_player:
                                valid_moves.append( ( row, col, idx))
                                break

                            elif board_state[ this_row][ this_col] == -specific_player:
                                continue

                            else:
                                break

                        else:
                            break

        valid_moves = np.array( valid_moves)
        return valid_moves

def flip_direction( board_state, cheer_row, cheer_col, player):
    directions = ( ( -1, -1), ( -1, 0), ( -1, 1), ( 0, -1), ( 0, 1), ( 1, -1), ( 1, 0), ( 1, 1))
    explore_direction = []

    for direction in directions:
        row = cheer_row
        col = cheer_col

        while True:
            row += direction[ 0]
            col += direction[ 1]

            if 0 <= row < 8 and 0 <= col < 8:

                if board_state[ row][ col] == -player:
                    continue

                elif board_state[ row][ col] != 0:
                    explore_direction.append( direction)
                    break

                else:
                    break

            else:
                break

    return explore_direction


class Player:
    def __init__(self):
        self.name = "Player"

    def move( self, board_inf):
        """
        Args:
            board_inf:
                 [0] - valid_moves: ????????????????????????????????????????????? list ex:[[1,2],[2,2]]
                 [1] - board_state: ??????????????????
                 [2] - player_no  : ????????????????????? 1(O),?????? -1(X)
                 [3] - total_step : ????????????????????? (Hint: ?????????????????????????????????????????????)
        return:
            your moves: ?????????????????????????????????????????? list ex:[1,2]
        """
        # print( board_inf[ 1])
        max_weights = [ [ 100, -50, 50, 40, 40, 50, -50, 100],
                        [ -50, -80, 50,  5,  5, 50, -80, -50],
                        [  50,  50, 60,  3,  3, 60,  50,  50],
                        [  40,   5,  3,  0,  0,  3,   5,  40],
                        [  40,   5,  3,  0,  0,  3,   5,  40],
                        [  50,  50, 50,  3,  3, 60,  50,  50],
                        [ -50, -80, 60,  5,  5, 50, -80, -50],
                        [ 100, -50, 50, 40, 40, 50, -50, 100]]

        best_score = float( "-inf")

        # ????????????????????????????????? ??? ???????????????????????? and ??????????????????
        valid_position_loc = empty_position( board_state= board_inf[ 1])
        valid_position = { player: compute_available_move( board_state= board_inf[ 1], empty_list= valid_position_loc, specific_player= player) for player in [ -1, 1]}

        if board_inf[ 3] < 58:
            for empty_ind, empty_col, _ in valid_position[ board_inf[ 2]]:
                now_board = board_inf[ 1].copy()

                # ???????????? ( empty_ind, empty_col) ??????
                now_board[ empty_ind][ empty_col] = board_inf[ 2]

                # ?????????????????????????????????????????????
                # ???????????????????????????
                flip_direction_list = flip_direction( board_state= now_board, cheer_row= empty_ind, cheer_col= empty_col, player= board_inf[ 2])

                # ???????????????????????????
                for diretion in flip_direction_list:
                    this_row, this_col = empty_ind, empty_col

                    while True:
                        this_row += diretion[ 0]
                        this_col += diretion[ 1]

                        if 0 <= this_row < 8 and 0 <= this_col < 8:
                            if now_board[ this_row][ this_col] == -board_inf[ 2]:
                                now_board[ this_row][ this_col] = board_inf[ 2]
                            else:
                                break
                        else:
                            break

                # ???????????????????????????
                layer_1 = max_weights[ empty_ind][ empty_col]

                ## ?????? human ???????????? ????????????????????? ??? ???????????????????????? and ??????????????????
                valid_position_loc_ai = empty_position( board_state= now_board)
                valid_position_ai = { player: compute_available_move( board_state= now_board, empty_list= valid_position_loc_ai, specific_player= player) for player in [ -1, 1]}

                for ai_empty_ind, ai_empty_col, _ in valid_position_ai[ -board_inf[ 2]]:
                    # ?????? ai ?????? ( ai_empty_ind, ai_empty_col) ??????
                    now_board[ ai_empty_ind][ ai_empty_col] = -board_inf[ 2]

                    # ?????????????????????????????????????????????
                    # ???????????????????????????
                    flip_direction_list = flip_direction( board_state= now_board, cheer_row= ai_empty_ind, cheer_col= ai_empty_col, player= -board_inf[ 2])

                    # ???????????????????????????
                    for diretion in flip_direction_list:
                        this_row, this_col = empty_ind, empty_col

                        while True:
                            this_row += diretion[ 0]
                            this_col += diretion[ 1]

                            if 0 <= this_row < 8 and 0 <= this_col < 8:
                                if now_board[ this_row][ this_col] == board_inf[ 2]:
                                    now_board[ this_row][ this_col] = -board_inf[ 2]
                                else:
                                    break
                            else:
                                break

                    ## ?????? ai ???????????? ????????????????????? ??? ???????????????????????? and ??????????????????
                    valid_position_loc_hm = empty_position( board_state= now_board)
                    valid_position_hm = { player: compute_available_move( board_state= now_board, empty_list= valid_position_loc, specific_player= player) for player in [ -1, 1]}

                    now_board[ ai_empty_ind][ ai_empty_col] = 0

                    for hm_empty_ind, hm_empty_col, _ in valid_position_hm[ board_inf[ 2]]:
                        layer_2 = max_weights[ hm_empty_ind][ hm_empty_col]

                        # ??????????????????????????????????????????????????????
                        if layer_1 + layer_2 > best_score:
                            best_score = layer_1 + layer_2
                            global best_position
                            best_position = ( empty_ind, empty_col)

                now_board[ empty_ind][ empty_col] = 0

            # print( best_position, "", sep= "\n")
            for item in board_inf[0]:
                if item[0] == best_position[0] and item[1] == best_position[1]:
                    return best_position
            return board_inf[0][0]

        else:
            return choice( board_inf[ 0])