// Em produção o frontend e a API são servidos pela mesma origem (/api).
// No fluxo local o Live Server roda na 5500 e o uvicorn na 8000.
const API_BASE =
  location.hostname === "127.0.0.1" || location.hostname === "localhost"
    ? "http://127.0.0.1:8000/api"
    : "/api";

// A API não guarda a partida: o estado vai e volta em toda requisição.
async function postJSON(path, body = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  if (!response.ok) {
    throw new Error(`${path} respondeu ${response.status}`);
  }
  return response.json();
}

async function newGame() {
  return postJSON("/new_game");
}

async function fetchPossibleMoves(state, row, col, is_white) {
  const data = await postJSON("/possible_moves", {
    state,
    position: [row, col],
    is_white: is_white
  });
  return data.moves;
}

async function promotePawn(state, pos, pieceType) {
  return postJSON("/pawn_promotion", { state, pos, piece_type: pieceType });
}

async function fetchMove(state, act_row, act_col, future_row, future_col, is_white) {
  return postJSON("/move", {
    state,
    position: {
      actual: [act_row, act_col],
      new: [future_row, future_col]
    },
    is_white: is_white
  });
}
