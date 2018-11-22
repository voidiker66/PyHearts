class Tracker():

	def __init__(self):
		self.refresh()

	def refresh(self):
		self.cards_played = list()
		self.cards_left = 52
		self.hearts_broken = False
		self.current_center = list()

	def card_played(self, card):
		self.current_center.append(card)
		self.cards_played.append(card)
		self.cards_left -= 1

		if not self.hearts_broken and card // 13 == 1:
			self.hearts_broken = True

	def end_turn(self):
		self.current_center = list()