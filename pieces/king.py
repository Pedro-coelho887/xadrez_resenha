from pieces.basic_piece import Piece
class King(Piece):
    def __init__(self,id,is_white):
        super().__init__(id=id,type=4,is_white=is_white)

    def calculate_moves(self, act_pos, board):
        directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        options = []

        for dx,dy in directions:
            nx, ny = act_pos[0] + dx, act_pos[1] + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[nx][ny]
                if target is None or target.is_white != self.is_white:
                    options.append((nx,ny))
        return options
