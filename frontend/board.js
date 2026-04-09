const board = document.getElementById("board");
const pieces_dict = {
    2:"pawn.png>", 3:"rook.png>", 4:"king.png>",
    5:"bishop.png>", 6:"queen.png>", 7:"knight.png>"
}
let selectedCell = null;
let currentMoves = [];    
let isWhiteTurn = true;
async function renderBoard() {
    board.innerHTML = '';
    const board_info = await fetchBoard()
    for (let row=0;row<8;row++){
        for (let col = 0; col<8;col++){
            const cell = document.createElement("div");
            cell.classList.add("cell");
            cell.dataset.row = row;
            cell.dataset.col = col;

            cell.addEventListener("click", () => onCellClick(row, col));
            
            if ((row + col) % 2 == 0){
                cell.classList.add("light");
            }
            else{
                cell.classList.add("dark");
            }
            let img = '';
            piece = board_info[row][col]
            if (piece != null){
                if (piece["is_white"] == true){
                img = '<img src=graphics/pink/pink_'
                }
                else{
                img = '<img src=graphics/blue/blue_' 
                }
                img = img + pieces_dict[piece["type"]]
            }
            cell.innerHTML = img
            board.appendChild(cell)
        }
    
    }
}

function highlightMoves(moves) {
    // remove highlights anteriores
    document.querySelectorAll(".highlight").forEach(cell => {
        cell.classList.remove("highlight");
    });
    // adiciona highlight nas novas opções
    moves.forEach(([row, col]) => {
        const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
        if (cell) cell.classList.add("highlight");
    });
}
async function onCellClick(row, col) {
    if (selectedCell && currentMoves.some(([r, c]) => r === row && c === col)) {
        await fetchMove(selectedCell[0], selectedCell[1], row, col,isWhiteTurn);
        isWhiteTurn = !isWhiteTurn
        selectedCell = null;
        currentMoves = [];
        await renderBoard();
    } else {
        selectedCell = [row, col];
        currentMoves = await fetchPossibleMoves(row, col,isWhiteTurn);
        highlightMoves(currentMoves);  // ← mantém o highlight aqui
    }
}
renderBoard();
