from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

bot = ChatBot("チャットボット試作版")

training_ = open('chat.txt', 'r').readlines()
training2_ = open('chat2.txt', 'r').readlines()

trainer = ListTrainer(bot)

trainer.train(training_)
trainer.train(training2_)

while True:
    try:
        bot_input = bot.get_response(input())
        print(bot_input)
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
