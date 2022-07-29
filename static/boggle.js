"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();
  // loop over board and create the DOM tr/td structure
  //make table body
  const $body = $('<tbody>');
  for (let y = 0; y < board.length; y++) {
    //make table row
    const $row = $('<tr>');
    for (let x = 0; x < board.length; x++) {
      //make table data with td filled with letters from board
      //append to rows
      const $letter = $('<td>').text(board[y][x]);
      $row.append($letter);
    }
    //append rows to body
    $body.append($row);
  }
  $table.append($body);
}


start();

