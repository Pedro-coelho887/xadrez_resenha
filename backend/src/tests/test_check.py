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

class TestCheckmate(unittest.TestCase):
 
    def setUp(self):
        self.game = Game()
 
    # -------------------------
    # Não é checkmate
    # -------------------------
 
    def test_check_but_not_checkmate(self):
        """Check sem checkmate — rei pode escapar"""
        self.game.board[0][4] = King(id=1, is_white=True)
        self.game.kings["white"] = (0, 4)
        self.game.board[0][7] = Rook(id=2, is_white=False)
        # rei pode se mover para fora da linha
        self.assertFalse(self.game.valid_checkmate(is_white=True))
 
    def test_check_blockable(self):
        """Check sem checkmate — peça aliada pode bloquear"""
        self.game.board[0][4] = King(id=1, is_white=True)
        self.game.kings["white"] = (0, 4)
        self.game.board[3][4] = Rook(id=3, is_white=True)   # pode bloquear
        self.game.board[7][4] = Rook(id=2, is_white=False)  # atacante
        self.assertFalse(self.game.valid_checkmate(is_white=True))
 
    def test_check_capturable_attacker(self):
        """Check sem checkmate — peça atacante pode ser capturada"""
        self.game.board[0][4] = King(id=1, is_white=True)
        self.game.kings["white"] = (0, 4)
        self.game.board[0][6] = Rook(id=2, is_white=False)  # atacante capturável
        self.game.board[2][5] = Rook(id=3, is_white=True)   # pode capturar
        self.assertFalse(self.game.valid_checkmate(is_white=True))
 
    # -------------------------
    # Checkmate
    # -------------------------
 
    def test_back_rank_checkmate(self):
        """Back rank mate — rei preso na primeira fileira"""
        self.game.board[0][4] = King(id=1, is_white=True)
        self.game.kings["white"] = (0, 4)
        self.game.board[0][3] = Pawn(id=2, is_white=True)   # bloqueia fuga
        self.game.board[0][5] = Pawn(id=3, is_white=True)   # bloqueia fuga
        self.game.board[1][3] = Pawn(id=4, is_white=True)   # bloqueia fuga
        self.game.board[1][4] = Pawn(id=5, is_white=True)   # bloqueia fuga
        self.game.board[1][5] = Pawn(id=6, is_white=True)   # bloqueia fuga
        self.game.board[0][7] = Rook(id=7, is_white=False)  # ataca pela fileira
        self.assertTrue(self.game.valid_checkmate(is_white=True))
 
    # -------------------------
    # Integração com execute_move
    # -------------------------
 
    def test_execute_move_sets_checkmate(self):
        """execute_move deve setar checkmate após movimento decisivo"""
        self.game.board[0][4] = King(id=1, is_white=False)
        self.game.kings["black"] = (0, 4)
        self.game.board[0][3] = Pawn(id=2, is_white=False)
        self.game.board[1][4] = Pawn(id=4, is_white=False)
        self.game.board[1][5] = Pawn(id=5, is_white=False)
        self.game.board[1][3] = Pawn(id=6, is_white=False)
        self.game.show_board()
        self.game.board[7][7] = Rook(id=7, is_white=True)  # posição antes do mate
        self.game.execute_move((7, 7), (0, 7), is_white=True)  # move torre para dar mate
        self.game.show_board()
        self.assertTrue(self.game.checkmate)
 
    def test_execute_move_no_checkmate_after_normal_move(self):
        """execute_move não deve setar checkmate em jogada normal"""
        self.game.board[4][4] = Pawn(id=1, is_white=True)
        self.game.board[0][4] = King(id=2, is_white=True)
        self.game.kings["white"] = (0, 4)
        self.game.board[7][4] = King(id=3, is_white=False)
        self.game.kings["black"] = (7, 4)
        self.game.execute_move((4, 4), (5, 4), is_white=True)
        self.assertFalse(self.game.checkmate)
 

class TestPromotion(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_promotion_sets_pending(self):
        """execute_move com peão na penúltima fileira deve setar promotion_pending"""
        self.game.board[7][7] = King(id=1, is_white=True)
        self.game.kings["white"] = (7, 7)
        self.game.board[0][7] = King(id=2, is_white=False)
        self.game.kings["black"] = (0, 7)
        self.game.board[1][4] = Pawn(id=10, is_white=True)
        self.game.execute_move((1, 4), (0, 4), is_white=True)
        self.assertTrue(self.game.promotion_pending)
        self.assertEqual(self.game.promotion_pos, (0, 4))

    def test_promotion_replaces_pawn(self):
        """promote deve substituir peão por Rainha mantendo o id original"""
        self.game.board[7][7] = King(id=1, is_white=True)
        self.game.kings["white"] = (7, 7)
        self.game.board[7][0] = King(id=2, is_white=False)
        self.game.kings["black"] = (7, 0)
        self.game.board[0][4] = Pawn(id=10, is_white=True)
        self.game.promotion_pending = True
        self.game.promote((0, 4), 6)
        piece = self.game.board[0][4]
        self.assertEqual(piece.type, 6)
        self.assertEqual(piece.id, 10)
        self.assertFalse(self.game.promotion_pending)

    def test_promotion_gives_check(self):
        """Rainha promovida na mesma fileira do rei inimigo deve dar check"""
        self.game.board[7][7] = King(id=1, is_white=True)
        self.game.kings["white"] = (7, 7)
        self.game.board[0][0] = King(id=2, is_white=False)
        self.game.kings["black"] = (0, 0)
        self.game.board[0][4] = Pawn(id=10, is_white=True)
        self.game.promotion_pending = True
        self.game.promote((0, 4), 6)
        self.assertTrue(self.game.in_check)

    def test_promotion_gives_checkmate(self):
        """Promoção deve dar checkmate quando rei inimigo não tem escapes"""
        self.game.board[0][7] = King(id=1, is_white=False)
        self.game.kings["black"] = (0, 7)
        self.game.board[1][7] = Pawn(id=3, is_white=False)
        self.game.board[1][6] = Pawn(id=4, is_white=False)
        self.game.board[7][0] = King(id=2, is_white=True)
        self.game.kings["white"] = (7, 0)
        self.game.board[0][1] = Pawn(id=10, is_white=True)
        self.game.promotion_pending = True
        self.game.promote((0, 1), 6)
        self.assertTrue(self.game.checkmate)


if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=False,defaultTest="TestCheckmate")