from typing import Optional
from pieces.basic_piece import Piece
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.king import King
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.knight import Knight

class Game:
    def __init__(self):
        self.board: list[list[Optional[Piece]]] = [[None] * 8 for _ in range(8)]
    
    def fill_pieces(self):
        """Preenche Tabuleiro com peças padrão"""
        pieces_init = {0:Rook, 1:Knight, 2:Bishop, 3:Queen, 4:King, 5:Bishop, 6:Knight, 7:Rook}
        for x in [0,1,6,7]:
            is_white = x>2

            for y in range(8):
                id = 8*x + y

                if x in [1,6]:
                    piece = Pawn(id=id,is_white=is_white)

                else:
                    PieceType = pieces_init[y]
                    piece = PieceType(id=id,is_white=is_white)

                self.board[x][y] = piece

    def new_game(self):
        """Inicia um novo jogo"""
        self.fill_pieces()
        while True:
            black_played = True
            white_played = False
            self.show_board()
            if black_played:
                is_white = True
                white_played = self.player_turn(is_white)
                self.show_board()
            if white_played:
                is_white = False
                black_played = self.player_turn(is_white)
    
    def show_board(self):
        """Printa a situação atual do tabuleiro"""
        result = ''
        for row in self.board:
            for piece in row:
                if piece is None:
                    result += '. '
                else:
                    result += f'{piece.type} '
            result += '\n'
        print(result)
        return result
    
    def player_turn(self,is_white):
        act_row = int(input("Linha da peça a ser movida: "))
        act_col = int(input("Coluna da peça a ser movida: "))
        act_pos = (act_row,act_col)
        if self.board[act_row][act_col] is None or is_white != self.board[act_row][act_col].is_white:
            print("Movimento Inválido!")
            return False
        new_row = int(input("Linha da posição nova da peça: "))
        new_col = int(input("Coluna da posição nova peça: "))
        new_pos = (new_row,new_col)
        self.move(act_pos,new_pos)
        return True

    def move(self,act_pos,future_pos):
        """Move a peça seleciona e, se for o caso, elimina a peça do oponente"""
        piece = self.board[act_pos[0]][act_pos[1]]
        if piece is None:
            print("Selecione peça válida!")
        options = piece.calculate_moves(act_pos,self.board)
        print(options)
        if future_pos in options:
            if self.board[future_pos[0]][future_pos[1]] is not None:
                self.board[future_pos[0]][future_pos[1]] = None
            self.board[future_pos[0]][future_pos[1]] = piece
            self.board[act_pos[0]][act_pos[1]] = None
        else:
            print("Movimento Inválido!")


def main():
    game1 = Game()
    game1.new_game()
    #game1.show_board()
    # game1.move((1,1),(2,1))
    # game1.move((7,0),(6,0))
    # game1.move((2,1),(3,1))
    # game1.move((3,1),(4,1))
    # game1.move((4,1),(5,1))
    # game1.move((5,1),(6,1))
    # game1.move((6,1),(7,1))
    # game1.move((7,1),(8,1))
    # game1.move((6,0),(5,0))
    # game1.move((7,0),(6,0))
    # game1.move((5,5),(6,5))
    # game1.show_board()


if __name__ == "__main__":
    main()
