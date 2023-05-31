import asyncio
from disnake.ext import commands
from riotCommands import *
from apikeys import *
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user} has logged on')

@bot.slash_command(name="lol", description="Takes player's info from solo queue")
async def lolCommand(inter, player):
    print("Start")
    await inter.response.defer() # tell Discord what the bot is thinking, by processing the information received from the user
    await asyncio.sleep(3.4)
    await lol(inter, player)


bot.run(token)