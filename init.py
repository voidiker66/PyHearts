from Game import Game, Player

game = Game(debug=True)
game.add_player(Player("Austin", debug=True))
game.add_player(Player("Alex", debug=True))
game.add_player(Player("Mom", debug=True))
game.add_player(Player("Dad", debug=True))
game.play()