import disnake
from disnake.ext import commands
from apikeys import *
import asyncio
from riotwatcher import LolWatcher, ApiError
bot = commands.Bot(command_prefix='!')

api_key = league_of_legendsAPI
my_region = 'br1' # save the region that will be used to find player's status


async def lolSoloQueue(inter, player):
    watcher = LolWatcher(api_key)
    try:
        status = watcher.summoner.by_name(my_region, player) # player's basic status
        ranked_status_player = watcher.league.by_summoner(my_region, status['id']) # player's ranked status (solo/duo and flex)
        champid = watcher.champion_mastery.by_summoner(my_region, status['id'])  # return champ id 240(id) -> kled
        latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']  # get lol's last version about 'n' and about the champions
        static_champion_list = watcher.data_dragon.champions(latest, False, 'pt_BR')  # get champions static info
        champ_key = champid[0]['championId']
        '''
        "champid" was getting an id of the player's main champion. 
        So, in sintaxe, we convert to champ_key to find in champion_name ( return player's main champion basic status )
        '''

        embed = disnake.Embed(title=status['name'], type='rich')

        solo_queue = None

        for queue in ranked_status_player:
            if queue['queueType'] == 'RANKED_SOLO_5x5':
                solo_queue = queue
                break

        if solo_queue:
            embed.add_field(inline=False, name='Queue Type', value='Solo/Duo')
            embed.add_field(inline=True, name='Wins', value=str(solo_queue['wins']))
            embed.add_field(inline=True, name='Losses', value=str(solo_queue['losses']))
            embed.add_field(inline=True, name='LPs', value=str(solo_queue['leaguePoints']))
            embed.add_field(inline=True, name='Tier', value=str(solo_queue['tier']))
            embed.add_field(inline=True, name='Rank', value=str(solo_queue['rank']))

            wins = int(solo_queue.get('wins'))
            losses = int(solo_queue.get('losses'))
            win_rate = (wins / losses)

            embed.add_field(inline=True, name='Win Rate', value=("%.2f" % win_rate))
            embed.add_field(inline=False, name='', value='')
            champion_name = next(
                (champ['name'] for champ in static_champion_list['data'].values() if champ['key'] == str(champ_key)), None)
            '''
            champ['name'] is getting the value of name in static_champion_list (dictionary).
            So when 'if' starts, the id from static_champion_list stored on champ will pass through an equal test, confirming if champ['key'] is equal to champions key.
            '''
            if champion_name:
                embed.add_field(inline=True, name="Main Champ", value=champion_name)
            mastery_points = champid[0]['championPoints']
            embed.add_field(inline=True, name='Mastery Points', value=(f"{mastery_points:,}".replace(',', '.')))
        elif IndexError:
                embed.add_field(name='No Rank', value=(f"{player} has no ranked matches yet."))
        else:
                embed.add_field(name='No Matches', value=(f"{player} has no flex ranked matches yet, try !lolflex."))

        await inter.followup.send(embed=embed)
    except ApiError as e:
        await inter.followup.send(f"Error: {e}")




async def lolFlex(inter, player):
    watcher = LolWatcher(api_key)
    print(player)
    try:
        status = watcher.summoner.by_name(my_region, player)
        ranked_status_player = watcher.league.by_summoner(my_region, status['id'])
        champid = watcher.champion_mastery.by_summoner(my_region, status['id'])  # return champ id 240(id) -> kled
        latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']  # get lol's last version about 'n' and about the champions
        static_champion_list = watcher.data_dragon.champions(latest, False, 'pt_BR')  # get champions static info
        champ_key = champid[0]['championId']

        embed = disnake.Embed(title=status['name'], type='rich')

        flex_queue = None  # variable to get and save the flex queue, if exist

        for queue in ranked_status_player:
            if queue['queueType'] == 'RANKED_FLEX_SR':
                flex_queue = queue
                break

        if flex_queue:
            embed.add_field(inline=False, name="Queue Type", value='Flex')
            embed.add_field(inline=True, name='Wins', value=str(flex_queue['wins']))
            embed.add_field(inline=True, name='Losses ', value=str(flex_queue['losses']))
            embed.add_field(inline=True, name='LPs', value=str(flex_queue['leaguePoints']))
            embed.add_field(inline=True, name='Tier', value=str(flex_queue['tier']))
            embed.add_field(inline=True, name='Rank', value=str(flex_queue['rank']))

            wins = int(flex_queue.get('wins'))
            losses = int(flex_queue.get('losses'))
            win_rate = (wins / losses)

            embed.add_field(inline=True, name='Win Rate', value=("%.2f" % win_rate))
            embed.add_field(inline=False, name='', value='')
            champion_name = next(
                (champ['name'] for champ in static_champion_list['data'].values() if champ['key'] == str(champ_key)),
                None)
            if champion_name:
                embed.add_field(inline=True, name="Main Champ", value=champion_name)
            mastery_points = champid[0]['championPoints']
            embed.add_field(inline=True, name='Mastery Points', value=(f"{mastery_points:,}".replace(',', '.')))
        elif IndexError:
            embed.add_field(name='No Rank', value=(f"{player} has no ranked matches yet."))
        else:
            embed.add_field(name='No Matches', value=(f"{player} has no flex ranked matches yet, try !lol."))

        await inter.followup.send(embed=embed)
    except ApiError as e:
        await inter.followup.send(f"Error: {e}")
