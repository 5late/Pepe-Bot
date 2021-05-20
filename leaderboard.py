from PIL.Image import new
import discord
from PIL import Image, ImageFont, ImageDraw
import requests
from discord.ext import commands
import asyncio


async def leaderBoard(ctx, arg):
        msg = await ctx.send(f'The command hand-off was successful, I am working hard to sort last game leaderboard information for {arg}.\nPlease allow up to 15 seconds.')
        def lastLetter(word):
                return word[::-1]


        newArg = arg.split('#')
        name = newArg[0]
        tag = newArg[1]

        if len(newArg) == 3:
                lbnum = int(newArg[2]) - 1
        else:
                lbnum = 0
        
        response = requests.get(f'https://api.henrikdev.xyz/valorant/v3/matches/na/{name}/{tag}')
        jsonR = response.json()

        Match = jsonR['data']['matches'][lbnum]
        metadata = Match['metadata']
        players = Match['players']['all_players']
        if metadata['mode'] == 'Deathmatch':
                await msg.edit(content='Error 5 || Error 400')
                await ctx.send('Deathmatch games are not supported.')
        for j in players:
                if j['name'] == name or j['name'] == name.title():
                        global team
                        team = j['team']
        teamScore = []
        teamSort = []
        enemyScore = []
        enemySort = []

        if team.lower() == 'blue':
                enemyTeam = 'red'
        else:
                enemyTeam = 'blue'

        if Match['teams'][team.lower()]['has_won'] and not Match['teams'][enemyTeam]['has_won']:
                friendlyColor = 0x34ebb4
        elif not Match['teams'][team.lower()]['has_won'] and not Match['teams'][enemyTeam]['has_won']:
                friendlyColor = 0xd7d9db
        else:
                friendlyColor = 0xce0e0e
        
        if not Match['teams'][team.lower()]['has_won'] and Match['teams'][enemyTeam]['has_won']:
                enemyColor = 0x34ebb4
        elif not Match['teams'][team.lower()]['has_won'] and not Match['teams'][enemyTeam]['has_won']:
                enemyColor = 0xd7d9db
        else:
                enemyColor = 0xce0e0e
        

        for i in players:
                if i['team'] == team:
                        teamScore.append(i['stats']['score'])
        
        newScore = sorted(teamScore)
        print(newScore)
        await msg.edit(content = 'I have collected information for the ``friendly`` team. Now I\'m working on collecting information for the ``enemy`` team. Hang tight.')
        await asyncio.sleep(1)

        for ii in players:
                for num in range(5):
                        if ii['stats']['score'] == newScore[num]:
                                nameNum = f"{ii['name']}     {ii['stats']['kills']}/{ii['stats']['deaths']}/{ii['stats']['assists']}   {num}"
                                teamSort.append(nameNum)
        print(teamSort)

        sortedTeam = sorted(teamSort, key=lastLetter)
        print(sortedTeam)
        
        finalMessage = ""

        for teamNum in range(4, -1, -1):
                finalMessage += f"\n{str(sortedTeam[teamNum])[:-1]} {newScore[teamNum]//metadata['rounds_played']}"
        
        Fembed = discord.Embed(title='Friendly Team', description=f'```{finalMessage}```', color = friendlyColor)
        await ctx.send(embed = Fembed)

        
        for i in players:
                if not i['team'] == team:
                        enemyScore.append(i['stats']['score'])
        
        newEScore = sorted(enemyScore)
        print(newEScore)
        await msg.edit(content='I have collected information for the ``enemy`` team.')
        await asyncio.sleep(1)

        for ii in players:
                for num in range(5):
                        if ii['stats']['score'] == newEScore[num]:
                                nameNumE = f"{ii['name']}     {ii['stats']['kills']}/{ii['stats']['deaths']}/{ii['stats']['assists']}   {num}"
                                enemySort.append(nameNumE)
        print(enemySort)

        sortedETeam = sorted(enemySort, key=lastLetter)

        finalEMessage = ""
        
        for teamNum in range(4, -1, -1):
                finalEMessage += f"\n{str(sortedETeam[teamNum])[:-1]} {round(newEScore[teamNum]/metadata['rounds_played'])}"

        Eembed = discord.Embed(title='Enemy Team', description=f'```{finalEMessage}```', color=enemyColor)
        await ctx.send(embed = Eembed)

if __name__ == '__main__':
    leaderBoard(ctx, arg)