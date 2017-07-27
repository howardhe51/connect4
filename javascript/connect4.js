function clickColumn() {
  var button = $(this);
  var col = Number($(this).attr('id'));
  $.post('/column', {'column': col}, function(game_json) {
    // Update the number in the "like" element.
    game = JSON.parse(game_json)
    console.log("Game", game.board)
    drawBoard(game.board);
  })}


function clearBoard() {
  for(i = 0; i< 7; i++) {
    for(j = 0; j<6; j++) {
      board[i][j]==0;
    }
  }
}

function drawBoard(game) {
  console.log(game)
  for(i = 0; i< 6; i++) {
    for(j = 0; j<7; j++) {
      if(game[i][j]==1){
        console.log("I am in 1st if statement")
        $("#square" + j + i).addClass('p1');
      }
      else if(game[i][j]==2){
        $("#square" + j + i).addClass('p2');
      }
    }
  }
}

$(".col").click(clickColumn);
setInterval(refresh,1000);
function refresh() {
    // make Ajax call here, inside the callback call:
    $.get('/column', function(game_json) {
      game = JSON.parse(game_json);
      if(game.winner==game.player1){
        alert("Player One Wins!");
      }
      else if(game.winner == game.player2 && game.winner != null){
        alert("Player Two Wins!");
      }
      console.log("Board" , game.board);
      // Update the number in the "like" element.
      //console.log("Game", game)
      //$(col).text(game);
      drawBoard(game.board);
    })
    // ...
}
