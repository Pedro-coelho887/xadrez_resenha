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
        self.targets = {'black':set(),'white':set()}
        self.kings = {'black':(0,4),'white':(7,4)}

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

    def calculate_all_targets(self):
        for x in range(8):
            for y in range(8):
                if self.board[x][y] is not None:
                    piece = self.board[x][y]
                    options = piece.calculate_moves((x,y),self.board,calculate_possible_targets=True) #type:ignore
                    if piece.is_white: #type:ignore    
                        for pos in options:
                            self.targets["white"].add(pos)
                    else:
                        for pos in options:
                            self.targets["black"].add(pos)

    def new_game(self):
        """Inicia um novo jogo"""
        self.fill_pieces()
        self.calculate_all_targets()
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
    
    def move(self,act_pos,future_pos):
        """Move a peça seleciona e, se for o caso, elimina a peça do oponente"""
        piece = self.board[act_pos[0]][act_pos[1]]
        if self.board[future_pos[0]][future_pos[1]] is not None:
            self.board[future_pos[0]][future_pos[1]] = None
        self.board[future_pos[0]][future_pos[1]] = piece
        self.board[act_pos[0]][act_pos[1]] = None

        # Atualiza posição do rei
        if piece.type == 4:
            if piece.is_white:
                self.kings["white"] = (future_pos[0],future_pos[1])
            else:
                self.kings["black"] = (future_pos[0],future_pos[1])

    def valid_check(self):
        self.calculate_all_targets()
        if self.kings["white"] in self.targets["black"] or self.kings["black"] in self.targets["white"]:
            print("check!")

    def player_turn(self,is_white):
        """Ciclo completo de uma jogada"""
        # Seleção de peça
        act_row = int(input("Linha da peça a ser movida: "))
        act_col = int(input("Coluna da peça a ser movida: "))
        act_pos = (act_row,act_col)
        # Seleção de Movimento
        piece = self.board[act_pos[0]][act_pos[1]]
        if piece is None or piece.is_white != is_white:
            print("Selecione uma peça válida!")
            return False
        options = piece.calculate_moves(act_pos,self.board)
        if not options:
            print("Selecione uma peça válida!")
            return False
        print(options)
        movimento = int(input("Selecione o Movimento desejado:"))
        if movimento > len(options):
            print("Selecione um Movimento Válido!")
            return False
        future_pos = options[movimento]
        self.move(act_pos,future_pos)
        self.valid_check()
        return True

    


def main():
    game1 = Game()
    game1.new_game()


if __name__ == "__main__":
    main()
