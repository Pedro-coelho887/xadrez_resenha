from pieces.basic_piece import Piece
class Bishop(Piece):
    def __init__(self,id,is_white):
        super().__init__(id=id,type=5,is_white=is_white)

    def calculate_moves(self, act_pos, board):
        options = []
        directions = [(1,1),(-1,1),(-1,-1),(1,-1)]
        for dx,dy in directions:
            nx, ny = act_pos[0] + dx, act_pos[1] + dy
            while 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] is None:
                options.append((nx,ny))
                nx += dx
                ny += dy
            if (0 <= nx <8 and 0 <= ny < 8) and board[nx][ny].is_white != self.is_white:
                options.append((nx,ny))
                
        return options