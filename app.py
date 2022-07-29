from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    info = {"gameId": game_id, "board": games[game_id].board}

    return jsonify(info)


@app.post('/api/score-word')
def score_word():
    """Accepts post request with JSON(gameId,word) checks if word is legal """

    # should be in wordlist, findable on board
    word = request.json["word"].upper()
    gameId = request.json["gameId"]
    curent_game = games[gameId]

    if not curent_game.is_word_in_word_list(word):
        return jsonify({'result': 'not-word'})
    elif not curent_game.check_word_on_board(word):
        return jsonify({'result': 'not-on-board'})
    else:
        return jsonify({'result': 'ok'})