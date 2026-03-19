from pieces import Piece
class Game:
    def __init__(self):
        self.board = [[Piece()]*8 for _ in range(8)]
    
    def new_game(self):
        for x in range(2):
            for y in range(8):
                id = x*8 + y
                self.board[x][y] = Piece(id=id,type=1,team=False,position=[0,0])
        
        for x in range(6,8):
            for y in range(8):
                id = x*8 + y
                self.board[x][y] = Piece(id=id,type=1,team=True,position=[0,0])
    
    def show_board(self):
        result = ''
        for row in self.board:
            for piece in row:
                if piece.id == -1:
                    result += '. '
                else:
                    result += f'{piece.type} '
            result += '\n'
        print(result)


def main():
    game1 = Game()
    game1.new_game()
    game1.show_board()


if __name__ == "__main__":
    main()
