import discord
import requests
from discord.ext import commands
from datetime import datetime
import asyncio


async def career(ctx, arg):
    auth = [564466359107321856, 323269361232248832, 564562239739396098, 564584121582747659]
    if not ctx.author.id in auth:
        await ctx.send('You are not authorized to use this command. Contact ``Xurxx#7879`` to see how to become authorized.')
    else:
        await ctx.send('You are an authorized user. Results processing...')
        try:
            msg = await ctx.send(f'Your message has been registered and I\'m working hard to query, read, format, and send you the last match for ``{arg}``. Hang tight!')
           
            newArg = arg.split('#')
            name = newArg[0]
            tag = newArg[1]

            async with ctx.typing():
                response = requests.get(f'https://api.henrikdev.xyz/valorant/v3/matches/na/{name}/{tag}')
                jsonR = response.json()

                embedM = discord.Embed(title=f"{name}\'s Career:")

                for j in range(5):
                    players = jsonR['data']['matches'][j]['players']['all_players']
                    
                    def mode():
                        try:
                            if jsonR['data']['matches'][j]['metadata']['mode'] == 'Normal':
                                return 'Unrated'
                            else:
                                return jsonR['data']['matches'][j]['metadata']['mode']
                        except:
                            if KeyError:
                                return 'Unknown'
                        
                    def map():
                        try:
                            return str(jsonR['data']['matches'][j]['metadata']['map'])
                        except KeyError:
                            return 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/200px-Question_mark_%28black%29.svg.png'

                    for i in players:
                        if i['name'] == name or i['name'] == name.title():
                            team = str(i['team']).lower()
                            if str(mode()) == 'Deathmatch':
                                won = i['stats']['kills']
                                lost = i['stats']['deaths']
                                
                            else:    
                                won = jsonR['data']['matches'][j]['teams'][team]['rounds_won']
                                lost = jsonR['data']['matches'][j]['teams'][team]['rounds_lost']
                    
                            embedM.add_field(name='--------------------------', value=f"**{mode()} | {map()}** | ***{won}-{lost}***", inline=False)
                            embedM.add_field(name='Character: ', value=i['character'])
                            embedM.add_field(name='KDA: ', value=str(i['stats']['kills']) + '/' + str(i['stats']['deaths'])+ '/' +str(i['stats']['assists']), inline=True)
                            embedM.add_field(name='Combat Score: ', value=int(i['stats']['score'])//int(jsonR['data']['matches'][0]['metadata']['rounds_played']), inline=True)
                embedM.description = f'Map/Mode/Score'
                embedM.color = 0xd9d9d9       
                if mode() == 'Unknown':
                    embedM.set_footer(text='Wondering what happened to mode/map? Run command ``=error 1``.')
                else:
                    embedM.set_footer(text='https://github.com/5late/Pepe-Bot')
                await asyncio.sleep(1)
                await ctx.send(embed=embedM)
                await msg.edit(content=f':smile: I successfully got the last 5 matches for {name}#{tag}! Congrats on being an authorized user.')
        except:
            await msg.edit(content='Error 2||Error 404 :(')
            await ctx.send('Use command ``=error 2`` to see more information.')