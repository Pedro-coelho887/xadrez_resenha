from pieces.basic_piece import Piece
class King(Piece):
    def __init__(self,id,is_white):
        super().__init__(id=id,type=4,is_white=is_white)
        self.directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
    def calculate_moves(self, act_pos,board,calculate_possible_targets = False, enemy_targets = []):
        options = []
        for dx,dy in self.directions:
            nx, ny = act_pos[0] + dx, act_pos[1] + dy
            if (0 <= nx < 8 and 0 <= ny < 8) and (nx,ny) not in enemy_targets:
                target = board[nx][ny]
                if target is None or target.is_white != self.is_white or calculate_possible_targets:
                    options.append((nx,ny))
        return options
