from pieces.basic_piece import Piece
from typing import Optional


class Game:
    def __init__(self):
        self.board: list[list[Optional[Piece]]] = [[None] * 8 for _ in range(8)]
    
    def new_game(self):
        """Preenche Tabuleiro com peças padrão"""
        for x in range(2):
            for y in range(8):
                id = x*8 + y
                self.board[x][y] = Piece(id=id,type=1,team=False)
        
        for x in range(6,8):
            for y in range(8):
                id = x*8 + y
                self.board[x][y] = Piece(id=id,type=1,team=True)
    
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

    # def possible_moves(self,act_pos):
    #     """Elimina os movimentos não válidos que a peça calculou"""
    #     piece = self.board[act_pos[0]][act_pos[1]]
    #     if piece is None:
    #         return [],None
        
    #     options_all = piece.calculate_moves(act_pos)
    #     for option in options_all:
    #         if (option[0] or option [1]) > 7 or (option[0] or option[1]) < 0:
    #             options_all.remove(option)
    #         elif self.board[option[0]][option[1]] is not None and self.board[option[0]][option[1]].team == piece.team:
    #              options_all.remove(option)
    #     return options_all, piece

    
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
    game1.show_board()
    game1.move((1,1),(2,1))
    game1.move((7,0),(6,0))
    game1.move((2,1),(3,1))
    game1.move((3,1),(4,1))
    game1.move((4,1),(5,1))
    game1.move((5,1),(6,1))
    game1.move((6,1),(7,1))
    game1.move((7,1),(8,1))
    game1.move((6,0),(5,0))
    game1.move((7,0),(6,0))
    game1.move((5,5),(6,5))
    game1.show_board()


if __name__ == "__main__":
    main()
