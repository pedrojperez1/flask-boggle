import json
from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify, redirect, make_response
from flask_debugtoolbar import DebugToolbarExtension # pylint: disable=import-error

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickensarecool12341"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def root():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template(
        'base.html',
        board=board
    )

@app.route('/guess', methods=['POST'])
def make_a_guess():
    """Responds with result if given word is a word and in the boggle board"""
    try:
        response = json.loads(request.data)
    except:
        raise Exception("Invalid form data provided by client")

    result = boggle_game.check_valid_word(session['board'], response['guess'])
    return jsonify(result=result)

@app.route('/send-score', methods=['POST'])
def save_user_score():
    """Records the score sent to this route and redirects user back to root"""
    user_score = json.loads(request.data)['score']

    if not isinstance(user_score, int):
        return make_response("Score must be of type *int*.", 400)

    session['game_count'] = session.get('game_count', 0) + 1 
    session['hiscore'] = get_new_hiscore(user_score)
    return redirect('/')

def get_new_hiscore(new_score):
    """Compares the input score to the current hiscore in session and returns the higher one"""
    return max(session.get('hiscore', 0), new_score)

