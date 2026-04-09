import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import unittest
from game import Game
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King
from pieces.knight import Knight

class TestCheck(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_king_not_in_check(self):
        """Rei isolado não deve estar em check"""
        self.game.board[4][4] = King(id=1, is_white=True)
        self.assertFalse(self.game.in_check)

    def test_king_in_check_by_rook(self):
        """Rei deve estar em check com torre na mesma linha"""
        self.game.board[4][4] = King(id=1, is_white=True)
        self.game.kings["white"] = (4,4)
        self.game.board[3][7] = Rook(id=2, is_white=False)
        self.game.execute_move((3, 7), (4, 7), is_white=False)
        self.assertTrue(self.game.in_check)

    def test_king_in_check_by_queen(self):
        """Rei deve estar em check com rainha na diagonal"""
        self.game.board[4][4] = King(id=1, is_white=True)
        self.game.kings["white"] = (4,4)
        self.game.board[6][7] = Queen(id=2, is_white=False)
        self.game.execute_move((6, 7), (7, 7), is_white=False)
        self.game.show_board()
        print(self.game.get_moves((7,7),is_white=False))
        print(self.game.in_check)
        self.assertTrue(self.game.in_check)

    def test_piece_blocking_check(self):
        """Peça aliada entre rei e atacante deve bloquear o check"""
        self.game.board[4][4] = King(id=1, is_white=True)
        self.game.board[4][6] = Pawn(id=3, is_white=True)   # bloqueador
        self.game.board[4][7] = Rook(id=2, is_white=False)
        self.assertFalse(self.game.in_check)

    def test_move_exposes_king_to_check(self):
        """Movimento que expõe o rei deve ser ilegal"""
        self.game.board[4][4] = King(id=1, is_white=True)
        self.game.board[4][6] = Pawn(id=3, is_white=True)   # bloqueando torre
        self.game.board[4][7] = Rook(id=2, is_white=False)
        # o peão em [4][6] não pode se mover pois exporia o rei
        moves = self.game.get_moves((4, 6), is_white=True)
        self.assertNotIn((5, 6), moves)

    def test_king_cannot_move_into_check(self):
        """Rei não deve poder se mover para casa atacada"""
        self.game.board[4][4] = King(id=1, is_white=True)
        self.game.board[6][5] = Rook(id=2, is_white=False)  # ataca coluna 5
        moves = self.game.get_moves((4, 4), is_white=True)
        self.assertNotIn((4, 5), moves)  # mover para coluna 5 seria check

    def test_execute_move_updates_board(self):
        """execute_move deve atualizar o tabuleiro corretamente"""
        self.game.board[4][4] = Pawn(id=1, is_white=False)
        self.game.execute_move((4, 4), (5, 4), is_white=False)
        self.assertIsNone(self.game.board[4][4])
        self.assertIsNotNone(self.game.board[5][4])

    def test_execute_invalid_move_returns_false(self):
        """execute_move deve retornar False para movimento inválido"""
        self.game.board[4][4] = Pawn(id=1, is_white=True)
        result = self.game.execute_move((4, 4), (6, 6), is_white=True)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=False,defaultTest="TestCheck")