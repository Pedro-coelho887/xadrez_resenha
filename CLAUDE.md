# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run the backend (from project root):**
```bash
source venv/bin/activate
python -m uvicorn backend.api:app --reload
```

**Run all tests:**
```bash
python -m unittest backend.src.tests.test_move
python -m unittest backend.src.tests.test_check
```

**Run a specific test:**
```bash
python -m unittest backend.src.tests.test_check.TestCheck.test_name -v
```

**Run the frontend:**
Serve `frontend/` with any static file server on port 5500 (e.g. VSCode Live Server). Backend must be running on port 8000.

---

## Architecture

### Backend (`backend/`)

FastAPI app with a single **global `Game` instance** (`api.py:23`) that persists board state across all requests. No database; state lives in memory and resets on server restart.

**6 REST endpoints** (`backend/api.py`):
- `GET /board` — serialized board state
- `POST /possible_moves` — legal moves for a piece
- `POST /move` — execute a move; returns check/checkmate status
- `POST /restart` — reset game

**Game logic** (`backend/src/game.py`):
- Board is `board[row][col]` (8×8 list), `row=0` is the black side, `row=7` is the white side.
- `execute_move()` is the main entry point: validates ownership, fetches legal moves, performs the move, then detects check/checkmate.
- `get_moves()` filters candidates by running `simulate_move()` for each — any move that leaves the own king in check is discarded.
- `valid_check()` returns `-1` (mover's king in check — illegal), `0` (no check), or `1` (opponent's king in check).
- King positions are tracked in `self.kings` dict for O(1) lookup.

**Pieces** (`backend/src/pieces/`):
- All pieces inherit from `Piece` (`basic_piece.py`) and implement `calculate_moves(board) -> list[[row, col]]`.
- Piece type IDs: `2=Pawn`, `3=Rook`, `4=King`, `5=Bishop`, `6=Queen`, `7=Knight`.

**Missing rules:** castling and en passant are not implemented.

---

### Frontend (`frontend/`)

Vanilla JS — no build step, no npm. Three files:

- `api.js` — thin wrapper over `fetch`; all calls go to hardcoded `http://127.0.0.1:8000`.
- `board.js` — board rendering, click handling, move highlighting, check/checkmate display.
- `style.css` — dark theme; white pieces use `graphics/pink/`, black pieces use `graphics/blue/`.

**Interaction model:** two-click flow — first click selects a piece and fetches legal moves from backend; second click on a highlighted cell executes the move.

**State split:** the backend is the single source of truth for board state. The frontend only tracks `selectedCell`, `currentMoves`, and `isWhiteTurn` locally. After every move the board is fully re-fetched and re-rendered.

**Piece colors in UI:** white pieces are displayed in pink (`graphics/pink/`), black pieces in blue (`graphics/blue/`). The checkmate modal labels them "Rosa" (white) and "Azul" (black).
