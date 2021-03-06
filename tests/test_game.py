import unittest

import numpy as np
import tensorflow as tf

from dual_net import DualNet
from game import self_play_game, play_game, RandomModel
from kqk_chess_env import KQKChessEnv, KQK_CHESS_INPUT_SHAPE
from tictactoe_env import TicTacToeEnv

from utils import numline_env, mock_model_numline


class TestNumlineGame(unittest.TestCase):
    def test_numline_game(self):
        start_state = 0
        model = mock_model_numline
        env = numline_env

        n_leaf_expansions = 10
        c_puct = 1000
        temperature = 1
        states, v, pi = self_play_game(model,
                                       env,
                                       start_state,
                                       n_leaf_expansions,
                                       c_puct,
                                       temperature,
                                       max_num_turns=5)


class TestTicTacToeGame(unittest.TestCase):
    def setUp(self):
        self.env = TicTacToeEnv()

    def test_ttt_game(self):
        states, v = play_game(RandomModel(self.env), RandomModel(self.env), self.env)
        self.assertLessEqual(len(states), 9)
        self.assertGreaterEqual(len(states), 5)

    def test_ttt_with_mcts(self):
        states, v, pi = self_play_game(RandomModel(self.env),
                                       self.env,
                                       n_leaf_expansions=10,
                                       c_puct=1.0,
                                       temperature=1,
                                       max_num_turns=9,
                                       verbose=False)


class TestKQKChessGame(unittest.TestCase):
    def setUp(self):
        state_regime = 'KQK_conv'
        action_regime = 'KQK_pos_pos_piece'
        self.env = KQKChessEnv(state_regime, action_regime)
        start_state = np.zeros(KQK_CHESS_INPUT_SHAPE, dtype=int)

        # White King
        start_state[0, 2, 0] = 1
        # White Queen
        start_state[2, 0, 1] = 1
        # Black King
        start_state[3, 3, 2] = 1
        # initial board state:
        # . . . . . . . .
        # . . . . . . . .
        # . . . . . . . .
        # . . . . . . . .
        # . . . k . . . .
        # K . . . . . . .
        # . . . . . . . .
        # . . Q . . . . .

        self.start_state = start_state
        sess = tf.Session()
        self.network = DualNet(sess, self.env)
        sess.__enter__()
        tf.global_variables_initializer().run()

    def test_simulate_game(self):
        n_leaf_expansions = 10
        c_puct = 1000
        temperature = 1
        states, v, pi = self_play_game(self.network,
                                       self.env,
                                       self.start_state,
                                       n_leaf_expansions,
                                       c_puct,
                                       temperature,
                                       max_num_turns=5)
        self.assertEqual(len(v), 6)
        self.assertEqual(len(states), 6)
        self.assertEqual(len(pi), 6)
