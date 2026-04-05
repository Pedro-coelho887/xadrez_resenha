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

@app.get("/")
def root():
    return {"status":"ok"}

game = Game()
game.fill_pieces()

@app.get("/board")
def get_board():
    board_serialized = []
    for row in game.board:
        serialized_row = []
        for piece in row:
            if piece in row:
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