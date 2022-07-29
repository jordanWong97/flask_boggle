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

/** Display board appends rows and cells for letters from server*/

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

$('#newWordForm').on('submit', handleSubmit);

/** sends word to server, returns response */

async function sendWord() {

  let response = await axios.post("/api/score-word", {
    gameId,
    word: $wordInput.val()
  });

  return response;
}

/** adds valid words to word list on right side of page */

function appendGoodWords() {
  $playedWords.append(`<li>${$wordInput.val()}</li>`);
}

/** shows response result if word is not valid */

function displayIllegalPlay(response) {
  //take response from sendWord and display on msg $message
  //use reg expression to stringify result msg
  const msg = response.data.result.replace(/\-/gi, " ");
  $message.text(msg);
}


async function handleSubmit(evt) {

  evt.preventDefault();
  $message.empty();
  const response = await sendWord();
  if (response.data.result === 'ok') {
    appendGoodWords();
  } else {
    displayIllegalPlay(response);
  }
}




start();

