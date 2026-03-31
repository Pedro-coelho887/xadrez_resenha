import unittest
from src.pieces.basic_piece import Piece
from src.pieces.pawn import Pawn
from src.pieces.rook import Rook
from src.pieces.king import King
from src.pieces.bishop import Bishop
from src.pieces.queen import Queen
from src.pieces.knight import Knight
from src.game import Game

# Testes de Colisão Desativados por mudança na função move
class TestPiece(unittest.TestCase):

    def test_basic_piece(self):
        game_teste = Game()
        #Teste Criação
        game_teste.board[0][0] = Piece(id=1,type=1,is_white=False)
        game_teste.board[1][0] = Piece(id=2,type=1,is_white=True)
        result = game_teste.show_board()
        expected = '1 . . . . . . . \n1 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n'
        self.assertEqual(result, expected)
        #Teste Eliminação
        game_teste.move((0,0),(1,0))
        result = game_teste.show_board()
        self.assertEqual(result, '. . . . . . . . \n1 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        # #Teste Colisão com mesmo time
        # game_teste.move((1,0),(2,0))
        # game_teste.move((2,0),(3,0))
        # game_teste.board[4][0] = Piece(id=3,type=1,is_white=False)
        # game_teste.move((3,0),(4,0))
        # result = game_teste.show_board()
        # self.assertEqual(result,'. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n1 . . . . . . . \n1 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n' )
        # #Teste Bordas
        # game_teste.move((4,0),(5,0))
        # game_teste.move((5,0),(6,0))
        # game_teste.move((6,0),(7,0))
        # game_teste.move((7,0),(8,0))
        # result = game_teste.show_board()
        #self.assertEqual(result,'. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n1 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n1 . . . . . . . \n')

    def test_pawn(self):
        game_teste = Game()
        # Movimento Base Peão
        game_teste.board[0][0] = Pawn(id=1,is_white=False)
        result = game_teste.show_board()
        game_teste.move((0,0),(1,0))
        result = game_teste.show_board()
        self.assertEqual(result,'. . . . . . . . \n2 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        # # Colisão mesmo time
        # game_teste.board[2][0] = Pawn(id=2,is_white=False)
        # result = game_teste.show_board()
        # game_teste.move((1,0),(2,0))
        # result = game_teste.show_board()
        # self.assertEqual(result,'. . . . . . . . \n2 . . . . . . . \n2 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        # # Colisão time adversário
        # game_teste.board[3][0] = Pawn(id=3,is_white = True)
        # game_teste.move((2,0),(3,0))
        # result = game_teste.show_board()
        #self.assertEqual(result,'. . . . . . . . \n2 . . . . . . . \n2 . . . . . . . \n2 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        # Eliminação Time adversário
        game_teste.board[3][1] = Pawn(id=4,is_white=True)
        game_teste.board[4][0] = Pawn(id=5,is_white=True)
        game_teste.board[2][1] = Pawn(id=6,is_white=False)
        game_teste.move((4,0),(3,0))
        game_teste.move((3,0),(2,1))
        result = game_teste.show_board()
        self.assertEqual(result,'. . . . . . . . \n2 . . . . . . . \n. 2 . . . . . . \n. 2 . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        # Teste Borda
        # game_teste.move((1,0),(0,0))
        # game_teste.move((0,0),(1,0))
        # result = game_teste.show_board()
        # self.assertEqual(result,'2 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n2 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')

    def test_rook(self):
        game_teste = Game()
        # Movimento Básico Torre
        game_teste.board[0][0] = Rook(id=1,is_white=True)
        result = game_teste.show_board()
        game_teste.move((0,0),(6,0))
        game_teste.move((6,0),(6,7))
        game_teste.move((6,7),(2,7))
        game_teste.move((2,7),(2,0))
        result = game_teste.show_board()
        self.assertEqual(result,'. . . . . . . . \n. . . . . . . . \n3 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        # Eliminação com Torre
        game_teste.board[2][5] = Pawn(id=2,is_white = False)
        game_teste.move((2,0),(2,6))
        game_teste.move((2,0),(2,5))
        result = game_teste.show_board()
        # Colisão com mesmo Time
        # game_teste.board[0][5] = Rook(id=3,is_white=False)
        # game_teste.board[2][7] = Pawn(id=4,is_white=True)
        # game_teste.board[2][0] = Pawn(id=5,is_white=True)
        # game_teste.board[6][5] = Rook(id=6,is_white=True)
        # game_teste.move((2,5),(2,6))
        # result = game_teste.show_board()
        # self.assertEqual(result,'. . . . . 3 . . \n. . . . . . . . \n2 . . . . . 3 2 \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . 3 . . \n. . . . . . . . \n')

    def test_king(self):
        game_teste = Game()
        #Movimento Básico Rei
        game_teste.board[0][0] = King(id=1,is_white = True)
        result = game_teste.show_board()
        self.assertEqual(result,'4 . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        # Eliminação Time Oposto
        game_teste.board[2][5] = Rook(id=2,is_white = False)
        game_teste.move((0,0),(1,0))
        game_teste.move((2,5),(2,1))
        game_teste.move((1,0),(2,1))
        result = game_teste.show_board()
        self.assertEqual(result,'. . . . . . . . \n. . . . . . . . \n. 4 . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        #Colisão Mesmo Time
        # game_teste.board[1][2] = Pawn(id=3,is_white = True)
        # game_teste.move((2,1),(1,2))
        # result = game_teste.show_board()
        # self.assertEqual(result,'. . . . . . . . \n. . 2 . . . . . \n. 4 . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')

    def test_bishop(self):
        game_teste = Game()
        # Movimento Básico Bispo
        game_teste.board[5][5] = Bishop(id=1,is_white=True)
        game_teste.move((5,5),(7,7))
        result = game_teste.show_board()
        self.assertEqual(result,'. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . 5 \n')
        # Eliminação Time oposto
        game_teste.board[1][1] = Pawn(id=2,is_white = False)
        game_teste.move((7,7),(1,1))
        result = game_teste.show_board()
        self.assertEqual(result,'. . . . . . . . \n. 5 . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        # Colisão Mesmo Time
        # game_teste.board[0][2] = Rook(id=3,is_white = True)
        # game_teste.move((1,1),(0,2))
        # result = game_teste.show_board()
        # self.assertEqual(result,'. . 3 . . . . . \n. 5 . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')

    def test_queen(self):
        game_teste = Game()
        # Movimento Básico Rainha
        game_teste.board[4][4] = Queen(id=1,is_white=True)
        game_teste.move((4,4),(5,5))
        result = game_teste.show_board()
        self.assertEqual(result,'. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . 6 . . \n. . . . . . . . \n. . . . . . . . \n')
        # Eliminação Time oposto
        game_teste.board[5][2] = Pawn(id=2,is_white = False)
        game_teste.move((5,5),(5,2))
        result = game_teste.show_board()
        self.assertEqual(result,'. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . 6 . . . . . \n. . . . . . . . \n. . . . . . . . \n' )
        # #Colisão Mesmo Time
        # game_teste.board[7][0] = King(id=3,is_white = True)
        # game_teste.move((5,2),(7,0))
        # result = game_teste.show_board()
        # self.assertEqual(result,'. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . 6 . . . . . \n. . . . . . . . \n4 . . . . . . . \n')

    def test_knight(self):
        game_teste = Game()
        # Movimento Básico Cavalo (Com pulo)
        game_teste.board[2][4] = Knight(id=1,is_white = False)
        game_teste.board[3][4] = Pawn(id=2,is_white = True)
        game_teste.move((2,4),(4,5))
        result = game_teste.show_board()
        # Eliminação Time oposto
        game_teste.board[3][3] = Rook(id=3,is_white = True)
        game_teste.move((4,5),(3,3))
        result = game_teste.show_board()
        self.assertEqual(result,'. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . 7 2 . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')
        #Colisão Mesmo Time
        # game_teste.board[2][5] = King(id=4,is_white = False)
        # game_teste.move((3,3),(2,5))
        # result = game_teste.show_board()
        # self.assertEqual(result,'. . . . . . . . \n. . . . . . . . \n. . . . . 4 . . \n. . . 7 2 . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n. . . . . . . . \n')

if __name__ == "__main__":
    unittest.main(verbosity=2, defaultTest="TestPiece.test_pawn")
    #unittest.main()