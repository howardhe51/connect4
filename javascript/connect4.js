var board = [ [0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0]];

var player = 1;

function clickColumn() {
  var button = $(this);
  var col = Number($(this).attr('id'));
  var urlsafeKey = $(button).val();
  $.post('/column', {'column': col}, function(response) {
    // Update the number in the "like" element.
    $(col).text(response);
  });
  /*if(board[col][5] == 0 && player == 1) {
    board[col][5] = player;
    player = 2;
  }
  else if(board[col][5] == 0 && player == 2) {
    board[col][5] = player;
    player = 1;
  }
  else if(board[col][4] == 0 && player == 1) {
    board[col][4] = player;
    player = 2;
  }
  else if(board[col][4] == 0 && player == 2) {
    board[col][4] = player;
    player = 1;
  }
  else if(board[col][3] == 0 && player == 1) {
    board[col][3] = player;
    player = 2;
  }
  else if(board[col][3] == 0 && player == 2) {
    board[col][3] = player;
    player = 1;
  }
  else if(board[col][2] == 0 && player == 1) {
    board[col][2] = player;
    player = 2;
  }
  else if(board[col][2] == 0 && player == 2) {
    board[col][2] = player;
    player = 1;
  }
  else if(board[col][1] == 0 && player == 1) {
    board[col][1] = player;
    player = 2;
  }
  else if(board[col][1] == 0 && player == 2) {
    board[col][1] = player;
    player = 1;
  }
  else if(board[col][0] == 0 && player == 1) {
    board[col][0] = player;
    player = 2;
  }
  else if(board[col][0] == 0 && player == 2) {
    board[col][0] = player;
    player = 1;
  }
  console.log(board);*/

}

// Add a click event handler.
// Use $.post to "call" the /selectionHandler with the column that the user clicked on
// Use the result that the /selecdtionHandler gives back to update the board and see if there's a winner
$(".col").click(clickColumn);
