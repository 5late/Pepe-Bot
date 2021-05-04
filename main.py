import discord
from discord.ext import commands
import logging 
import numbers
from datetime import datetime, time, timedelta
import json
import requests
import random
import asyncio

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='=', description='A simple bot to learn python.')

deletedMsgs = []
deletedChnl = []
deletedAthr = []

@bot.event
async def on_ready():
    print('Logged on as ')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')

@bot.event
async def on_message_delete(message):
    deletedAthr.clear()
    deletedChnl.clear()
    deletedMsgs.clear()

    author = str(message.author) 
    deletedAthr.append(author)

    channel= '<#'+str(message.channel.id)+'>: '
    deletedChnl.append(channel)

    content= str(message.content)
    deletedMsgs.append(content)

@bot.command()
async def ldm(ctx):
    try:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        embedVar = discord.Embed(title=deletedAthr[0], description=deletedMsgs[0], color=0xff0000)
        embedVar.add_field(name="Time: ", value=current_time)
        embedVar.add_field(name="Channel: ", value=deletedChnl[0])

        await ctx.send(embed = embedVar)
    except:
        await ctx.send('I couldnt find any deleted messages. :(')

@bot.command()
async def hello(message):
    await message.channel.send('Hello!')

@bot.command()
async def dt (ctx):
    now = datetime.now()
    formatTime = now.strftime("%a, %B %d, %Y | %H:%M")
    await ctx.reply('It is: ' + formatTime)

@bot.command()
async def delete(ctx, amount):
    try:
        amount = int(amount)
        if ctx.author.id == 342874810868826112:
            return
        else:
            if amount > 100:
                ctx.send('Thats too many messages for me!')
            else:
                await ctx.channel.purge(limit=amount)

    except:
        ctx.send('An error occured.')

@bot.command()
async def add(ctx, *nums):
    result = 0
    for num in nums:
        try:
            result += int(num)
        
        except:
            await ctx.send('Numbers, please!')
            break
    await ctx.send("{} = {}".format((' + '.join(map(str, list(nums)))), result))

@bot.command()
async def keyword(ctx, *, word:str):
    # channel = bot.get_channel(ctx.channel.id)
    messages = await ctx.channel.history(limit=200).flatten()

    for msg in messages:
        if word in msg.content:
            await ctx.send(msg.jump_url)
            time.sleep(1.2)

@bot.command()
async def cry(ctx):
    await ctx.send("<:chriscry:758862800637657118>")

@bot.command()
async def pog(ctx):
    await ctx.send("<:pog:766067548520448001>")


@bot.command()
async def val(ctx, name, tag):
    try:
        response = requests.get(f'https://api.henrikdev.xyz/valorant/v1/mmr/na/{name}/{tag}')
        jsonR = response.json()

        def last_2_digits_at_best(n):
            return float(str(n)[-3:]) if '.' in str(n)[-2:] else int(str(n)[-2:])
        fElo = last_2_digits_at_best(jsonR["data"]["elo"])

        embedR = discord.Embed(title=name+"#"+tag, description=jsonR["data"]["currenttierpatched"], color=0x0000ff)
        embedR.add_field(name="Elo: ", value= str(fElo) + "/100")
        embedR.add_field(name="Last Game Change: ", value=jsonR["data"]["mmr_change_to_last_game"])
        await ctx.send(embed = embedR)
    except:
        await ctx.send("I couldn't find a VALORANT profile with that name and/or tag. Try again. :(")

@bot.command()
async def ras(ctx, option=''):
    agentList = ["Astra", "Breach", "Skye", "Yoru", "Phoenix", "Brimstone", "Sova", "Jett", "Reyna", "Omen", "Viper", "Cypher", "Killjoy", "Sage", "Raze"]
    agentListNF = ["Astra", "Brimstone", "Sova", "Jett", "Reyna", "Omen", "Viper", "Cypher", "Killjoy", "Sage", "Raze"]
    
    embedN = discord.Embed(title="Random Agent Selector", description=random.choice(agentList))
    embedNF = discord.Embed(title="Random Agent Selector", description=random.choice(agentListNF))

    if option == "nf":
        await ctx.send(embed = embedNF)
    if not option:
        await ctx.send(embed=embedN)

