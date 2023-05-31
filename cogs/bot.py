import asyncio
from disnake.ext import commands
from riotCommands import *
from apikeys import *
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user} has logged on')

@bot.slash_command(name="lol", description="Takes player's info from solo queue")
async def lolSoloQueueCommand(inter, player):
    await inter.response.defer() # tell Discord what the bot is thinking, by processing the information received from the user
    await asyncio.sleep(3.4)
    await lolSoloQueue(inter, player)
    print(player)

@bot.slash_command(name="lolflex", description="Takes player's info from flex queue")
async def lolFlexCommand(inter, player):
    print("Start")
    await inter.response.defer()
    await asyncio.sleep(3.4)
    await lolFlex(inter, player)
    print(player)


bot.run(token)