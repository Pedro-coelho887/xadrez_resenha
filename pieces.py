class Piece:
    def __init__(self,id:int=-1,type:int=0,team:bool=False,position:list = [-1,-1]):
        self.id = id
        self.type = type
        self.team = team
        self.position = position

    def __str__(self):
        return str(self.type)
    
    def calculate_moves(self,act_pos):
        if self.id != -1:
            if self.team == False:
                options = [(act_pos[0]+1,act_pos[1])]
            else:
                options = [(act_pos[0]-1,act_pos[1])]
            return options
        else:
            print("Peça inválida")
    #def move(self,)
