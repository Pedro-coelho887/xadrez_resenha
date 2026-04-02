from pieces.basic_piece import Piece
class Bishop(Piece):
    def __init__(self,id,is_white):
        super().__init__(id=id,type=5,is_white=is_white)
        self.directions = [(1,1),(-1,1),(-1,-1),(1,-1)]
    def calculate_moves(self, act_pos, board, calculate_possible_targets = False,atk_check = False,king_pos = (0,0),deff_check=False,options_to_stop_check = []):
        options = []
        # Calculo de Movimentos base
        for dx,dy in self.directions:
            nx, ny = act_pos[0] + dx, act_pos[1] + dy
            while (0 <= nx < 8 and 0 <= ny < 8) and (board[nx][ny] is None or (board[nx][ny].type == 4 and board[nx][ny].is_white != self.is_white)):
                options.append((nx,ny))
                nx += dx
                ny += dy
            # Calculo de possíveis alvos
            if (0 <= nx <8 and 0 <= ny < 8) and (board[nx][ny].is_white != self.is_white or calculate_possible_targets):
                options.append((nx,ny))
            # Em caso da peça estiver aplicando check, calcula as casas da direção do check
            if atk_check:
                if king_pos not in options:
                    options.clear()
                else:
                    options.append((act_pos[0],act_pos[1]))
                    break
        if deff_check and options_to_stop_check:
            options = [op for op in options if op in options_to_stop_check]
        
        return options