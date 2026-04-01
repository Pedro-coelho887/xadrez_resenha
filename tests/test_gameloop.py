import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import unittest
from unittest.mock import patch
from pieces.basic_piece import Piece # type: ignore
from pieces.pawn import Pawn # type: ignore
from pieces.rook import Rook # type: ignore 
from pieces.king import King # type: ignore
from pieces.bishop import Bishop # type: ignore
from pieces.queen import Queen # type: ignore
from pieces.knight import Knight # type: ignore
from game import Game # type: ignore
class TestChecks(unittest.TestCase):
    def test_simpleCheck(self):
        game_test = Game()
        game_test.kings["black"] = (-1,-1)
        game_test.kings["white"] = (-1,-1)
        game_test.board[3][3] = Queen(id=1,is_white=True)
        game_test.board[2][5] = Knight(id=2, is_white = False)
        game_test.board[7][7] = King(id=3,is_white = False)
        game_test.kings["black"] = (7,7)
        # Movimenta Rainha
        with patch('builtins.input', side_effect=[3, 3, 0]):
            game_test.player_turn(is_white=True)
            game_test.show_board()
        self.assertEqual(game_test.in_check,False)
        # Checa se Rei não pode se deixar em check.
        options_king = game_test.board[7][7].calculate_moves((7,7),game_test.board,enemy_targets = game_test.targets["white"])
        self.assertNotIn((7,6),options_king)
        # Move Rainha para Deixar rei em check.
        with patch('builtins.input',side_effect=[4,3,6]):
            game_test.player_turn(is_white=True)
            game_test.show_board()
        self.assertEqual(game_test.in_check,True)
        # Move Rei para tirá-lo do check.
        with patch('builtins.input',side_effect=[7,7,0]):
            game_test.player_turn(is_white=False)
            game_test.show_board()
        self.assertEqual(game_test.in_check,False)
        # Move Rainha para retornar o Check e depois mata Rainha com Cavalo.
        with patch('builtins.input',side_effect=[4,7,7,2,5,1]):
            game_test.player_turn(is_white=True)
            self.assertEqual(game_test.in_check,True)
            game_test.player_turn(is_white=False)
            self.assertEqual(game_test.in_check,False)   
            game_test.show_board()
        # Cria Torre e Move ela para dar check no rei. Usa o Rei para matar a Torre.
        game_test.board[0][5] = Rook(id=4, is_white=True)
        with patch('builtins.input',side_effect=[0,5,6,7,6,2]):
            game_test.player_turn(is_white=True)
            self.assertEqual(game_test.in_check,True)
            game_test.show_board()
            game_test.player_turn(is_white=False)
            self.assertEqual(game_test.in_check,False)
            game_test.show_board()


if __name__ == "__main__":
    unittest.main()