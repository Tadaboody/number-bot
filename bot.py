import random
from enum import Enum
from pathlib import Path

import aiohttp
import discord
from word2number.w2n import word_to_num


class NumbersAPI:
    class Categories(Enum):
        TRIVIA = "trivia"
        YEAR = "year"
        MATH = "math"
        RANDOM = "random"

        @classmethod
        def non_random(cls):
            return [category for category in cls if category != cls.RANDOM]

    async def get(self, number: int, category: "NumbersAPI.Categories"):
        if category == NumbersAPI.Categories.RANDOM:
            non_random_categories = self.Categories.non_random()
            random.shuffle(non_random_categories)
            for cat in non_random_categories:
                try:
                    return await self.__ask_trivia(number, cat)
                except ValueError:
                    pass
        return await self.__ask_trivia(number, category)

    async def __ask_trivia(self, number, category: "NumbersAPI.Categories"):
        NUMBERS_API = "http://numbersapi.com"
        url = "/".join([NUMBERS_API, str(number), category.value])
        async with aiohttp.request("GET", url, params={"json": "true"}) as resp:
            resp.raise_for_status()
            json = await resp.json()
        if not json["found"]:
            raise ValueError(f"{number} is boooring")
        return json["text"]


FILE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = FILE_DIR / "secrets"


def main():
    print("Reloading...")
    token_file = SECRETS_DIR / "token.txt"
    id_file = SECRETS_DIR / "client_id.txt"
    Numbie(id_file.read_text()).run(token_file.read_text())


def find_number(sentance: str) -> int:
    try:
        return word_to_num(sentance)
    except ValueError:  # No word that is a number
        import re

        match = re.search(r"(\d+)", sentance)
        if match:
            return match[0]
    raise ValueError("No number found in sentence")


class Numbie(discord.Client):
    def __init__(self, client_id: str,**kwargs):
        self.client_id = client_id
        super().__init__(**kwargs)

    async def on_message(self, message: discord.Message):
        print(self.user.display_name)
        if message.author == self.user:
            return
        try:
            num = find_number(message.content)
            print(f"number found {num}")
            api = NumbersAPI()
            resp = await api.get(num, api.Categories.RANDOM)
            print(resp)
            await message.channel.send(resp)
        except ValueError as e:
            print(e)

    async def on_ready(self):
        client_id = SECRETS_DIR / "client_id.txt"
        permissions = 2048
        invite_link = f"https://discordapp.com/oauth2/authorize?&client_id={client_id.read_text()}&scope=bot&permissions={permissions}"
        print(f"Bot running! Invite me at {invite_link}")


if __name__ == "__main__":
    main()
