import unittest
from pieces.basic_piece import Piece
from pieces.pawn import Pawn
from game import Game
class TestPiece(unittest.TestCase):

    def test_basic_piece(self):
        game_teste = Game()
        #Teste Criação
        game_teste.board[0][0] = Piece(id=1,type=1,team=False)
        game_teste.board[1][0] = Piece(id=2,type=1,team=True)
        result = game_teste.show_board()
        expected = '1 . . . . . . . \n1 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n'
        self.assertEqual(result, expected)
        #Teste Eliminação
        game_teste.move((0,0),(1,0))
        result = game_teste.show_board()
        #print(repr(result))
        self.assertEqual(result, '. . . . . . . . \n1 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        #Teste Colisão com mesmo time
        game_teste.move((1,0),(2,0))
        game_teste.move((2,0),(3,0))
        game_teste.board[4][0] = Piece(id=3,type=1,team=False)
        game_teste.move((3,0),(4,0))
        result = game_teste.show_board()
        self.assertEqual(result,'. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n1 . . . . . . . \n1 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n' )
        #Teste Bordas
        game_teste.move((4,0),(5,0))
        game_teste.move((5,0),(6,0))
        game_teste.move((6,0),(7,0))
        game_teste.move((7,0),(8,0))
        result = game_teste.show_board()
        #print(repr(result))
        self.assertEqual(result,'. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n1 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n1 . . . . . . . \n')

    def test_pawn(self):
        game_teste = Game()
        # Movimento Base Peão
        game_teste.board[0][0] = Pawn(id=1,team=False)
        game_teste.move((0,0),(1,0))
        result = game_teste.show_board()
        self.assertEqual(result,'. . . . . . . . \n2 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        # Colisão mesmo time
        game_teste.board[2][0] = Pawn(id=2,team=False)
        game_teste.move((1,0),(2,0))
        result = game_teste.show_board()
        self.assertEqual(result,'. . . . . . . . \n2 . . . . . . . \n2 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        # Colisão time adversário
        game_teste.board[3][0] = Pawn(id=3,team = True)
        game_teste.move((2,0),(3,0))
        result = game_teste.show_board()
        self.assertEqual(result,'. . . . . . . . \n2 . . . . . . . \n2 . . . . . . . \n2 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        # Eliminação Time adversário
        game_teste.board[3][1] = Pawn(id=4,team=True)
        game_teste.board[4][0] = Pawn(id=5,team=True)
        game_teste.board[2][1] = Pawn(id=6,team=False)
        game_teste.move((2,0),(3,1))
        game_teste.move((3,1),(4,0))
        game_teste.move((3,0),(2,1))
        game_teste.move((2,1),(1,0))
        result = game_teste.show_board()
        self.assertEqual(result,'. . . . . . . . \n2 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n2 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        # Bordas
        game_teste.move((1,0),(0,0))
        game_teste.move((0,0),(1,0))
        result = game_teste.show_board()
        self.assertEqual(result,'2 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n2 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')

if __name__ == "__main__":
    unittest.main()