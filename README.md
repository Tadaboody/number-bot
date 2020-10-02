# Mathbot
[![Uptime Robot status](https://img.shields.io/uptimerobot/status/m781443243-d947be8fe240aa4811f5ebcc.svg)](https://discordapp.com/oauth2/authorize?&client_id=508)

---
Interrupts you with ~~hopefully~~ interesting and relevant number facts!
[Add them to your server today!](https://discordapp.com/oauth2/authorize?&client_id=508)

Number facts are supplied thanks to [numbersapi](http://numbersapi.com/#42)

## Dependencies:
- Python 3.6+
- All packages in listed in [requirements.txt](requirements.txt)
## Getting a token:
The token in secrets/token.txt and client ID in client_id.txt need to be replaced with discord API token.
Instructions on getting a token can be found [here](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
## Running
```sh
python3 -m venv venv --prompt number-bot
source venv/bin/activate
pip install -r requirements.txt
# Put bot token in token.txt and app Client ID in client_id.txt
python bot.py
```
