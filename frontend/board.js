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
async function renderBoardAnimated() {
    // fade out nas imagens existentes
    document.querySelectorAll(".cell img").forEach(img => {
        img.classList.add("fading");
    });

    await new Promise(resolve => setTimeout(resolve, 150)); // espera transição

    await renderBoard(); // re-renderiza (limpa e recria o board)

    // força o navegador a reconhecer o estado inicial antes do fade in
    await new Promise(resolve => setTimeout(resolve, 20));
    document.querySelectorAll(".cell img").forEach(img => {
        img.classList.remove("fading");
    });
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
        // inicia fade out imediatamente ao clicar
        const fadePromise = new Promise(resolve => {
        document.querySelectorAll(".cell img").forEach(img => img.classList.add("fading"));
        setTimeout(resolve, 150);
        });
        const promotingIsWhite = isWhiteTurn;
        const result = await fetchMove(selectedCell[0], selectedCell[1], row, col,isWhiteTurn);
        isWhiteTurn = !isWhiteTurn
        selectedCell = null;
        currentMoves = [];
        await fadePromise;
        await renderBoard(); // re-renderiza

        await new Promise(resolve => setTimeout(resolve, 20));
        document.querySelectorAll(".cell img").forEach(img => img.classList.remove("fading"));

        if (result.promotion_pending) {
            showPromotionModal(result.promotion_pos, promotingIsWhite);
            return;
        }
        // Tratamento de Check
        // limpa check anterior
        document.querySelectorAll(".in_check").forEach(c => c.classList.remove("in-check"));
        if (result.check.status) {
            const [r, c] = result.check.king_pos;
            console.log(r)
            const kingCell = document.querySelector(`[data-row="${r}"][data-col="${c}"]`);
            console.log(kingCell)
            if (kingCell) kingCell.classList.add("in_check");
            if (result.check.checkmate){
                const winner = isWhiteTurn ? "Azul" : "Rosa";  // isWhiteTurn já foi invertido
                document.getElementById("winner-text").textContent = `Time ${winner} Ganhou!`;
                document.getElementById("checkmate-modal").classList.remove("hidden");
            }
        }
    } else {
        selectedCell = [row, col];
        currentMoves = await fetchPossibleMoves(row, col,isWhiteTurn);
        highlightMoves(currentMoves);
    }
}

function showPromotionModal(pos, isWhite) {
    const color = isWhite ? "pink" : "blue";
    const choices = document.getElementById("promotion-choices");
    choices.innerHTML = "";
    const promotable = [
        { type: 6, name: "queen" },
        { type: 3, name: "rook" },
        { type: 5, name: "bishop" },
        { type: 7, name: "knight" }
    ];
    promotable.forEach(({ type, name }) => {
        const img = document.createElement("img");
        img.src = `graphics/${color}/${color}_${name}.png`;
        img.addEventListener("click", () => onPromotionChoice(pos, type));
        choices.appendChild(img);
    });
    document.getElementById("promotion-modal").classList.remove("hidden");
}

async function onPromotionChoice(pos, pieceType) {
    document.getElementById("promotion-modal").classList.add("hidden");
    const result = await promotePawn(pos, pieceType);
    await renderBoardAnimated();
    document.querySelectorAll(".in_check").forEach(c => c.classList.remove("in_check"));
    if (result.check.status) {
        const [r, c] = result.check.king_pos;
        const kingCell = document.querySelector(`[data-row="${r}"][data-col="${c}"]`);
        if (kingCell) kingCell.classList.add("in_check");
        if (result.check.checkmate) {
            const winner = isWhiteTurn ? "Azul" : "Rosa";
            document.getElementById("winner-text").textContent = `Time ${winner} Ganhou!`;
            document.getElementById("checkmate-modal").classList.remove("hidden");
        }
    }
}

async function restartGame() {
    await fetch("http://127.0.0.1:8000/restart", { method: "POST" });
    document.getElementById("checkmate-modal").classList.add("hidden");
    isWhiteTurn = true;
    selectedCell = null;
    currentMoves = [];
    await renderBoard();
}

function startGame() {
    document.getElementById("start-modal").classList.add("hidden");
}

renderBoard();
