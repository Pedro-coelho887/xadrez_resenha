from pieces.basic_piece import Piece
class Knight(Piece):
    def __init__(self,id,is_white):
        super().__init__(id=id,type=7,is_white=is_white)
        self.directions = [(2,-1),(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2)]
    def calculate_moves(self, act_pos, board, calculate_possible_targets = False,atk_check = False,king_pos = (0,0),deff_check=False,options_to_stop_check = []):
        options = []
        # Caso esteja aplicando check
        if atk_check:
            options.append((act_pos[0],act_pos[1]))
            return options
        # Calculo Movimentos Base
        for dx,dy in self.directions:
            nx, ny = act_pos[0] + dx, act_pos[1] + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and (board[nx][ny] is None or board[nx][ny].is_white != self.is_white or calculate_possible_targets):
                options.append((nx,ny))

        if deff_check and options_to_stop_check:
            options = [op for op in options if op in options_to_stop_check]
        return options