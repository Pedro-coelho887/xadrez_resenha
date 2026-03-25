from pieces.basic_piece import Piece
class Pawn(Piece):
    def __init__(self,id,is_white):
        super().__init__(id=id,type=2,is_white=is_white)
    
    def calculate_moves(self, act_pos, board):
        options = []
        # Estudo de nova implementação:
        # directions = [(1,0),(-1,0)]
        # if self.is_white:
        #     nx,ny = act_pos[0] + 1
        if not self.is_white and act_pos[0] < 7:
                if board[act_pos[0]+1][act_pos[1]] is None:
                    options.append((act_pos[0]+1,act_pos[1]))
                if act_pos[1] < 7 and board[act_pos[0] + 1][act_pos[1]+1] is not None and board[act_pos[0] + 1][act_pos[1]+1].is_white:
                    options.append((act_pos[0]+1,act_pos[1]+1))
                if act_pos[1] > 0 and board[act_pos[0] + 1][act_pos[1]-1] is not None and board[act_pos[0] + 1][act_pos[1]-1].is_white:
                    options.append((act_pos[0]+1,act_pos[1]-1))
                
        elif self.is_white and act_pos[0] > 0 :
                if board[act_pos[0]-1][act_pos[1]] is None:
                    options.append((act_pos[0]-1,act_pos[1]))
                if act_pos[1] < 7 and board[act_pos[0] - 1][act_pos[1]+1] is not None and not board[act_pos[0] - 1][act_pos[1]+1].is_white:
                    options.append((act_pos[0]-1,act_pos[1]+1))
                if act_pos[1] > 0 and board[act_pos[0] - 1][act_pos[1]-1] is not None and  not board[act_pos[0] - 1][act_pos[1]-1].is_white:
                    options.append((act_pos[0]-1,act_pos[1]-1))
        return options
        