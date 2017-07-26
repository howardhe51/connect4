

function clickColumn() {
  var button = $(this);
  var col = Number($(this).attr('id'));
  var urlsafeKey = $(button).val();
  $.post('/column', {'column': col}, function(game) {
    // Update the number in the "like" element.
    console.log("Game", game)
    $(col).text(game);
        drawBoard(JSON.parse(game));
  })}


function clearBoard() {
  for(i = 0; i< 7; i++) {
    for(j = 0; j<6; j++) {
      board[i][j]==0;
    }
  }
}

function drawBoard(game) {
  for(i = 0; i< 7; i++) {
    for(j = 0; j<6; j++) {
      if(game[j][i]==1){
        $("#square" + i + j).addClass('p1')
      }
      else if(game[j][i]==2){
        $("#square" + i + j).addClass('p2')
      }
    }
  }
}

$(".col").click(clickColumn);
