import random


def get_random_word():
    with open("words.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    return random.choice(lines)
