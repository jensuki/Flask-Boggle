from flask import Flask, render_template, request, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my53cr3tk3y'

boggle_game = Boggle()

# define a route for home page
@app.route('/')
def homepage():
    """ Display the Boggle gameboard & the form for guesses """
    board = boggle_game.make_board()
    session['board'] = board
    topscore = session.get('topscore', 0)
    ntimesplayed = session.get('ntimesplayed', 0)

    return render_template(
        'index.html',
        board=board,
        topscore=topscore,
        ntimesplayed=ntimesplayed)

# define a route for checking word validity
@app.route('/check-word')
def check_word():
    """ Check if word is valid """
    word = request.args['word']
    board=session['board']
    response = boggle_game.check_valid_word(board,word)

    return jsonify({'result': response})

@app.route('/post-score', methods=["POST"])
def post_score():
    """Get score, update ntimesplayed, update topscore if broken"""
    # extract score value from JSON data that was sent in request
    score = request.json['score']
    # retrieve current topscore & ntimesplayed
    topscore = session.get('topscore', 0)
    ntimesplayed = session.get('ntimesplayed', 0)

    # increment 1 to each ntimesplayed & save to session
    session['ntimesplayed'] = ntimesplayed + 1
    # return higher score from either score or topscore & save to session
    session['topscore'] = max(score, topscore)

    return jsonify(brokeRecord=score > topscore)
