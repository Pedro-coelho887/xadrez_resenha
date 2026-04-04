class Piece:
    def __init__(self,id:int=-1,type:int=0,is_white:bool=False):
        self.id = id
        self.type = type
        self.is_white = is_white

    def __str__(self):
        return str(self.type)
    
    def calculate_moves(self, act_pos, board, calculate_possible_targets = False,atk_check = False,king_pos = (0,0),deff_check=False,options_to_stop_check = []):
        """Calcula os possíveis movimentos da peça básica"""
        options = []
        if self.is_white == False and act_pos[0] < 7 and (board[act_pos[0]+1][act_pos[1]] is None or board[act_pos[0]+1][act_pos[1]].is_white == True):
            options = [(act_pos[0]+1,act_pos[1])]
        elif self.is_white == True and act_pos[0] > 0 and (board[act_pos[0]-1][act_pos[1]] is None or board[act_pos[0]-1][act_pos[1]].is_white == True):
            options = [(act_pos[0]-1,act_pos[1])]
        return options
    
    def check_direction(self,act_pos,king_pos):
        pass
        
