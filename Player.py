class Player():

	def __init__(self, name):
		self.name = name
		self.hand = None
		self.cards_won = list()
		self.score = 0
		self.valid = False

	def take_turn(self, initial, first_card=None, hearts_broken=False):
		"""
			player chooses card to play if he has a card
			should never reach here if hand is empty
		"""
		print(self.name + ", it is your turn.")
		if len(self.hand.deck_array) <= 0:
			return None

		# reset self.valid
		self.valid = False

		while not self.valid:
			for i in range(len(self.hand.deck_array)):
				print(str(i), self.hand.deck_array[i])
			card_index = input("Which card will you play?\n")
			if not card_index:
				print("Please type the number next to the card you want to play and press enter.\n")
				continue
			print()
			card_index = int(card_index)

			if self.check_play_validity(self.hand.int_deck_array[card_index], initial, first_card, hearts_broken):
				self.valid = True
			else:
				print("Card was not valid to be played.\n")

		card = self.hand.deck_array[card_index]
		self.hand.remove_card(card_index)
		return card

	def set_hand(self, hand):
		self.hand = hand

	def get_hand(self):
		return self.hand

	def score_pile(self, points):
		pile = Deck(self.cards_won)
		for card in pile.int_deck_array:
			suit = card // 13
			# every heart counts as a point, but queen of spades counts as 13
			if suit == 1:
				self.score += 1
			elif card == 12:
				self.score += 13

	def check_play_validity(self, card, initial, first_card, hearts_broken):
		"""
			check if this card is possible to be played considering
			the player's hand and the initial card played
		"""
		# if initial has not been set (this is the first card to be played), all cards are viable
		if not initial:
			# if card is the first in the round, must be 2 of clubs
			if first_card and card != first_card:
				if first_card = 40:
					c = "2♣"
				else:
					c = "3♣"
				print("You must play " + c + " as the initial card for this round.")
				return False
			# cannot play hearts unless hearts have been broken or you only have hearts left
			# if suit is hearts and ((hearts are not broken) or all cards in hand are hearts)
			suit = card // 13
			suits_in_hand = list(map(lambda x: x // 13, self.hand.int_deck_array))
			if suit == 1 and ((not hearts_broken) or all(suit == s for s in suits_in_hand)):
				if not hearts_broken:
					reason = "Hearts have not been broken."
				else:
					reason = "You have a card that is not a heart."
				print("You cannot play a heart. " + reason)
				return False
			return True
		# if not first card, must abide by the first card played
		else:
			suit = card // 13
			suit_initial = initial // 13
			suits_in_hand = list(map(lambda x: x // 13, self.hand.int_deck_array))

			# if card played is not the same suit and you have the same suit in you hand
			if suit != suit_initial and suit_initial in suits_in_hand:
				print("You have to play the same suit as the initial card.")
				return False
			return True


	def get_number_hand(self):
		return self.hand.int_deck_array

	def add_to_pile(self, cards_won):
		"""
			when a player wins a turn, he takes the card and adds it to his pile (self.cards_won)
		"""
		print(cards_won)
		for card in cards_won:
			self.cards_won.append(card)