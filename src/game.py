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
        self.in_check = False
        self.checkmate = False
        self.options_to_stop_check = [(-1,-1)]

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
        self.targets["white"] = set()
        self.targets["black"] = set()
        for x in range(8):
            for y in range(8):
                if self.board[x][y] is not None:
                    piece = self.board[x][y]
                    if piece.type == 4 and piece.is_white: #type:ignore
                        options = piece.calculate_moves((x,y),self.board,enemy_targets = self.targets["black"],calculate_possible_targets=True) #type:ignore
                    elif piece.type == 4 and not piece.is_white: #type:ignore
                        options = piece.calculate_moves((x,y),self.board,enemy_targets = self.targets["white"]) # type: ignore
                    else:
                        options = piece.calculate_moves((x,y),self.board,calculate_possible_targets=True) #type:ignore
                    if piece.is_white: #type:ignore    
                        for pos in options:
                            self.targets["white"].add(pos)
                    else:
                        for pos in options:
                            self.targets["black"].add(pos)

    def new_game(self,test = False):
        """Inicia um novo jogo"""
        if not test:
            self.fill_pieces()
        self.calculate_all_targets()
        while not self.checkmate:
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

    def valid_check(self,piece,act_pos):
        self.calculate_all_targets()
        atk_team = "white" if piece.is_white == True else "black"
        deff_team = "black" if atk_team == "white" else "white"
        # Se não estiver em Check, retorna
        if self.kings[deff_team] not in self.targets[atk_team]:
            self.options_to_stop_check = []
            self.in_check = False
            return
        print("check!")
        self.in_check = True
        self.options_to_stop_check = piece.calculate_moves(act_pos,self.board,calculate_possible_targets = False,atk_check = True,king_pos = self.kings[deff_team])

        if not any(op in self.options_to_stop_check for op in self.targets[deff_team]): #type:ignore
            print("checkmate!" + atk_team + " venceu!")
            self.checkmate = True

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
        # Calculo de Movimentos
        options = []
        
        # Movimentação Rei
        if piece.type == 4 and piece.is_white == True:
            options = piece.calculate_moves(act_pos,self.board,enemy_targets = self.targets["black"]) # type: ignore
        elif piece.type == 4 and piece.is_white == False:
            options = piece.calculate_moves(act_pos,self.board,enemy_targets = self.targets["white"]) # type: ignore
        # Movimentação outras peças
        else:
            options = piece.calculate_moves(act_pos,self.board,deff_check=self.in_check,options_to_stop_check = self.options_to_stop_check)
    
        if not options:
            print("Selecione uma peça válida!")
            return False
        
        print(options)
        movimento = int(input("Selecione o Movimento desejado:"))
        if movimento not in range(len(options)):
            print("Selecione um Movimento Válido!")
            return False
        future_pos = options[movimento]
        self.move(act_pos,future_pos)
        self.valid_check(piece,future_pos)
        return True

    


def main():
    game1 = Game()
    game1.new_game()


if __name__ == "__main__":
    main()
