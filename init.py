from Game import Game, Player
from Tracker import Tracker
from SmartPlayer import SmartPlayer

tracker = Tracker()
ai = SmartPlayer("Austin", debug=True)
ai.add_tracker(tracker)

game = Game(tracker=tracker, debug=True)
game.add_player(ai)
game.add_player(Player("Alex", debug=True))
game.add_player(Player("Mom", debug=True))
game.add_player(Player("Dad", debug=True))
game.play()