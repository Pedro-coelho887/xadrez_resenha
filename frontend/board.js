const board = document.getElementById("board");
const pieces_dict = {
    2:"pawn.png>", 3:"rook.png>", 4:"king.png>",
    5:"bishop.png>", 6:"queen.png>", 7:"knight.png>"
}
async function renderBoard() {
    const board_info = await fetchBoard()
    for (let row=0;row<8;row++){
        for (let col = 0; col<8;col++){
            const cell = document.createElement("div");
            cell.classList.add("cell");
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
renderBoard();
