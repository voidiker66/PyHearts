from Deck import Deck
from Player import Player

class Game():
	"""
		self.players is a list of Player objects
	"""

	def __init__(self, tracker=None, debug=False):
		self.players = list()
		self.game_over = False
		self.deck = Deck()
		self.first_heart = False
		self.first_heart_card = None
		self.player_start_round = None
		self.center = dict()
		self.round_over = False
		self.hearts_broken = False

		self.tracker = tracker
		self.output_debug = debug

		# the card that dictates who starts the round
		# 39 = 2 of clubs, 40 = 3 of clubs
		# only in 3 player games can someone not have 42, but then it is
		# guaranteed that someone will have 43
		self.starting_card = 39

	def add_player(self, player):
		"""
			adds a new player to the game if there are less than 4 players
			hearts maxes at 4 players, so there can never be more than 4
		"""
		if len(self.players) < 4:
			self.players.append(player)

	def remove_player(self, player):
		"""
			if player exists and the list of players is greater than 0, we remove the player
		"""
		if len(self.players) > 0 and player in self.players:
			self.players.remove(player)

	def score_round(self):
		"""
			score the round and adds the points to the respective players
			then checks if there is a game_over status
			if not, start a new round of the game
		"""
		winner = None
		best_score = 200
		for player in self.players:
			player.score_pile()
			if player.score < best_score:
				winner = player.name
				best_score = player.score
			if player.score > 100:
				self.debug(player.name + " lost the game!")
				self.game_over = True
		if self.game_over:
			self.debug("The winner of the game is " + winner + " with a score of " + str(best_score) + "!")
		else:
			self.start_round()
		

	def play(self):
		"""
			starts the game
		"""
		# if 3 player game, we set aside the last card when dealing
		self.first_heart = len(self.players) == 3
		self.start_round()

	def print_scores(self):
		"""
			print the scores
		"""
		self.debug()
		for player in self.players:
			self.debug(player.name + " has a score of " + str(player.score))
		self.debug()

	def start_round(self):
		"""
			starts the new round and continues until all cards are played
		"""
		# if tracker exists, refresh
		if self.tracker:
			self.tracker.refresh()

		# reset round_over
		self.round_over = False
		# resets hearts broken
		self.hearts_broken = False

		self.print_scores()
		start_card = self.deal_cards()

		# while the players still have cards to play
		while not self.round_over:
			# this will reset the start_card after the first round
			# unfortunately, we have to keep resetting the start_card
			# will need to be addressed eventually
			start_card = self.players_take_turn(start_card)

			# if player1 is out of cards, all other players will be out, too
			if len(self.players[0].hand.deck_array) <= 0:
				self.round_over = True
		self.score_round()

	def print_center(self):
		"""
			prints the center to allow players to see what cards have been played so far this turn
		"""
		self.debug('Cards played in this order: ')
		for key, value in self.center.items():
			self.debug(value, end=' ')
		self.debug('\n')

	def players_take_turn(self, first_card=None):
		"""
			starting with the designated player, players left to right take their turns,
			and loops back to original player (who should not play again)
			if there is a designated first card to be played, restricts the 
			first Player's choices to only that card
		"""
		# clear the center
		self.center = dict()

		# the initial card determines validity
		# initial card is set by the first Player
		center_initial = self.players[self.player_start_round].take_turn(None, first_card, self.hearts_broken)
		self.center[self.player_start_round] = center_initial
		if self.tracker:
			self.tracker.card_played(self.deck.convert_external_card_to_int(center_initial), self.player_start_round)

		# we need the number value for the validation to work
		int_center_initial = self.deck.convert_external_card_to_int(center_initial)

		for i in range(self.player_start_round + 1, len(self.players)):
			self.print_center()
			self.center[i] = self.players[i].take_turn(int_center_initial, None, self.hearts_broken)
			if self.tracker:
				self.tracker.card_played(self.deck.convert_external_card_to_int(self.center[i]), i)
		for i in range(self.player_start_round):
			self.print_center()
			self.center[i] = self.players[i].take_turn(int_center_initial, None, self.hearts_broken)
			if self.tracker:
				self.tracker.card_played(self.deck.convert_external_card_to_int(self.center[i]), i)

		# end the turn and select a new player to start the next turn
		self.end_turn(int_center_initial)
		# reset the start_card
		return None


	def deal_cards(self):
		"""
			deals the cards to all the players and gets the Player who should start this round
			returns the card that will start the game. Should be 2 of clubs unless this is a 
			3 player game and the 2 of clubs is the first_heart_card
		"""
		self.player_start_round = None
		start_card = 39

		# we only care about 3 of clubs if it is a 3 player game
		if self.first_heart:
			clubs = None

		self.deck.shuffle_deck()
		# how many cards each person gets (17 if 3 player, 13 if 4)
		cards_each = 52 // len(self.players)
		for i in range(len(self.players)):
			self.players[i].set_hand(Deck(self.deck.deck_array[i*cards_each:(i*cards_each)+cards_each]))
			if 39 in self.players[i].get_number_hand():
				# if player was dealt the 2 of clubs, he is the starter
				self.player_start_round = i
			elif 40 in self.players[i].get_number_hand() and self.first_heart:
				clubs = i

		# if we didn't find the 2 of clubs, we assign the Player with 3 of clubs to start
		# then we set 3 of clubs to be the start card
		if not self.player_start_round and self.first_heart:
			self.player_start_round = clubs
			start_card = 40

		# if 3 player, we set aside the last card for who gets first heart
		if self.first_heart:
			self.first_heart_card = self.deck.deck_array[51]

		return start_card


	def end_turn(self, initial):
		"""
			determines which Player puts the cards in their cards_won and starts the next round
		"""
		top_card = initial

		suit_initial = initial // 13
		for player, card in self.center.items():
			int_card = self.deck.convert_external_card_to_int(card)
			suit = int_card // 13
			if suit == 1 and not self.hearts_broken:
				self.debug("Hearts have been broken.")
				self.hearts_broken = True
			if suit_initial == suit and int_card >= top_card:
				self.player_start_round = player
				top_card = int_card

		if self.tracker:
			self.tracker.end_turn()

		# now that we know who played the highest viable card, we give them the center
		self.players[self.player_start_round].add_to_pile(list(card for player, card in self.center.items()))


	def debug(self, message='', end='\n'):
		if self.output_debug:
			print(message, end=end)



