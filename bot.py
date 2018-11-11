import random
from enum import Enum
from pathlib import Path
from typing import Callable

import discord
import requests
from discord import Client, Message
from discord.ext import commands
from word2number.w2n import word_to_num

class NumbersAPI:
    class Categories(Enum):
        TRIVIA = 'trivia'
        YEAR = 'year'
        MATH = 'math'
        RANDOM = 'random'

        @classmethod
        def non_random(cls):
            return [category for category in cls if category != cls.RANDOM]

    def __init__(self):
        self.client = requests.Session()

    def get(self, number: int, category: 'NumbersAPI.Categories'):
        if category == NumbersAPI.Categories.RANDOM:
            non_random_categories = self.Categories.non_random()
            for cat in random.sample(non_random_categories, len(non_random_categories)):
                try:
                    return self.__ask_trivia(number, cat)
                except ValueError:
                    pass
                raise ValueError
        return self.__ask_trivia(number, category)

    def __ask_trivia(self, number, category: 'NumbersAPI.Categories'):
        NUMBERS_API = 'http://numbersapi.com'
        resp = self.client.get(
            '/'.join([NUMBERS_API, str(number), category.value]), params={'json': True})
        resp.raise_for_status()
        json = resp.json()
        if not json['found']:
            raise ValueError("Boring number is boring")
        return json['text']


class IOClient():
    def event(self, func: Callable):
        setattr(self, func.__name__, func)

    def run(self, token):
        self.on_ready()
        while True:
            self.on_message(discord.Message(content=input('Dissy:')))


client = commands.Bot(command_prefix='#')


def main():
    print("Reloading...")
    FILE_DIR = Path(__file__).parent
    token_file = FILE_DIR/'secrets'/'token.txt'
    client.run(token_file.read_text())


def find_number(sentance: str)->int:
    try:
        return word_to_num(sentance)
    except ValueError: # No number that is a word
        for word in sentance.split():
            try:
                return int(word)
            except ValueError:
                pass
    raise ValueError("No number found in sentane")


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return
    try:
        num = find_number(message.content)
        print(f"number found {num}")
        api = NumbersAPI()
        resp = api.get(num, api.Categories.RANDOM)
        print(resp)
        await client.send_message(message.channel, resp)
    except ValueError:
        pass


@client.event
async def on_ready():
    FILE_DIR = Path(__file__).parent
    client_id = FILE_DIR/'secrets'/'client_id.txt'
    permissions = 2048
    invite_link = f'https://discordapp.com/oauth2/authorize?&client_id={client_id.read_text()}&scope=bot&permissions={permissions}'
    print(f"Bot running! Invite me at {invite_link}")

if __name__ == '__main__':
    main()
