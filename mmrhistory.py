import discord
import requests
from discord.ext import commands
import asyncio
from datetime import datetime


def checkStatusCode(status: str, task: str):
    f = open('./logs/API.txt', 'a')
    now = datetime.now()
    formatTime = now.strftime("%a, %B %d, %Y | %H:%M")
    if status == "200":
        f.write(f'\nSuccesful query on task {task} at {formatTime}.')
    else:
        f.write(f'\nTask {task} returned error code {status} at {formatTime}.')
    f.close()


async def mmrhistory(ctx, arg):
    newArg = arg.split('#')
    name = newArg[0]
    tag = newArg[1]

    response = requests.get(
        f'https://api.henrikdev.xyz/valorant/v1/mmr-history/na/{name}/{tag}')
    jsonR = response.json()

    status = jsonR['status']
    checkStatusCode(status, 'GET-ACCOUNT-MMR-HISTORY')
    if not status == "200":
        return await ctx.send(f'Error occured - status code {status}. Case recorded.')

    games = jsonR['data']
    number_of_games = len(games)

    wins = 0
    losses = 0
    elo = 0
    for game in games:
        if game['mmr_change_to_last_game'] < 0:
            losses += 1
        else:
            wins += 1
        elo += game['mmr_change_to_last_game']

    if wins > losses:
        color = 0x1bfa5e
    elif wins < losses:
        color = 0xff2626
    else:
        color = 0x424744

    if elo > 0:
        elo = f'+{elo}'
    else:
        elo = elo

    latest_game = games[0]['date']

    current_rank = games[0]['currenttier']
    icon_file = discord.File(
        f'./imgs/icons/TX_CompetitiveTier_Large_{current_rank}.png',
        filename='icon.png')

    embed = discord.Embed(
        title=f'MMR History for {name}#{tag}',
        description=f'**{name}** has {number_of_games} competitive games in their career.',
        color=color)
    embed.add_field(name='Wins', value=f'``{wins}``')
    embed.add_field(name='Losses', value=f'``{losses}``')
    embed.add_field(name='Net RR Gained/Lost', value=f'``{elo}``')
    embed.add_field(name='Latest Competitive Game', value=latest_game)
    embed.set_thumbnail(url='attachment://icon.png')

    await ctx.send(file=icon_file, embed=embed)
