import random
import math


class Deck():

	def __init__(self, deck_array=None):
		"""
			Deck can either be the game deck to be dealt out
			or can be the hand a Player has, based on whether
			we set deck_array in the initialization
			if not set, we create a full deck
			if not, we want the Player's hand to have the same
			functions as the regular deck but with only so many cards
		"""
		self.heart = '♥'
		self.diamond = '♦'
		self.spade = '♠'
		self.club = '♣'

		# map number and suit to num value
		# Spade 1-13, Heart 1-13, Club 1-13, Diamond 1-13
		self.suit_array = ['Spade', 'Heart', 'Club', 'Diamond']
		self.char_suit_dict = {'♠': 0, '♥': 1, '♦': 2, '♣': 3}

		if deck_array:
			self.deck_array = deck_array
			self.int_deck_array = self.hand_cards_to_hand_numbers(self.deck_array)

			# sort the hands
			self.deck_array.sort(key=self.map_card_to_number_value)
			self.int_deck_array.sort()
			return

		self.deck_array = list()
		# initialize deck
		for x in range(1,14):
			val = str(x)
			if x == 1:
				val = 'A'
			if x == 11:
				val = 'J'
			if x == 12:
				val = 'Q'
			if x == 13:
				val = 'K'

			self.deck_array.append(val + self.heart)
			self.deck_array.append(val + self.diamond)
			self.deck_array.append(val + self.spade)
			self.deck_array.append(val + self.club)

		self.int_deck_array = self.hand_cards_to_hand_numbers(self.deck_array)

		# sort the decks
		self.deck_array.sort(key=self.map_card_to_number_value)
		self.int_deck_array.sort()

		# print the face value and associated number value for each card
		# for i in range(52):
		# 	print(self.deck_array[i], str(self.int_deck_array[i]))

	def shuffle_deck(self):
		"""
			randomizes the cards in the deck
		"""
		random.shuffle(self.deck_array)

	def hand_cards_to_hand_numbers(self, hand):
		"""
			maps the entire hand from the face value to the integer value
		"""
		ret = []
		for card in hand:
			ret.append(self.map_card_to_number_value(card))
		return ret

	def map_card_to_number_value(self, value):
		"""
			maps the face value of the card to the integer value
			Aces are high, so we count it as 13, not 1
		"""
		# if length is 3, we know it is a 10 of a suit
		if len(value) == 3:
			suit_val = self.char_suit_dict.get(value[2]) * 13
			suit_val += 8
		else:
			suit_val = self.char_suit_dict.get(value[1]) * 13
			if value[0] == 'A':
				suit_val += 12
			elif value[0] == 'J':
				suit_val += 9
			elif value[0] == 'Q':
				suit_val += 10
			elif value[0] == 'K':
				suit_val += 11
			else:
				suit_val += (int(value[0]) - 2)
		return suit_val

	def get_key_from_val(self, val, dicter):
		"""
			helper function for mapping
		"""
		for key in dicter.keys():
			if dicter[key] == val:
				return key

	def hand_numbers_to_hand_cards(self, int_hand):
		"""
			maps the entire hand from the integer value to the face value
		"""
		ret = []
		for card in int_hand:
			ret.append(self.map_card_to_hand(card))
		return ret

	def map_card_to_hand(self, value):
		"""
			maps the integer value of the card to the face value
		"""
		if value / 13 == 4:
			suit = '♣'
		else:
			suit = self.get_key_from_val(math.floor(value / 13), self.char_suit_dict)
		num = value % 13
		card = num
		if num == 1:
			card = 'A'
		if num == 11:
			card = 'J'
		if num == 12:
			card = 'Q'
		if num == 0:
			card = 'K'
		return str(card) + suit

	def remove_card(self, index):
		"""
			removes the card from the deck
			I use this after Player plays a card
			should never be used in the actual gameplay
		"""
		self.deck_array.pop(index)
		self.int_deck_array.pop(index)

	def convert_external_card_to_int(self, card):
		return self.map_card_to_number_value(card)