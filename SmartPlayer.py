from Player import Player

class SmartPlayer(Player):
	"""
		Player that makes decisions based on logic written down
		The main goal is to create an artificial intelligence that can
		play Hearts, but for now, we need a basis on how to play
		in order to create a ranking system with ELO
	"""

	def take_turn(self, initial, first_card=None, hearts_broken=False):
		# can't change function parameters because this is a overriding function

		# uncomment to just use the original function (only if do not want a smart player)
		# return super(SmartPlayer, self).take_turn(initial, first_card, hearts_broken)

		# get how many cards have been played before you
		# how many people are left to play after you is important
		play_count = len(self.tracker.current_center)

		# set the weights for each suit
		# default: spades=10, hearts=10, diamond=10, clubs=10
		suit_weights = self.get_weights(play_count)

		# create a dict of (card : point_value) pairs based on the policy
		points = dict()
		for c in self.get_valid_cards(initial, first_card, hearts_broken):
			points[c] = self.policy(c, suit_weights, play_count)

		# get the card with the max policy value in this situation
		# if multiple with the same value, chooses the first (should not matter)
		# only problem I see is that we prioritize lower cards over higher cards
		# meaning - 1, 2, 3, etc for each suit, and spade, hearts, diamonds, clubs for suits
		card_index = self.hand.int_deck_array.index(max(points.keys(), key=(lambda i: points[i])))

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

	def get_weights(self, play_count):
		"""
			returns the weight of each suit based on game conditions
		"""

		weights = {0:10, 1:10, 2:10, 3:10}

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

		# we need to weigh the rest of the suits based on conditions
		# so far only have spades if first pick, and if not first pick weigh initial suit

		# if we are the first to play, need to choose the initial card
		if play_count == 0:
			# if player has queen of spades (determine weights of spades)
			if 10 in self.hand.int_deck_array:
				# if we reasonably have more spades than anyone else
				# if (num spades left // len(num players that do not have an off suit or none of the off suits is spades)) less than spades in hand
				if (self.tracker.suits[0] // len(list([p for p in range(self.tracker.player_count) if not p in self.tracker.off_suit.keys() \
				or 0 not in self.tracker.off_suit[p]]))) < len(list([c for c in self.hand.int_deck_array if c // 13 == 0])):
					# treat spades with more weight
					"""
						if we play more spades, forces out higher spades?
						forces others to play off-suit, draining their hand?
					"""
					weights[0] *= 10
				# if we have only a few spades, need to conserve them and drain other suits
				else:
					weights[0] /= 10

			# do not have queen of spades in our hand
			else:
				# if queen of spades has already been played, we do not need to 
				# rush spades to force queen of spades. instead, focus on hearts
				if 10 in self.tracker.cards_played:
					pass

				# if queen of spades has not been played, we can choose to rush spades if 
				# we have more spades than ace or king, or we can play normally
				else:
					# if we reasonably have more spades than anyone else
					# if (num spades left // len(num players that do not have an off suit or none of the off suits is spades)) less than spades in hand
					if (self.tracker.suits[0] // len(list([p for p in range(self.tracker.player_count) if not p in self.tracker.off_suit.keys() \
					or 0 not in self.tracker.off_suit[p]]))) < len(list([c for c in self.hand.int_deck_array if c // 13 == 0])):
						weights[0] *= 10
					else:
						# if playing spades puts us at risk, we should avoid
						if 11 in self.hand.int_deck_array or 12 in self.hand.int_deck_array:
							weights[0] /= 5
						# if we can't force out queen ourselves, it is still a good option, but not a priority
						else:
							weights[0] *= 5

		# we have to follow the suit, so weigh the initial suit appropriately
		else:
			weights[self.tracker.current_center[0] // 13] = 100

		# our next objective is to get rid of an entire suit
		# even if we are not first, we need to weigh in case we don't have the initial suit
		for s in range(4):
			# weight of each suit inversely related to the amount of cards left of that suit in your hand
			weights[s] += (1.0 / ((1.0 + len(list([c for c in self.hand.int_deck_array if (c // 13) == s])))) ** 2)

		return weights

	def policy(self, card, suit_weights, play_count):
		"""
			assigns a point value to the card based on the
			potential benefits of playing the card in this situation
		"""

		# suit of the card to be evaluated
		suit = card // 13

		# how many points would be gained if we won
		points_weight = 0

		# weight card based on how high the card is (higher is better)
		card_weight = card % 13

		if play_count == 0:
			# if this is the first turn in the round, we obviously need to play 2 of clubs
			# so we treat 2 of clubs as 100 and all else as 1 so that we know it is the max value
			if self.tracker.turn_number == 1:
				# we should always have 2 of clubs if we get here
				if 39 not in self.hand.int_deck_array:
					return -1

				# if card is 2 of clubs
				if card == 39:
					return 100
				else:
					return 1

			# if first card this turn, but not the first card this round (not restricted to 2 of clubs)
			else:
				risk_score = 0
				return suit_weights[suit] + risk_score + card_weight
		else:
			# if we are the last to play, we can potentially choose to take the turn or give it up
			if play_count == 3:
				# counts how many hearts are in the center
				points = list([c // 13 for c in self.tracker.current_center]).count(1)

				# if queen of spades in center
				if 10 in self.tracker.current_center:
					points += 13

				initial_suit = self.tracker.current_center[0] // 13

				# does this card win the hand? if card is the same suit as initial and is higher than the other cards in center of initial suit
				wins_turn = (initial_suit == suit) and card > max(list([c for c in self.tracker.current_center if (c // 13) == initial_suit]))

				# if it wins, we want to make sure the points are small
				if wins_turn:
					# weight card based on the inverse of points gained
					points_weight = 1.0 / ((points + 1.0) ** 2)


			"""
				we need to decide whether it is safe or not to beat the current hand state
					If we win, do we get points? If we lose, do we risk getter more points later?
				If first player:
					Will this suit result in hearts being played?
					Will this suit cause someone else to get the Queen of Spades?
					Is it safe for me to play a high card?
					Do I want to win this turn or should I pass the turn to someone else?
			"""

			# based on this policy, the card has this value at being played
			# highest card that can be played of the best suit that won't give us too many points
			return suit_weights[suit] - points_weight + card_weight


