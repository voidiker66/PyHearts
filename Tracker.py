class Tracker():

	def __init__(self):

		# all variables are set in refresh
		self.refresh()

		# we can also track how many rounds are in a game
		# we start at 0 because game starts rounds until game is finished
		# so best way to track is increment on start_round
		self.round_number = 0

		# track who received the queen each round
		self.queens = list()

	def refresh(self):
		"""
			resets all the variables so that next round is fresh
		"""
		self.turn_number = 1

		self.cards_played = list()
		self.cards_left = 52
		self.hearts_broken = False
		self.current_center = list()
		self.current_player = None

		# suits counts so we can reduce times calculated
		# allows us to know how many of each suit are left
		# 0=spades, 1=hearts, 2=diamonds, 3=clubs
		self.suits = {0:13, 1:13, 2:13, 3:13}

		# we need to track is someone is out of a suit so we can predict their play
		# dict of lists, where player_id provides list of suits player no longer has
		self.off_suit = dict()

		# we need to keep track of how many points each player has received
		self.points_received = dict()

	def card_played(self, card, player_id):
		"""
			tracks the card played and which player played it
			player is the player id from the game, not the player object
			if player plays off-suit card, we know he does not have that suit
		"""
		self.current_player = player_id

		self.current_center.append(card)
		self.cards_played.append(card)
		self.cards_left -= 1

		# get suit of the card played
		suit = card // 13

		# get the suit of the first card
		initial_suit = self.current_center[0] // 13

		# if this card is the first card, will always be on suit
		# if suit not equal to first card played, card is off-suit
		# if card is off-suit we need to record
		if initial_suit != suit:
			# if self.off_suit[player_id] does not exist, create the key, value pair
			if player_id not in self.off_suit.keys():
				self.off_suit[player_id] = list()
			
			# if we do not already know that the player does not have this suit
			if initial_suit not in self.off_suit[player_id]:
				self.off_suit[player_id].append(initial_suit)

		# reduces suit count for card played
		self.suits[suit] -= 1

		if not self.hearts_broken and suit == 1:
			self.hearts_broken = True

	def end_turn(self):
		"""
			at the end of a turn, the center is cleared
		"""
		self.current_center = list()
		self.turn_number += 1

	def start_round(self):
		"""
			at the end of a round, we increment the round counter
		"""
		self.round_number += 1

	def set_players(self, player_count):
		"""
			sets the number of players in the game
			this is for SmartPlayer to determine how many players
			are left to play after their card
		"""
		self.player_count = player_count

	def track_cards_received(self, cards, player_id):
		"""
			for each card received, add the value to the player if heart or queen of spades
		"""
		# if card is queen of spades
		for card in cards:
			if card == 10:
				# add the player_id to the list of who received the queen of spades
				self.queens.append(player_id)
				self.points_received[player_id] += 13
			# if card is a heart
			elif card // 13 == 1:
				self.points_received[player_id] += 1