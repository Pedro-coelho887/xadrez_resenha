from pieces.basic_piece import Piece
class Queen(Piece):
    def __init__(self,id,is_white):
        super().__init__(id=id,type=6,is_white=is_white)
        self.directions = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
    def calculate_moves(self, act_pos, board, calculate_possible_targets = False):
        options = []
        for dx,dy in self.directions:
            nx, ny = act_pos[0] + dx, act_pos[1] + dy
            while 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] is None:
                options.append((nx,ny))
                nx += dx
                ny += dy
            if (0 <= nx <8 and 0 <= ny < 8) and (board[nx][ny].is_white != self.is_white or calculate_possible_targets):
                options.append((nx,ny))

        return options