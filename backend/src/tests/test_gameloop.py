import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
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
        print(20*"="+" Teste 1 "+20*"=")
        game_test.kings["white"] = (-1,-1)
        game_test.board[3][3] = Queen(id=1,is_white=True)
        game_test.board[2][5] = Knight(id=2, is_white = False)
        game_test.board[7][7] = King(id=3,is_white = False)
        game_test.kings["black"] = (7,7)
        game_test.board[0][0] = King(id=3,is_white = True)
        game_test.kings["black"] = (0,0)
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
        with patch('builtins.input',side_effect=[4,7,7,2,5,0]):
            game_test.player_turn(is_white=True)
            self.assertEqual(game_test.in_check,True)
            game_test.player_turn(is_white=False)
            game_test.show_board()
            self.assertEqual(game_test.in_check,False)   
            game_test.show_board()
        # Cria Torre e Move ela para dar check no rei. Usa o Rei para matar a Torre.
        game_test.board[0][5] = Rook(id=4, is_white=True)
        with patch('builtins.input',side_effect=[0,5,6,7,6,1]):
            game_test.player_turn(is_white=True)
            self.assertEqual(game_test.in_check,True)
            game_test.show_board()
            game_test.player_turn(is_white=False)
            self.assertEqual(game_test.in_check,False)
            game_test.show_board()

    def test_basic_checkmate(self):
        game_test = Game()
        game_test.board[0][0] = Rook(is_white = False,id=1)
        game_test.board[1][1] = Rook(is_white=False,id=2)
        game_test.board[7][7] = King(is_white=True,id=3)
        game_test.board[0][7] = King(is_white=False,id=4)
        game_test.kings["white"] = (7,7)
        game_test.kings["black"] = (0,7)
        # Move torre para ultima linha, rei em cheque, depois tira o rei do cheque
        with patch('builtins.input',side_effect=[0,0,6,7,7,0]):
            game_test.player_turn(is_white=False)
            self.assertEqual(game_test.in_check,True)
            game_test.show_board()
            game_test.player_turn(is_white = True)
            game_test.show_board()
            self.assertEqual(game_test.in_check,False)
        # Encurrala Rei, e dá check novamente.
        with patch('builtins.input',side_effect=[1,1,3,6,7,0,7,0,7]):
            game_test.player_turn(is_white=False)
            game_test.show_board()
            game_test.player_turn(is_white = True)
            game_test.show_board()
            game_test.player_turn(is_white=False)
            game_test.show_board()
            self.assertEqual(game_test.in_check,True)
        # Rei Foge, depois checkmate
        with patch('builtins.input',side_effect=[6,6,0,5,1,1]):
            game_test.player_turn(is_white=True)
            game_test.show_board()
            game_test.player_turn(is_white=False)
            game_test.show_board()
            print(game_test.options_to_stop_check)
            print(game_test.targets)
            # game_test.player_turn(is_white=False)
            self.assertEqual(game_test.checkmate,True)
            # game_test.show_board()

    def test_advanced_checkmate(self):
        game_test = Game()
        game_test.kings["black"] = (7,0)
        game_test.kings["white"] = (0,4)
        game_test.board[0][4] = King(id=1,is_white=True)
        game_test.board[7][0] = King(id=6,is_white=True)
        game_test.board[0][5] = Bishop(id=2,is_white=True)
        game_test.board[0][3] = Rook(id=3,is_white=True)
        game_test.board[5][5] = Queen(id=4,is_white=False)
        game_test.board[5][1] = Bishop(id=5,is_white=False)
        with patch('builtins.input',side_effect=[5,1,2,5,5,7]):
            game_test.player_turn(is_white=False)
            game_test.show_board()
            game_test.player_turn(is_white=False)
            game_test.show_board()
        self.assertEqual(game_test.checkmate,True)
        
        # print(game_test.options_to_stop_check)
        # print(game_test.targets["white"])
        # print(game_test.targets["black"])
        # with patch('builtins.input',side_effect=[0,7,0]):
        #     game_test.player_turn(is_white=True)
        #print(game_test.board[0][7].calculate_moves())
        


if __name__ == "__main__":
    #unittest.main(verbosity=2, defaultTest="TestChecks.test_basic_checkmate")
    unittest.main()