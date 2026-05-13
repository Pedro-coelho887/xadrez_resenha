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


class TestMovement(unittest.TestCase):

    def setUp(self):
        """Cria um jogo limpo antes de cada teste"""
        self.game = Game()
        self.game.board[0][3] = King(id=-1,is_white=False)
        self.game.board[0][7] = King(id=-2,is_white=True)
        #self.game.fill_pieces()

    # -------------------------
    # Testes de movimentação
    # -------------------------

    def test_pawn_move_forward(self):
        """Peão deve poder avançar uma casa"""
        self.game.board[4][4] = Pawn(id=0, is_white=False)
        moves = self.game.get_moves((4, 4), is_white=False)
        self.assertIn((5, 4), moves)

    def test_pawn_blocked(self):
        """Peão não deve poder avançar se há peça na frente"""
        self.game.board[4][4] = Pawn(id=1, is_white=False)
        self.game.board[5][4] = Pawn(id=2, is_white=True)
        moves = self.game.get_moves((4, 4), is_white=False)
        self.assertNotIn((5, 4), moves)

    def test_rook_moves_horizontally(self):
        """Torre deve poder se mover horizontalmente em casa vazia"""
        self.game.board[4][4] = Rook(id=1, is_white=True)
        moves = self.game.get_moves((4, 4), is_white=True)
        self.assertIn((4, 7), moves)
        self.assertIn((4, 0), moves)

    def test_rook_blocked_by_ally(self):
        """Torre não deve atravessar peça aliada"""
        self.game.board[4][4] = Rook(id=1, is_white=True)
        self.game.board[4][6] = Pawn(id=2, is_white=True)
        moves = self.game.get_moves((4, 4), is_white=True)
        self.assertNotIn((4, 7), moves)  # bloqueado pela aliada em [4][6]
        self.assertIn((4, 5), moves)     # pode ir até antes da aliada

    def test_rook_captures_enemy(self):
        """Torre deve poder capturar peça inimiga"""
        self.game.board[4][4] = Rook(id=1, is_white=True)
        self.game.board[4][6] = Pawn(id=2, is_white=False)
        moves = self.game.get_moves((4, 4), is_white=True)
        self.assertIn((4, 6), moves)     # pode capturar
        self.assertNotIn((4, 7), moves)  # mas não atravessar

    def test_knight_L_shape(self):
        """Cavalo deve se mover em L"""
        self.game.board[4][4] = Knight(id=1, is_white=True)
        moves = self.game.get_moves((4, 4), is_white=True)
        self.assertIn((6, 5), moves)
        self.assertIn((6, 3), moves)
        self.assertIn((2, 5), moves)
        self.assertIn((2, 3), moves)

    def test_knight_jumps_over_pieces(self):
        """Cavalo deve poder pular sobre peças"""
        self.game.board[4][4] = Knight(id=1, is_white=True)
        self.game.board[5][4] = Pawn(id=2, is_white=True)
        self.game.board[4][5] = Pawn(id=3, is_white=True)
        moves = self.game.get_moves((4, 4), is_white=True)
        self.assertIn((6, 5), moves)  # ainda consegue pular

    def test_bishop_moves_diagonally(self):
        """Bispo deve se mover na diagonal"""
        self.game.board[4][4] = Bishop(id=1, is_white=True)
        moves = self.game.get_moves((4, 4), is_white=True)
        self.assertIn((7, 7), moves)
        self.assertIn((1, 1), moves)

    def test_queen_moves_all_directions(self):
        """Rainha deve se mover em todas as direções"""
        self.game.board[4][4] = Queen(id=1, is_white=True)
        moves = self.game.get_moves((4, 4), is_white=True)
        self.assertIn((4, 7), moves)  # horizontal
        self.assertIn((7, 4), moves)  # vertical
        self.assertIn((7, 7), moves)  # diagonal

    def test_pawn_first_move_white(self):
        """Peão branco na linha inicial deve poder avançar duas casas"""
        self.game.board[6][4] = Pawn(id=0, is_white=True)
        moves = self.game.get_moves((6, 4), is_white=True)
        self.assertIn((4, 4), moves)

    def test_pawn_double_step_blocked_at_intermediate(self):
        """Peão não pode avançar duas casas se a casa intermediária está ocupada"""
        self.game.board[6][4] = Pawn(id=0, is_white=True)
        self.game.board[5][4] = Pawn(id=1, is_white=False)
        moves = self.game.get_moves((6, 4), is_white=True)
        self.assertNotIn((4, 4), moves)

    def test_wrong_team_cannot_move(self):
        """Não deve ser possível mover peça do time adversário"""
        self.game.board[4][4] = Pawn(id=1, is_white=False)
        moves = self.game.get_moves((4, 4), is_white=True)
        self.assertEqual(moves, [])

    def test_empty_cell_returns_no_moves(self):
        """Célula vazia não deve retornar movimentos"""
        moves = self.game.get_moves((4, 4), is_white=True)
        self.assertEqual(moves, [])

if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=False,defaultTest="TestMovement")