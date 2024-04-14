r'''# comment out this opening triple quote to time Wu computation
import mahjong, time
start = time.time()
w = mahjong.melds.Wu.from_str("""
tong/4|tong/4|tong/4|tong/5|tong/6|tong/6|tong/6|tong/7
""".strip(),
melds=[mahjong.Pong.from_str('zhu/3|zhu/3|zhu/3'), mahjong.Chow.from_str('wan/1|wan/2|wan/3')],
arrived=mahjong.Tile.from_str('tong/4')
#map(mahjong.Chow.from_str, 'zhu/3|zhu/4|zhu/5,zhu/5|zhu/6|zhu/7,zhu/7|zhu/8|zhu/9'.split(','))
)
end = time.time()
console.log('\n'.join(f'{w.faan(meld)}: ' + ', '.join(str(i) for i in meld)
                for meld in set(tuple(meld) for meld in w.melds)))
console.log(w.max_faan())
console.log(f'in {end-start:.2f}s')
# comment out this opening triple quote to test dealing
from mahjong import Game, Round, Hand
game = Game()
round = Round(game)
hand = Hand(round)
hand.shuffle()
hand.deal()
for p in game.players:
    console.log('|'.join(map(str, p.hand)))
    console.log(', '.join(map(str, p.bonus)))
'''

import sys

from rich.console import Console

from mahjong.game import Game, Hand, UserIO, Question, HandEnding, HandResult

console = Console()

if "--game" in sys.argv:
    game = Game(extra_hands=False)
else:
    game = Hand(None)
console.log("Note: all indexes are **1-based**.")
console.log("This is a rudimentary text-based mahjong implementation.")
console.log("It's purely as a proof-of-concept/manual testing method.")
console.log("It requires trust that each player won't look at the other's privacy.")
console.log("Please don't actually use this. Make something even a tiny bit better.")
console.log("With that said, let's start.")

question = game.play()
while question is not None:
    if isinstance(question, UserIO):
        if question.question == Question.READY_Q:
            input("Hit Enter when ready for the next round.")
            question = question.answer()
            continue
        hand_minus_tile = [tile for tile in question.hand if tile is not question.arrived]
        console.log("Question for Player #%s" % question.player.seat.value)
        console.log(
            "Draw/Last discard: %s;" % question.arrived,
            "Concealed:",
            ", ".join(map(str, hand_minus_tile)),
        )
        console.log(
            "Shown:",
            "\t".join(map(str, question.shown)),
            "- Bonuses:",
            "|".join(map(str, question.player.bonus)),
        )
        if question.question == Question.DISCARD_WHAT:
            idx = int(input("Enter index of card to discard. 0 for draw. "))
            if idx == 0:
                if question.arrived in question.hand:
                    tile = question.arrived
                else:
                    tile = hand_minus_tile[0]
            elif idx > 0:
                tile = hand_minus_tile[idx - 1]
            elif idx < 0:
                tile = hand_minus_tile[idx]
            else:
                tile = hand_minus_tile[0]
            console.log("Discarding", tile)
            question = question.answer(tile)
        elif question.question == Question.MELD_FROM_DISCARD_Q:
            assert question.melds is not None
            console.log("Available melds to meld:", "\t".join(map(str, question.melds)))
            try:
                idx = int(input("Enter index of meld to meld, or blank to not meld: "))
            except ValueError:
                question = question.answer(None)
            else:
                question = question.answer(question.melds[idx - 1])
        elif question.question == Question.SHOW_EKFCP_Q:
            assert question.melds is not None
            console.log(
                "Available Kongs to expose from concealed Pongs:",
                "\t".join(map(str, question.melds)),
            )
            try:
                idx = int(input("Enter index of Kong to expose, or blank to not expose: "))
            except ValueError:
                question = question.answer(None)
            else:
                question = question.answer(question.melds[idx - 1])
        elif question.question == Question.SHOW_EKFEP_Q:
            assert question.melds is not None
            console.log(
                "Available Kongs to expose from exposed Pongs:",
                "\t".join(map(str, question.melds)),
            )
            try:
                idx = int(input("Enter index of Kong to expose, or blank to not expose: "))
            except ValueError:
                question = question.answer(None)
            else:
                question = question.answer(question.melds[idx - 1])
        elif question.question == Question.ROB_KONG_Q:
            assert question.melds is not None
            console.log("You can rob the last Kong to win with:", question.melds[0])
            inp = "?"
            while inp not in {"y", "n"}:
                inp = input("Do you want to? (y/n) ").casefold()
            question = question.answer(inp == "y")
        elif question.question == Question.WHICH_WU:
            assert question.melds is not None
            idx = int(input("Which Wu combo (enter index) do you want to win with? "))
            question = question.answer(question.melds[idx - 1])
    elif isinstance(question, HandEnding):
        if question.result == HandResult.GOULASH:
            console.log("Goulash! Nobody wins. Starting next game...")
        else:
            assert question.choice is not None
            console.log(
                "Player #%s won with %s (%s faan; %s points; %s)! Starting next game..."
                % (
                    question.winner.seat.value,
                    ",".join(map(str, question.choice)),
                    question.faan()[0],
                    *question.points(1),
                )
            )
        question = question.answer()
console.log("Game Over!")
