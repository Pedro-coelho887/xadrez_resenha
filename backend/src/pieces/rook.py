from pieces.basic_piece import Piece
class Rook(Piece):
    def __init__(self,id,is_white):
        super().__init__(id=id,type=3,is_white=is_white)
        self.directions = [(1,0),(0,1),(-1,0),(0,-1)]
    def calculate_moves(self, act_pos, board):
        options = []
        # Calculo de Movimentos base
        options = []
        # Calculo de Movimentos base
        for dx,dy in self.directions:
            nx, ny = act_pos[0] + dx, act_pos[1] + dy
            while (0 <= nx < 8 and 0 <= ny < 8) and (board[nx][ny] is None):
                options.append((nx,ny))
                nx += dx
                ny += dy
            # Calculo de Possíveis eliminações
            if (0 <= nx <8 and 0 <= ny < 8) and board[nx][ny].is_white != self.is_white:
                options.append((nx,ny))
        
        return options