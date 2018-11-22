from Player import Player

class SmartPlayer(Player):
	"""
		Player that makes decisions based on logic written down
		The main goal is to create an artificial intelligence that can
		play Hearts, but for now, we need a basis on how to play
		in order to create a ranking system with ELO
	"""

	def take_turn(self, initial, first_card=None, hearts_broken=False):
		print(self.tracker)
		return super(SmartPlayer, self).take_turn(initial, first_card, hearts_broken)


	def add_tracker(self, tracker):
		self.tracker = tracker