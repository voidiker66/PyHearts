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
		self.tracker = tracker

	def get_valid_cards(self, initial, first_card, hearts_broken):
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

		# based on this policy, the card has this value at being played
		# right now, we just use 1 because we have yet to write the policy
		return 1


