class Piece:
    def __init__(self,id:int=-1,type:int=0,team:bool=False):
        self.id = id
        self.type = type
        self.team = team

    def __str__(self):
        return str(self.type)
    
    def calculate_moves(self,act_pos,board):
        """Calcula os possíveis movimentos da peça básica"""
        options = []
        if self.team == False and act_pos[0] < 7 and (board[act_pos[0]+1][act_pos[1]] is None or board[act_pos[0]+1][act_pos[1]].team == True):
            options = [(act_pos[0]+1,act_pos[1])]
        elif self.team == True and act_pos[0] > 0 and (board[act_pos[0]-1][act_pos[1]] is None or board[act_pos[0]-1][act_pos[1]].team == True):
            options = [(act_pos[0]-1,act_pos[1])]
        return options
        
