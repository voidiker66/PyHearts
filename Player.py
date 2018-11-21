from Deck import Deck

# temporary to automate gameplay
# import random

class Player():

	def __init__(self, name, debug=False):
		self.name = name
		self.hand = None
		self.cards_won = list()
		self.score = 0
		self.valid = False
		self.output_debug = debug

	def debug(self, message='', end='\n'):
		if self.output_debug:
			print(message, end=end)

	def take_turn(self, initial, first_card=None, hearts_broken=False):
		"""
			player chooses card to play if he has a card
			should never reach here if hand is empty
		"""
		self.debug(self.name + ", it is your turn.")
		if len(self.hand.deck_array) <= 0:
			return None

		# reset self.valid
		self.valid = False

		# temporary to automate gameplay
		# card_index = len(self.hand.deck_array)
		# r = len(self.hand.deck_array) - 1

		while not self.valid:
			# print out Player's hand
			for i in range(len(self.hand.deck_array)):
				print(str(i), self.hand.deck_array[i])

			# get index of the card in the Player's hand
			# user input must be an int associated with the index of the hand
			try:
				card_index = int(input("Which card will you play?\n"))
				if card_index == '':
					self.debug("Please type the number next to the card you want to play and press enter.\n")
					continue
				if card_index < 0 or card_index >= len(self.hand.deck_array):
					self.debug("This is not a valid choice.")
					continue
			except ValueError:
				self.debug("The user input was not a number.")
				continue

			# temporary to automate gameplay
			# card_index = random.randint(0, r)

			if self.check_play_validity(self.hand.int_deck_array[card_index], initial, first_card, hearts_broken):
				self.valid = True
			else:
				self.debug("Card was not valid to be played.\n")

		card = self.hand.deck_array[card_index]
		self.hand.remove_card(card_index)
		return card

	def set_hand(self, hand):
		self.hand = hand

	def get_hand(self):
		return self.hand

	def score_pile(self):
		score_increase = 0
		pile = Deck(self.cards_won)
		for card in pile.int_deck_array:
			suit = card // 13
			# every heart counts as a point, but queen of spades counts as 13
			if suit == 1:
				score_increase += 1
			elif card == 10:
				score_increase += 13
		# we won all the points, so our score goes down by 26
		if score_increase == 26:
			score_increase *= -1

		# now we can add the score increase to our score
		self.score += score_increase	

		# if the end result of scoring is a score that's a multiple of 50
		# we subtract 50 from the score, but only if the score increased to 50 this round
		# and is not zero
		if self.score % 50 == 0 and score_increase != 0 and self.score != 0:
			self.score -= 50

	def check_play_validity(self, card, initial, first_card, hearts_broken):
		"""
			check if this card is possible to be played considering
			the player's hand and the initial card played
		"""
		# if initial has not been set (this is the first card to be played), all cards are viable
		if not initial:
			# if card is the first in the round, must be 2 of clubs
			if first_card and card != first_card:
				if first_card == 39:
					c = "2♣"
				else:
					c = "3♣"
				self.debug("You must play " + c + " as the initial card for this round.")
				return False

			# cannot play hearts unless hearts have been broken or you only have hearts left
			suit = card // 13
			suits_in_hand = list(map(lambda x: x // 13, self.hand.int_deck_array))

			# if card is a heart
			if suit == 1:
				# if all the cards in the hand are hearts, we can play a heart
				if all(suit == s for s in suits_in_hand):
					return True
				# if not, check if hearts have been broken
				else:
					if not hearts_broken:
						reason = "Hearts have not been broken."
					else:
						reason = "You have a card that is not a heart."
				self.debug("You cannot play a heart. " + reason)
				return False
			return True
		# if not first card, must abide by the first card played
		else:
			suit = card // 13
			suit_initial = initial // 13
			suits_in_hand = list(map(lambda x: x // 13, self.hand.int_deck_array))

			# if card played is not the same suit and you have the same suit in you hand
			if suit != suit_initial and suit_initial in suits_in_hand:
				self.debug("You have to play the same suit as the initial card.")
				return False
			return True


	def get_number_hand(self):
		return self.hand.int_deck_array

	def add_to_pile(self, cards_won):
		"""
			when a player wins a turn, he takes the card and adds it to his pile (self.cards_won)
		"""
		for card in cards_won:
			self.cards_won.append(card)