@bot.command(pass_context=True)
async def randomchoice(ctx, *, question):
    randomAnswers = ["Don't bother asking", "It will certainly happen", "Only to you.", "Maybe or maybe not"]

    embed8 = discord.Embed(title="The Magic 8ball", description=random.choice(randomAnswers))

    await ctx.send(embed = embed8)
bot.command(name="ball", pass_context=True,)(randomchoice.callback)

@bot.command()
async def write(ctx, title:str, url:str):
    if ctx.message.author.id == 564466359107321856:
        def write_json(data, filename='clips.json'):
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)

        with open('clips.json') as json_file:
            data = json.load(json_file)
            
            temp = data['clips']
            clips = {
                'title': title,
                'url': url
            }
            temp.append(clips)
            
        write_json(data)
    else:
        await ctx.send('You are not authorized to use this command.')

@bot.command()
async def read(ctx, title=''):
    if not title:
        titles = []
        with open('clips.json') as f:
            data = json.load(f)
            dataClips = data['clips']
        for i in dataClips:
            titles.append(i['title'])
        await ctx.send(f'These are the clip titles I\'ve got: ```{str(titles)}```. Run command ``=read [title]`` to watch the clip.')
    else:        
        with open('clips.json') as f:
            data = json.load(f)
            dataClips = data['clips']
        
        for i in dataClips:
            if i['title'] == title:
                await ctx.send(i['url'])

@bot.command()
async def kissme(ctx):
    if ctx.message.author.id == 543866993602723843 or ctx.message.author.id == 564466359107321856 or ctx.message.author.id == 564562239739396098:
       await ctx.send('Ok <:happier:821406857678946394> , nht.')
    else:
       await ctx.send('Ew, no.') 

@bot.command()
async def vote(ctx):
    voteMsg = await ctx.channel.send('This is a test message for reactions.')
    await voteMsg.add_reaction('✅')
    await voteMsg.add_reaction('❎')
    await asyncio.sleep(30)
    voteMsg = await voteMsg.channel.fetch_message(voteMsg.id)
    positive = 0
    negative = 0

    for reaction in voteMsg.reactions:
        if reaction.emoji == '✅':
            positive = reaction.count - 1
        if reaction.emoji == '❎':
            negative = reaction.count - 1
    
    print(f'Vote Result: {positive} postiive and {negative} negative reactions.')

@bot.command()
async def quiz(ctx):
    voteMsg = await ctx.channel.send('Check mark or X mark?')
    await voteMsg.add_reaction('✅')
    await voteMsg.add_reaction('❎')
    await asyncio.sleep(10)
    voteMsg = await voteMsg.channel.fetch_message(voteMsg.id)
    positive = 0
    negative = 0
    randomC = random.choice(['✅', '❎'])

    try:
        for reaction in voteMsg.reactions:
            if reaction.emoji == '✅':
                positive = reaction.count - 1
            if reaction.emoji == '❎':
                negative = reaction.count - 1
    except:
        await ctx.send('An error occured.')


WHEN = time(9, 28, 0)  # 6:00 PM
channel_id = 801520877753597974 # Put your channel id here

async def called_once_a_day():
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id) 
    await channel.send(f"<@564466359107321856>, <@564562239739396098>, <@543866993602723843>, <@380761443479322624> This is an automated message to remind you all to take attendance at {WHEN}. This message was set to send to <#{channel_id}> by <@564466359107321856>.")

async def background_task():
    now = datetime.now()
    if now.time() > WHEN:  
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  
        await asyncio.sleep(seconds)   
    while True:
        now = datetime.now() 
        target_time = datetime.combine(now.date(), WHEN)  
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)  
        await called_once_a_day()  
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  
        await asyncio.sleep(seconds)   


if __name__ == "__main__":
    bot.loop.create_task(background_task())    
    token = open("token.txt", "r").read()
    bot.run(token)