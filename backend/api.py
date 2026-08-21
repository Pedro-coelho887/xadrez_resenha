import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from game import Game

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500","http://localhost:5500"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
router = APIRouter(prefix="/api")

# Status
@router.get("/health")
def health():
    return {"status":"ok"}

# Tabuleiro inicial
@router.post("/new_game")
def new_game():
    game = Game()
    game.fill_pieces()
    return {"state": game.to_dict()}

@router.post("/possible_moves")
def possible_moves(data:dict):
    game = Game.from_dict(data["state"])
    position = tuple(data["position"])
    is_white = data["is_white"]
    moves = game.get_moves(position,is_white)
    return {"moves": moves}

@router.post("/move")
def move(data:dict):
    game = Game.from_dict(data["state"])
    act_pos = tuple(data["position"]["actual"])
    new_pos = tuple(data["position"]["new"])
    is_white = data["is_white"]

    sucess = game.execute_move(act_pos,new_pos,is_white)
    response = {"status": "ok" if sucess else "invalid",
                "check":{"status":False},
                "state": game.to_dict()}

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

@router.post("/pawn_promotion")
def pawn_promotion(data: dict):
    game = Game.from_dict(data["state"])
    pos = tuple(data["pos"])
    piece_type = data["piece_type"]
    game.promote(pos, piece_type)
    response = {"status": "ok", "check": {"status": False}, "state": game.to_dict()}
    if game.in_check:
        attacker_is_white = game.board[pos[0]][pos[1]].is_white
        king_pos = game.kings["black"] if attacker_is_white else game.kings["white"]
        response["check"] = {"status": True, "king_pos": king_pos, "checkmate": game.checkmate}
    return response

app.include_router(router)
