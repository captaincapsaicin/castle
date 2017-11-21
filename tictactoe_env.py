import numpy as np
import chess

from tests.utils import map_xy_to_square, map_square_to_xy

class TicTacToeEnv(object):
    def __init__(self):
        '''
        state space: 2x3x3
        action space: 18 possible values -- 1 hot
            action: make actions a single integer -- in range(0, 18)
        assume x's always go first
        '''
        self.state = np.zeros((2, 3, 3))
        self.action_dims = (2, 3, 3)

    # The following 4 methods are called outside of the environment
    def get_next_state(self, state, action_int):
        # turn = get_turn_tictactoe(state)
        # if turn
        action_array = self.convert_int_to_action(action_int)
        next_state = state + action_array
        return next_state

    def get_legal_actions(self, state):
        turn = self.get_turn_tictactoe(state)
        # legal_actions = np.zeros((2, 3, 3), dtype=int)
        legal_actions = []
        for i in range(3):
            for j in range(3):
                if state[:, i, j].sum() == 0:
                    action_array = np.zeros((2, 3, 3), dtype=int)
                    action_array[turn, i, j] = 1
                    action_int = self.convert_action_to_int(action_array)
                    legal_actions.append(action_int)
        return np.array(legal_actions)

    def game_is_over(self, state):
        result = self.outcome(state)
        if result == 2:
            return 0
        else:
            return 1

    def outcome(self, state):
        '''
        1 is a win for x's
        -1 is a win for o's 
        0 is a tie 
        2: the game is not over
        '''
        for turn in range(2):
            if (state[turn,0,0] == 1 and state[turn,1,1] == 1 and state[turn,2,2] == 1) or (state[turn,2,0] == 1 and state[turn,1,1] == 1 and state[turn,0,2] == 1):
                return 1
            for i in range(3):
                if state[turn,0,i] == 1 and state[turn,1,i] == 1 and state[turn,2,i] == 1:
                    return 1
            for j in range(3):
                if state[turn,j,0] == 1 and state[turn,j,1] == 1 and state[turn,j,2] == 1:
                    return 1
        if state.sum() >= 9:
            return 0
        # if we reach this point, the game is not over.  return 2
        return 2

    def print_board(self, state):
        print('print_board')
        for i in range(3):
            row = ''
            for j in range(3):
                if state[0,i,j] == 1:
                    row += 'x '
                elif state[1,i,j] == 1:
                    row += 'o '
                else:
                    row += '* '
            print(row)

    def convert_action_to_int(self, action_array):
        '''
        action_array is 2x3x3
        '''
        action_array = np.reshape(action_array, -1)
        return np.where(action_array == 1)[0]

    def convert_int_to_action(self, action_int):
        action_array = np.zeros((self.action_dims), dtype=int)
        action_array = np.reshape(action_array, -1)
        action_array[action_int] = 1
        action_array = np.reshape(action_array, (self.action_dims))
        return action_array

    def get_turn_tictactoe(self, state):
        '''
        return 0 if x's turn 
        return 1 if o's turn
        '''
        num_xs = state[0,:,:].sum()
        num_os = state[1,:,:].sum()
        if num_os == num_xs:
            return 0
        elif num_xs > num_os:
            return 1
        else:
            return -1