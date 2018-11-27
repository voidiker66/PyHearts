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

		# get the card with the max policy value in this situation
		# need to fix because max() returns the value not the card
		card_index = max(list(map(lambda v: self.policy(v), self.hand)))

		# this is the card we should play according to our policy
		card = self.hand.deck_array[card_index]
		self.hand.remove_card(card_index)
		return card


	def add_tracker(self, tracker):
		self.tracker = tracker

	def policy(self, card):
		"""
			assigns a point value to the card based on the
			potential benefits of playing the card in this situation
		"""
		return 1