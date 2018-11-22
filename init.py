from Game import Game, Player
from Tracker import Tracker

game = Game(tracker=Tracker(), debug=True)
game.add_player(Player("Austin", debug=True))
game.add_player(Player("Alex", debug=True))
game.add_player(Player("Mom", debug=True))
game.add_player(Player("Dad", debug=True))
game.play()