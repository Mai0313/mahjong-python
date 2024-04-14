from src.mahjong import Game, Hand, Round
from rich.console import Console

console = Console()


game = Game()
question = game.play()
round = Round(game)
hand = Hand(round)
console.print(hand.players)
hand.shuffle()
hand.deal()
console.print(hand.players)
