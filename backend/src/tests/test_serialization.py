import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import unittest
from game import Game
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.king import King
from pieces.queen import Queen


class TestSerialization(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_round_trip_preserves_initial_board(self):
        """Tabuleiro inicial deve sobreviver ao ciclo to_dict -> from_dict"""
        self.game.fill_pieces()
        state = self.game.to_dict()
        restored = Game.from_dict(state)
        self.assertEqual(restored.to_dict(), state)

    def test_round_trip_preserves_piece_identity(self):
        """Cada peça deve voltar com a mesma classe, id e cor"""
        self.game.fill_pieces()
        restored = Game.from_dict(self.game.to_dict())
        for row in range(8):
            for col in range(8):
                original = self.game.board[row][col]
                copy = restored.board[row][col]
                if original is None:
                    self.assertIsNone(copy)
                    continue
                self.assertIsInstance(copy, type(original))
                self.assertEqual(copy.id, original.id)
                self.assertEqual(copy.is_white, original.is_white)

    def test_round_trip_rebuilds_targets(self):
        """targets é derivado e deve ser recalculado na desserialização"""
        self.game.fill_pieces()
        restored = Game.from_dict(self.game.to_dict())
        self.assertEqual(restored.targets, self.game.targets)

    def test_kings_come_back_as_tuples(self):
        """kings precisa ser tupla: valid_check compara com o set de targets"""
        self.game.fill_pieces()
        restored = Game.from_dict(self.game.to_dict())
        self.assertIsInstance(restored.kings["white"], tuple)
        self.assertIsInstance(restored.kings["black"], tuple)
        self.assertEqual(restored.kings, self.game.kings)

    def test_has_moved_survives_round_trip(self):
        """Rei que já se moveu não pode recuperar o direito ao roque"""
        self.game.board[7][4] = King(id=60, is_white=True)
        self.game.board[7][7] = Rook(id=63, is_white=True)
        self.game.kings["white"] = (7, 4)
        self.game.calculate_all_targets()
        self.assertEqual(self.game.get_castling_moves((7, 4), True), [(7, 6)])

        self.game.execute_move((7, 4), (6, 4), is_white=True)
        self.game.execute_move((6, 4), (7, 4), is_white=True)

        restored = Game.from_dict(self.game.to_dict())
        self.assertTrue(restored.board[7][4].has_moved)
        self.assertEqual(restored.get_castling_moves((7, 4), True), [])

    def test_castling_still_available_after_round_trip(self):
        """Contraprova: rei parado mantém o roque depois de serializar"""
        self.game.board[7][4] = King(id=60, is_white=True)
        self.game.board[7][7] = Rook(id=63, is_white=True)
        self.game.kings["white"] = (7, 4)

        restored = Game.from_dict(self.game.to_dict())
        self.assertFalse(restored.board[7][4].has_moved)
        self.assertEqual(restored.get_castling_moves((7, 4), True), [(7, 6)])

    def test_promotion_state_survives_round_trip(self):
        """promotion_pending/pos precisam atravessar a requisição"""
        self.game.board[1][0] = Pawn(id=8, is_white=True)
        self.game.board[7][4] = King(id=60, is_white=True)
        self.game.board[0][4] = King(id=4, is_white=False)
        self.game.kings["white"] = (7, 4)
        self.game.kings["black"] = (0, 4)
        self.game.execute_move((1, 0), (0, 0), is_white=True)
        self.assertTrue(self.game.promotion_pending)

        restored = Game.from_dict(self.game.to_dict())
        self.assertTrue(restored.promotion_pending)
        self.assertEqual(restored.promotion_pos, (0, 0))
        self.assertIsInstance(restored.promotion_pos, tuple)

    def test_promoted_piece_survives_round_trip(self):
        """Peão promovido deve voltar como a peça escolhida, não como peão"""
        self.game.board[1][0] = Pawn(id=8, is_white=True)
        self.game.board[7][4] = King(id=60, is_white=True)
        self.game.board[0][4] = King(id=4, is_white=False)
        self.game.kings["white"] = (7, 4)
        self.game.kings["black"] = (0, 4)
        self.game.execute_move((1, 0), (0, 0), is_white=True)
        self.game.promote((0, 0), 6)

        restored = Game.from_dict(self.game.to_dict())
        self.assertIsInstance(restored.board[0][0], Queen)
        self.assertFalse(restored.promotion_pending)
        self.assertIsNone(restored.promotion_pos)

    def test_check_flags_survive_round_trip(self):
        """in_check e checkmate fazem parte do estado da partida"""
        self.game.board[4][4] = King(id=1, is_white=True)
        self.game.kings["white"] = (4, 4)
        self.game.board[3][7] = Rook(id=2, is_white=False)
        self.game.board[0][0] = King(id=3, is_white=False)
        self.game.kings["black"] = (0, 0)
        self.game.execute_move((3, 7), (4, 7), is_white=False)
        self.assertTrue(self.game.in_check)

        restored = Game.from_dict(self.game.to_dict())
        self.assertTrue(restored.in_check)
        self.assertEqual(restored.checkmate, self.game.checkmate)

    def test_state_is_json_serializable(self):
        """to_dict tem que passar por json.dumps sem conversor customizado"""
        import json
        self.game.fill_pieces()
        payload = json.dumps(self.game.to_dict())
        self.assertEqual(Game.from_dict(json.loads(payload)).to_dict(),
                         self.game.to_dict())


if __name__ == "__main__":
    unittest.main(verbosity=2)
