from pieces.basic_piece import Piece
class Knight(Piece):
    def __init__(self,id,is_white):
        super().__init__(id=id,type=7,is_white=is_white)

    def calculate_moves(self, act_pos, board):
        options = []
        directions = [(2,-1),(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2)]
        for dx,dy in directions:
            nx, ny = act_pos[0] + dx, act_pos[1] + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and (board[nx][ny] is None or board[nx][ny].is_white != self.is_white):
                options.append((nx,ny))
        return options