async function fetchBoard() {
  const response = await fetch("http://127.0.0.1:8000/board");
  const data = await response.json();
  return data.board;
}