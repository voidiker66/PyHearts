from Game import Game, Player
from Tracker import Tracker
from SmartPlayer import SmartPlayer

tracker = Tracker()
austin = SmartPlayer("Austin", debug=True)
austin.add_tracker(tracker)

alex = SmartPlayer("Alex", debug=True)
alex.add_tracker(tracker)

mom = SmartPlayer("Mom", debug=True)
mom.add_tracker(tracker)

dad = SmartPlayer("Dad", debug=True)
dad.add_tracker(tracker)

game = Game(tracker=tracker, debug=True)
game.add_player(austin)
game.add_player(alex)
game.add_player(mom)
game.add_player(dad)
game.play()