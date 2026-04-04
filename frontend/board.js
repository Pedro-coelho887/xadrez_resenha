const board = document.getElementById("board");

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
    if (row == 1){
        cell.innerHTML='<img src=graphics/pink/pink_pawn.png>'
    }
    if (row == 6){
        cell.innerHTML='<img src=graphics/blue/blue_pawn.png>'
    }
    if (row == 0 && col == 6){
        cell.innerHTML='<img src=graphics/pink/pink_knight.png>'
    }
    board.appendChild(cell)
    }
}