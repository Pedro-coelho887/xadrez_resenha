from pieces.basic_piece import Piece
class Rook(Piece):
    def __init__(self,id,is_white):
        super().__init__(id=id,type=3,is_white=is_white)

    def calculate_moves(self, act_pos, board):
        options = []
        directions = [(1,0),(0,1),(-1,0),(0,-1)]
        for dx,dy in directions:
            nx, ny = act_pos[0] + dx, act_pos[1] + dy
            while 0 <= nx < 8 and 0 <= ny < 8 and board[nx][ny] is None:
                options.append((nx,ny))
                nx += dx
                ny += dy
            if (0 <= nx <8 and 0 <= ny < 8) and board[nx][ny].is_white != self.is_white:
                options.append((nx,ny))
        # Opções a direita
        # i = act_pos[0] + 1
        # while i < 8 and board[i][act_pos[1]] is None:
        #     options.append((i,act_pos[1]))
        #     i += 1
        # if i < 8 and board[i][act_pos[1]].is_white != self.is_white:
        #     options.append((i,act_pos[1]))
        
        # # Opções a esquerda
        # i = act_pos[0] - 1
        # while i >=0 and board[i][act_pos[1]] is None:
        #     options.append((i,act_pos[1]))
        #     i -= 1
        # if i >= 0 and board[i][act_pos[1]].is_white != self.is_white:
        #     options.append((i,act_pos[1]))

        # # Opções para baixo
        # j = act_pos[1] + 1
        # while j < 8 and board[act_pos[0]][j] is None:
        #     options.append((act_pos[0],j))
        #     j += 1
        # if j < 8 and board[act_pos[0]][j].is_white != self.is_white:
        #     options.append((act_pos[0],j))
        
        # # Opções para cima
        # j = act_pos[1] - 1
        # while j >= 0 and board[act_pos[0]][j] is None:
        #     options.append((act_pos[0],j))
        #     j -= 1
        # if j >= 0 and board[act_pos[0]][j].is_white != self.is_white:
        #     options.append((act_pos[0],j))
        return options
        