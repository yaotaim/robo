from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

bot = ChatBot("チャットボット試作版", storage_adapter="chatterbot.storage.SQLStorageAdapter", database_uri="sqlite:///tanaka.sqlite3")

trainer = ListTrainer(bot)
training_ = ["こんにちは", "こんにちは！", "元気ですか？", "元気です！"]
trainer.train(training_)
