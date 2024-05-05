import random


def get_random_compliment() -> str:
    with open("compliments.txt", "r", encoding="UTF-8") as file:
        lines = file.readlines()
        random_line = random.choice(lines)
        random_string = random_line.strip()
        return random_string
