from flask_login import LoginManager, login_user, current_user, login_required, logout_user, UserMixin
from flask import Flask,jsonify,request,render_template,Response,flash,redirect,url_for
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_wtf import Form
from wtforms import TextField, BooleanField, validators, PasswordField, SubmitField, SelectField, FileField, SelectMultipleField, BooleanField
from werkzeug.security import generate_password_hash, \
	 check_password_hash
from datetime import *
from sqlalchemy import create_engine
#from wtforms.validators import Required
from werkzeug.utils import secure_filename
import os
import uuid

# event scheduler so we can delete game instances after time delay
import sched, time
import schedule

# from flask_pusher import Pusher

from Game import Game, Player
from Tracker import Tracker
from SmartPlayer import SmartPlayer

games_states = dict()

CLIENT_AUTH_TIMEOUT = 24 # in Hours

garbage_collector = sched.scheduler(time.time, time.sleep)

app = Flask(__name__)
# pusher = Pusher(app, url_prefix='/play')
# for now, we will do manual webhooks

DATABASE_PATH = 'sqlite:///database/PyHearts.db'

UPLOAD_FOLDER = '/static/images'
# only allow images to be uploaded
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
db = SQLAlchemy(app)

app.config.update(dict(
	SECRET_KEY="powerful secretkey",
	WTF_CSRF_SECRET_KEY="a csrf secret key"
))

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_PATH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

e = create_engine(DATABASE_PATH)

login_manager = LoginManager()

# every day at noon, run the garbage collector to remove all the finished games
schedule.every().day.at("12:00").do(garbage_collector.run)

# using a scheduler, we delete the game instance after the delay
def schedule_delete(instance):
	games_states.pop(instance)



class StartGameForm(Form):
	# usernames for all 4 players
	playerone = TextField('Player One', validators=[validators.Required()])
	playertwo = TextField('Player Two', validators=[validators.Required()])
	playerthree = TextField('Player Three', validators=[validators.Required()])
	playerfour = TextField('Player Four', validators=[validators.Required()])

	# are the players computers or not (will implement later)
	# aione = BooleanField('AI', validators=[])
	# aitwo = BooleanField('AI', validators=[])
	# aithree = BooleanField('AI', validators=[])
	# aifour = BooleanField('AI', validators=[])

	submit = SubmitField('Start Game')

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		# if all the names are filled out and none are the same
		if self.playerone.data and self.playertwo.data and self.playerthree.data and self.playerfour.data:
			if self.playerone.data not in (self.playertwo.data, self.playerthree.data, self.playerfour.data):
				if self.playertwo.data not in (self.playerthree.data, self.playerfour.data):
					if self.playerthree.data != self.playerfour.data:
						return True
		flash('All fields must be filled out and unique.', category='red')
		return False


@app.route('/_change_state', methods=['GET', 'POST'])
def change_state():
	# hidden url that we can use to query the game state and update without refreshing
	gamestate = None
	token = request.args.get('token')
	card = request.args.get('card')

	initial_card = game.initial_card
	first_card = game.first_card
	hearts_broken = game.hearts_broken

	game = games_states[token]
	current_player = game.players[game.current_player]

	if card is not None:
		# if card has been played, we use that to update game state
		if current_player.check_play_validity(card, initial_card, first_card, hearts_broken):
			# if the card user chose is valid
			pass
		else:
			flash('The card you chose is not valid.', category='red')
	else:
		# we return the current game state without updating
		gamestate = game
	return gamestate

@app.route('/', methods=['GET', 'POST'])
def home():
	form = StartGameForm()
	if form.validate_on_submit():
		if form.validate():

			token = uuid.uuid1().hex

			tracker = Tracker()
			# i need to change Game so that it reacts to web input rather than command line
			game = Game(tracker=tracker, debug=True, flask=True)
			game.add_player(Player(form.playerone.data, debug=True))
			game.add_player(Player(form.playertwo.data, debug=True))
			game.add_player(Player(form.playerthree.data, debug=True))
			game.add_player(Player(form.playerfour.data, debug=True))

			games_states[token] = game

			# delete this game instance after the timeout (at the first noon after timeout ends)
			garbage_collector.enter(timedelta(hours=CLIENT_AUTH_TIMEOUT).total_seconds(), 1, schedule_delete(token))

			return redirect('play?token=' + token)
	return render_template('index.html', form=form)

@app.route('/play')
def play():
	return render_template('play.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
	#app.run(host='0.0.0.0', port=80)