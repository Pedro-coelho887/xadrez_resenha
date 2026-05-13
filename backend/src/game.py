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
        self.promotion_pending = False
        self.promotion_pos = None

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
        self.calculate_all_targets()

    def reset(self):
        self.__init__()
        self.fill_pieces()

    def calculate_all_targets(self):
        self.targets["white"] = set()
        self.targets["black"] = set()
        for x in range(8):
            for y in range(8):
                if self.board[x][y] is not None: #type:ignore
                    piece = self.board[x][y]
                    options = piece.calculate_moves((x,y),self.board) #type:ignore
                    if piece.is_white: #type:ignore    
                        for pos in options:
                            self.targets["white"].add(pos)
                    else:
                        for pos in options:
                            self.targets["black"].add(pos)
        
    
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


    def valid_check(self,act_pos):
        """Valida se há peça de check"""
        piece = self.board[act_pos[0]][act_pos[1]]
        self.calculate_all_targets()
        atk_team = "white" if piece.is_white == True else "black"
        deff_team = "black" if atk_team == "white" else "white"
        # Retorna 0 se não há check, -1 se o time da peça movida está em cheque e 1 se o time da peça movida deu cheque
        if self.kings[atk_team] in self.targets[deff_team]:
            return -1
        elif self.kings[deff_team] in self.targets[atk_team]:
            return 1
        else:
            return 0
        
    def valid_checkmate(self,is_white):
        """Valida se houve check-mate"""
        for x in range(8):
            for y in range(8):
                if self.get_moves((x,y),is_white):
                    return False

        return True


    def simulate_move(self,act_pos,future_pos):
        """Simula o movimento de uma peça"""
        sim_piece = self.board[future_pos[0]][future_pos[1]]
        self.move(act_pos=act_pos,future_pos=future_pos)
        situation = self.valid_check(future_pos)
        # Desfaz movimento
        self.move(act_pos=future_pos,future_pos=act_pos)
        self.board[future_pos[0]][future_pos[1]] = sim_piece
        if situation == -1:
            return False
        else:
            return True
        
    def get_moves(self, act_pos, is_white):
        """Retorna os movimentos válidos para uma peça"""
        piece = self.board[act_pos[0]][act_pos[1]]
        if piece is None or piece.is_white != is_white:
            return []
        all_options = piece.calculate_moves(act_pos, self.board)
        legal_options = []
        for opt in all_options:
            if self.simulate_move(act_pos,opt):
                legal_options.append(opt)

        if piece.type == 4:
            legal_options += self.get_castling_moves(act_pos, is_white)
        return legal_options

    def get_castling_moves(self, king_pos, is_white):
        castling = []
        row, col = king_pos
        king = self.board[row][col]
        if king is None or king.has_moved:
            return castling

        self.calculate_all_targets()
        enemy = "black" if is_white else "white"

        if king_pos in self.targets[enemy]:
            return castling

        # Kingside: Torre em col 7, Rei vai para col 6
        rook_ks = self.board[row][7]
        if (rook_ks is not None and rook_ks.type == 3 and not rook_ks.has_moved
                and all(self.board[row][c] is None for c in [5, 6])
                and (row, 5) not in self.targets[enemy]
                and (row, 6) not in self.targets[enemy]):
            castling.append((row, 6))

        # Queenside: Torre em col 0, Rei vai para col 2
        rook_qs = self.board[row][0]
        if (rook_qs is not None and rook_qs.type == 3 and not rook_qs.has_moved
                and all(self.board[row][c] is None for c in [1, 2, 3])
                and (row, 3) not in self.targets[enemy]
                and (row, 2) not in self.targets[enemy]):
            castling.append((row, 2))

        return castling

    def promote(self, pos, piece_type):
        piece_map = {3: Rook, 5: Bishop, 6: Queen, 7: Knight}
        pawn = self.board[pos[0]][pos[1]]
        self.board[pos[0]][pos[1]] = piece_map[piece_type](id=pawn.id, is_white=pawn.is_white)
        if piece_type == 3:
            self.board[pos[0]][pos[1]].has_moved = True
        self.promotion_pending = False
        self.promotion_pos = None
        in_check = self.valid_check(pos)
        if in_check != 0:
            self.in_check = True
            self.checkmate = self.valid_checkmate(not pawn.is_white)
        else:
            self.in_check = False

    def execute_move(self, act_pos, future_pos, is_white):
        """Executa o movimento e atualiza o estado do jogo"""
        piece = self.board[act_pos[0]][act_pos[1]]
        if piece is None or piece.is_white != is_white:
            return False
        options = self.get_moves(act_pos, is_white)
        if tuple(future_pos) not in options:
            return False
        self.move(act_pos, future_pos)
        piece = self.board[future_pos[0]][future_pos[1]]
        if piece.type in (3, 4):
            piece.has_moved = True
        if piece.type == 4 and abs(future_pos[1] - act_pos[1]) == 2:
            row = future_pos[0]
            if future_pos[1] == 6:
                self.move((row, 7), (row, 5))
                self.board[row][5].has_moved = True
            else:
                self.move((row, 0), (row, 3))
                self.board[row][3].has_moved = True
        if piece.type == 2 and (future_pos[0] == 0 or future_pos[0] == 7):
            self.promotion_pending = True
            self.promotion_pos = future_pos
            return True
        in_check = self.valid_check(future_pos)
        if in_check != 0:
            self.in_check = True
            self.checkmate = self.valid_checkmate(not is_white)
            if self.checkmate:
                print("checkmate! "+f"{is_white}"+" venceu!")
        else:
            self.in_check = False

        return True
    


def main():
    game1 = Game()


if __name__ == "__main__":
    main()
