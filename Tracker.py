class Tracker():

	def __init__(self):
		self.refresh()

	def refresh(self):
		self.cards_played = list()
		self.cards_left = 52
		self.hearts_broken = False
		self.current_center = list()

		# suits counts so we can reduce times calculated
		# allows us to know how many of each suit are left
		# 0=spades, 1=hearts, 2=diamonds, 3=clubs
		self.suits = {0:13, 1:13, 2:13, 4:13}

		# we need to track is someone is out of a suit so we can predict their play
		# dict of lists, where player_id provides list of suits player no longer has
		self.off_suit = dict()

	def card_played(self, card, player_id):
		"""
			tracks the card played and which player played it
			player is the player id from the game, not the player object
			if player plays off-suit card, we know he does not have that suit
		"""
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
		self.current_center = list()