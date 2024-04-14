from src import mahjong

game = mahjong.Game()
question = game.play()
game.execute()
print(question)
# next_question = question.answer("feng2")
