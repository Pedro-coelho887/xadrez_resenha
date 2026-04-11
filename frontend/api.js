async function fetchBoard() {
  const response = await fetch("http://127.0.0.1:8000/board");
  const data = await response.json();
  return data.board;
}

async function fetchPossibleMoves(row,col,is_white){
  const response = await fetch("http://127.0.0.1:8000/possible_moves",{
    method:"POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({position:[row,col],
                          is_white:is_white
    })
  });
  const data = await response.json();
  return data.moves;
}

async function fetchMove(act_row,act_col,future_row,future_col,is_white){
  const response = await fetch("http://127.0.0.1:8000/move",{
    method:"POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({position:{
                          actual:[act_row,act_col],
                          new:[future_row,future_col],
                        },
                          is_white:is_white})
  });
  const data = await response.json();
  return data;
}