from Player import Player

class SmartPlayer(Player):
	"""
		Player that makes decisions based on logic written down
		The main goal is to create an artificial intelligence that can
		play Hearts, but for now, we need a basis on how to play
		in order to create a ranking system with ELO
	"""

	def take_turn(self, initial, first_card=None, hearts_broken=False):
		# return super(SmartPlayer, self).take_turn(initial, first_card, hearts_broken)

		# create a dict of (card : point_value) pairs based on the policy
		points = list(map(lambda v: self.policy(v), self.get_valid_cards(initial, first_card, hearts_broken)))

		# get the card with the max policy value in this situation
		# if multiple with the same value, chooses the first (should not matter)
		# only problem I see is that we prioritize lower cards over higher cards
		# meaning - 1, 2, 3, etc for each suit, and spade, hearts, diamonds, clubs for suits
		card_index = max(points.keys(), key=(lambda i: points[i]))

		# this is the card we should play according to our policy
		card = self.hand.deck_array[card_index]
		self.hand.remove_card(card_index)
		return card


	def add_tracker(self, tracker):
		"""
			adds the tracker to the player object
			tracker is the same tracker inside the game object (if init is done correctly)
		"""
		self.tracker = tracker

	def get_valid_cards(self, initial, first_card, hearts_broken):
		"""
			returns a list of the int values of all the cards in the hand that are valid to be played
		"""
		return list([c for c in self.hand.int_deck_array if self.check_play_validity(c, initial, first_card, hearts_broken)])

	def policy(self, card):
		"""
			assigns a point value to the card based on the
			potential benefits of playing the card in this situation
		"""

		# localize the variables for clarity
		# will need to change to self.tracker variables later because this
		# code is used many times in self.take_turn() and will cause memory problems
		cards_left = self.tracker.cards_left
		cards_played = self.tracker.cards_played
		hearts_broken = self.tracker.hearts_broken
		current_center = self.tracker.current_center
		current_player = self.tracker.current_player

		# get how many cards have been played before you
		# how many people are left to play after you is important
		play_count = len(current_center)

		"""
			we need to decide whether it is safe or not to beat the current hand state
				If we win, do we get points? If we lose, do we risk getter more points later?
			If first player:
				Will this suit result in hearts being played?
				Will this suit cause someone else to get the Queen of Spades?
				Is it safe for me to play a high card?
				Do I want to win this turn or should I pass the turn to someone else?
		"""
		# if we are the first to play, need to choose the initial card
		if self.play_count == 0:

			# if this is the first turn in the round, we obviously need to play 2 of clubs
			# so we treat 2 of clubs as 1e6 so that we know it is the max value
			if self.tracker.turn_number == 1:
				# we should always have 2 of clubs if we get here
				if 39 not in self.hand.int_deck_array:
					return -1

				# if card is 2 of clubs
				if card == 39:
					return 1e6
				else:
					return 1
			"""
				if not the first turn, we do not have to play 2 of clubs
				Priority of suits after first turn is:

				if queen of spades has not been played:
					if we do not have queen of spades:
						if we have spades other than king or ace of spades:
							play spades
						else:
							clubs or diamonds
					else (we have queen of spades):
						if we have more than (13 // len(players)) spades in our hand:
							we can play spades
						else:
							play suit with lowest card count, unless hearts
				else (queen of spades has been played):
					spades, clubs, and diamonds are equal value


				(else clubs or diamonds, or if spades equal to clubs or diamonds):
					either get rid of one suit, or pass along turn responsability to other player

					if cards are all low, low risk of winning any turn:
						pass turn to someone else
					else:
						if all cards are high and high risk of winning:
							if lowest count suit can be successfully gotten rid of:
								play suit
							else:
								you're fucked, but keep playing
						else (have low and high cards):
							play low to high
			"""
			# if first player to play this turn, but not restricted to 2 of clubs
			else:
				pass

		# based on this policy, the card has this value at being played
		# right now, we just use 1 because we have yet to write the policy
		return 1


