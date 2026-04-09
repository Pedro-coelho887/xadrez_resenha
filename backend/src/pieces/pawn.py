from pieces.basic_piece import Piece
class Pawn(Piece):
    def __init__(self,id,is_white):
        super().__init__(id=id,type=2,is_white=is_white)
        self.directions = [(-1,0),(-1,1),(-1,-1)] if self.is_white else [(1,0),(1,1),(1,-1)]
    def calculate_moves(self, act_pos, board):
        options = []
        for x,y in self.directions:
            nx,ny = act_pos[0] + x,act_pos[1] + y
            if 0 <= nx < 8 and 0 <= ny < 8:
                if ny == act_pos[1] and board[nx][ny] is None:
                    options.append((nx,ny))
                if ny != act_pos[1] and board[nx][ny] is not None and board[nx][ny].is_white != self.is_white:
                    options.append((nx,ny))
        return options
        