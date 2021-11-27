from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Creating ChatBot Instance
chatbot = ChatBot('GitIssueBot')

# Training with Personal Ques & Ans
conversation = [
    "Hello",
    "Hi there!",
    "Hey",
    "Hi there!",
    "Hi",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "yes",
    "I am here to help! Can you please tell me issue in short?",
    "y",
    "I am here to help! Can you please tell me issue in short?",
    "no",
    "Thank you for your time, happy to help!",
    "No",
    "Thank you for your time, happy to help!"
]

trainer = ListTrainer(chatbot)
trainer.train(conversation)

