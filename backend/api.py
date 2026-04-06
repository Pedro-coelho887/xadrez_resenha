import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI
from src.game import Game

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500","http://localhost:5500"], 
    allow_methods=["GET", "POST"],             
    allow_headers=["*"],
)
# Status
@app.get("/")
def root():
    return {"status":"ok"}

game = Game()
game.fill_pieces()
# Tabuleiro Atual
@app.get("/board")
def get_board():
    board_serialized = []
    for row in game.board:
        serialized_row = []
        for piece in row:
            if piece is None:
                serialized_row.append(None)
            else:
                serialized_row.append({
                    "type":piece.type,
                    "is_white":piece.is_white,
                    "id":piece.id
                })
        board_serialized.append(serialized_row)
    return {"board":board_serialized}

@app.post("/possible_moves")
def possible_moves(data:dict):
    position = data["position"]
    piece = game.board[position[0]][position[1]]
    if piece is not None:
        options = piece.calculate_moves(position,game.board,deff_check=game.in_check,options_to_stop_check = game.options_to_stop_check)
    else:
        options = []
    return {"moves":options}

@app.post("/move")
def move(data:dict):
    act_pos = data["position"]["actual"]
    new_pos = data["position"]["new"]
    game.move(act_pos,new_pos)
    return {"status": "ok"}
