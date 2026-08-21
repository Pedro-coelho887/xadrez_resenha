import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI
from game import Game

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
    position = tuple(data["position"])
    is_white = data["is_white"]
    moves = game.get_moves(position,is_white)
    return {"moves": moves}

@app.post("/move")
def move(data:dict):
    act_pos = tuple(data["position"]["actual"])
    new_pos = tuple(data["position"]["new"])
    is_white = data["is_white"]

    sucess = game.execute_move(act_pos,new_pos,is_white)
    response = {"status": "ok" if sucess else "invalid",
                "check":{"status":False}}

    if sucess and game.promotion_pending:
        response["promotion_pending"] = True
        response["promotion_pos"] = list(game.promotion_pos) #type:ignore
        return response
    response["promotion_pending"] = False
    if sucess and game.in_check:
        defender = not is_white
        king_pos = game.kings["white"] if defender else game.kings["black"]
        response["check"] = {"status":True,"king_pos":king_pos,"checkmate":game.checkmate}
    return response

@app.post("/pawn_promotion")
def pawn_promotion(data: dict):
    pos = tuple(data["pos"])
    piece_type = data["piece_type"]
    game.promote(pos, piece_type)
    response = {"status": "ok", "check": {"status": False}}
    if game.in_check:
        attacker_is_white = game.board[pos[0]][pos[1]].is_white
        king_pos = game.kings["black"] if attacker_is_white else game.kings["white"]
        response["check"] = {"status": True, "king_pos": king_pos, "checkmate": game.checkmate}
    return response

@app.post("/restart")
def restart():
    game.reset()
    return {"status": "ok"}
