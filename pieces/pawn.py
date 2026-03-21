from pieces.basic_piece import Piece
class Pawn(Piece):
    def __init__(self,id,team):
        super().__init__(id=id,type=2,team=team)
    
    def calculate_moves(self, act_pos, board):
        options = []
        if self.team == False and act_pos[0] < 7:
                if board[act_pos[0]+1][act_pos[1]] is None:
                    options.append((act_pos[0]+1,act_pos[1]))
                if act_pos[1] < 7 and board[act_pos[0] + 1][act_pos[1]+1] is not None and board[act_pos[0] + 1][act_pos[1]+1].team is True:
                    options.append((act_pos[0]+1,act_pos[1]+1))
                if act_pos[1] > 0 and board[act_pos[0] + 1][act_pos[1]-1] is not None and board[act_pos[0] + 1][act_pos[1]-1].team is True:
                    options.append((act_pos[0]+1,act_pos[1]-1))
                
        elif self.team == True and act_pos[0] > 0 :
                if board[act_pos[0]-1][act_pos[1]] is None:
                    options.append((act_pos[0]-1,act_pos[1]))
                if act_pos[1] < 7 and board[act_pos[0] - 1][act_pos[1]+1] is not None and board[act_pos[0] - 1][act_pos[1]+1].team is False:
                    options.append((act_pos[0]-1,act_pos[1]+1))
                if act_pos[1] > 0 and board[act_pos[0] - 1][act_pos[1]-1] is not None and board[act_pos[0] - 1][act_pos[1]-1].team is False:
                    options.append((act_pos[0]-1,act_pos[1]-1))
        return options
        