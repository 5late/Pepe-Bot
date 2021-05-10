import discord
from discord.utils import get
from discord.ext import commands
import logging 
import numbers
from datetime import datetime, time, timedelta
import json
import requests
import random
import asyncio
from dotenv import load_dotenv
import youtube_dl
import os
from prsaw import RandomStuff
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

load_dotenv()

intents = discord.Intents().all()

DISCORD_TOKEN = os.getenv("discord_token")
AI_API_KEY = os.getenv('ai_api_key')
TRN_API_KEY = os.getenv('trn_api_key')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='=', description='A simple bot to learn python.', intents = intents)

deletedMsgs = []
deletedChnl = []
deletedAthr = []
editedMsgB = []
editedMsgA = []
editedAthr = []

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.1):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
        self.volume = volume

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

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

@bot.event
async def on_message_edit(message_before, message_after):
    editedMsgA.clear()
    editedMsgB.clear()
    editedAthr.clear()

    author = message_before.author
    editedAthr.append(author)

    msgb4 = message_before.content
    editedMsgB.append(msgb4)

    msga = message_after.content
    editedMsgA.append(msga)

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
async def lem(ctx):
    try:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        embedVar = discord.Embed(title="👁️Message Edit Watcher👁️", description = current_time)
        embedVar.add_field(name="Message Before: ", value=editedMsgB[0])
        embedVar.add_field(name="Message After: ", value=editedMsgA[0])
        embedVar.set_author(name=editedAthr[0],icon_url=editedAthr[0].avatar_url)

        await ctx.send(embed = embedVar)
    except:
        await ctx.send('I couldnt find any edited messages. :(')

sudoPriv = None
sudoers = open('sudoers.txt', 'r').read()
sudos = open('sudo.txt', 'r+')
sudosContent = sudos.read()
sudos.seek(0)
sudos.truncate()
sudos.write('False')

@bot.command()
async def sudo(message):
    print(sudoers)
    if str(message.author.id) in sudoers:
        sudos = open('sudo.txt', 'r+')
        sudos.seek(0)
        sudos.truncate()
        sudos.write('True')
        sudos.close()
        print(sudosContent)
        await message.channel.send('200')
    if not str(message.author.id) in sudoers:
        await message.channel.send(f'<@{message.author.id}> is not in the sudoers file. This incident will be reported.')
        sudos.seek(0)
        sudos.truncate()
        sudos.write('False')
        sudos.close()
        print(sudosContent)

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
async def dv(ctx, num1, num2):
    try:
        await ctx.send(f'{int(num1)/int(num2)}')
        
    except:
        await ctx.send('Numbers, please!')    

@bot.command()
async def mul(ctx, *nums):
    result = 1
    for num in nums:
        try:
            result *= int(num)
        except:
            await ctx.send('Numbers, please!')    
            break
    await ctx.send(f'{result}')


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
    await ctx.message.delete()
    await ctx.send("<:chriscry:758862800637657118>")
    await ctx.send(f'~~Called by {ctx.author.nick}~~')

@bot.command()
async def pog(ctx):
    await ctx.message.delete()
    await ctx.send("<:pog:766067548520448001>")
    await ctx.send(f'~~Called by {ctx.author.nick}~~')


@bot.command()
async def val(ctx, *, arg:str):
    try:
        newArg = arg.split('#')

        name = newArg[0]
        tag = newArg[1]

        msg = await ctx.send('Due to ratelimits and RIOT guidelines, this query could take between 4-8 seconds... Hang tight.')
        firstResponse = requests.get(f'https://api.henrikdev.xyz/valorant/v1/puuid/{name}/{tag}')
        jsonFR = firstResponse.json()
        puuid = jsonFR['data']['puuid']

        response = requests.get(f'https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/na/{puuid}')
        jsonR = response.json()

        ctp = int(jsonR['data']['elo'])
        if ctp <=100:
            image = 'https://static.wikia.nocookie.net/valorant/images/7/7f/TX_CompetitiveTier_Large_3.png/revision/latest/scale-to-width-down/185?cb=20200623203005'
        elif ctp >= 100 and ctp <200:
            image = 'https://static.wikia.nocookie.net/valorant/images/2/28/TX_CompetitiveTier_Large_4.png/revision/latest/scale-to-width-down/185?cb=20200623203053'
        elif ctp >= 200 and ctp <300:
            image = 'https://static.wikia.nocookie.net/valorant/images/b/b8/TX_CompetitiveTier_Large_5.png/revision/latest/scale-to-width-down/185?cb=20200623203101'
        elif ctp >= 300 and ctp < 400:
            image = 'https://static.wikia.nocookie.net/valorant/images/a/a2/TX_CompetitiveTier_Large_6.png/revision/latest/scale-to-width-down/185?cb=20200623203119'
        elif ctp >= 400 and ctp < 500:
            image = 'https://static.wikia.nocookie.net/valorant/images/e/e7/TX_CompetitiveTier_Large_7.png/revision/latest/scale-to-width-down/185?cb=20200623203140'
        elif ctp >= 500 and ctp < 600:
            image = 'https://static.wikia.nocookie.net/valorant/images/a/a8/TX_CompetitiveTier_Large_8.png/revision/latest/scale-to-width-down/185?cb=20200623203313'    
        elif ctp >= 600 and ctp < 700:
            image = 'https://static.wikia.nocookie.net/valorant/images/0/09/TX_CompetitiveTier_Large_9.png/revision/latest/scale-to-width-down/185?cb=20200623203408'
        elif ctp >= 700 and ctp < 800:
            image = 'https://static.wikia.nocookie.net/valorant/images/c/ca/TX_CompetitiveTier_Large_10.png/revision/latest/scale-to-width-down/185?cb=20200623203410'
        elif ctp >= 800 and ctp < 900:
            image = 'https://static.wikia.nocookie.net/valorant/images/1/1e/TX_CompetitiveTier_Large_11.png/revision/latest/scale-to-width-down/185?cb=20200623203413'
        elif ctp >= 900 and ctp < 1000:
            image = 'https://static.wikia.nocookie.net/valorant/images/9/91/TX_CompetitiveTier_Large_12.png/revision/latest/scale-to-width-down/185?cb=20200623203413'
        elif ctp >= 1000 and ctp < 1100:
            image = 'https://static.wikia.nocookie.net/valorant/images/4/45/TX_CompetitiveTier_Large_13.png/revision/latest/scale-to-width-down/185?cb=20200623203415'
        elif ctp >= 1100 and ctp < 1200:
            image = 'https://static.wikia.nocookie.net/valorant/images/c/c0/TX_CompetitiveTier_Large_14.png/revision/latest/scale-to-width-down/185?cb=20200623203417'
        elif ctp >= 1200 and ctp < 1300:
            image = 'https://static.wikia.nocookie.net/valorant/images/d/d3/TX_CompetitiveTier_Large_15.png/revision/latest/scale-to-width-down/185?cb=20200623203419'
        elif ctp >= 1300 and ctp < 1400:
            image = 'https://static.wikia.nocookie.net/valorant/images/a/a5/TX_CompetitiveTier_Large_16.png/revision/latest/scale-to-width-down/185?cb=20200623203606'
        elif ctp >= 1400 and ctp < 1500:
            image = 'https://static.wikia.nocookie.net/valorant/images/f/f2/TX_CompetitiveTier_Large_17.png/revision/latest/scale-to-width-down/185?cb=20200623203607'
        elif ctp >= 1500 and ctp < 1600:
            image = 'https://static.wikia.nocookie.net/valorant/images/b/b7/TX_CompetitiveTier_Large_18.png/revision/latest/scale-to-width-down/185?cb=20200623203609'
        elif ctp >= 1600 and ctp < 1700:
            image = 'https://static.wikia.nocookie.net/valorant/images/3/32/TX_CompetitiveTier_Large_19.png/revision/latest/scale-to-width-down/185?cb=20200623203610'
        elif ctp >= 1700 and ctp < 1800:
            image = 'https://static.wikia.nocookie.net/valorant/images/1/11/TX_CompetitiveTier_Large_20.png/revision/latest/scale-to-width-down/185?cb=20200623203611'
        elif ctp >= 1800 and ctp < 1900:
            image = 'https://static.wikia.nocookie.net/valorant/images/f/f9/TX_CompetitiveTier_Large_23.png/revision/latest/scale-to-width-down/185?cb=20200623203617'
        elif ctp >= 1900 and ctp < 2000:
            image = 'https://static.wikia.nocookie.net/valorant/images/f/f9/TX_CompetitiveTier_Large_23.png/revision/latest/scale-to-width-down/185?cb=20200623203617'
        elif ctp >= 2000:
            image = 'https://static.wikia.nocookie.net/valorant/images/2/24/TX_CompetitiveTier_Large_24.png/revision/latest/scale-to-width-down/185?cb=20200623203621'
        

        def last_2_digits_at_best(n):
            return float(str(n)[-3:]) if '.' in str(n)[-2:] else int(str(n)[-2:])
        fElo = last_2_digits_at_best(jsonR["data"]["elo"])
        rank = jsonR['data']['currenttierpatched']

        if ctp > 1800:
            eloEnd = f'{rank} ({ctp})'
        else:
            eloEnd = f'{fElo}/100'

        embedR = discord.Embed(title=name+"#"+tag, description=jsonR["data"]["currenttierpatched"], color=0x0000ff)
        embedR.add_field(name="Elo: ", value= eloEnd)
        embedR.add_field(name="Last Game Change: ", value=jsonR["data"]["mmr_change_to_last_game"])
        embedR.set_thumbnail(url=image)
        await ctx.send(embed = embedR)
        await msg.edit(content='Stats queryied.')
    except:
        await msg.edit(content='Error 404 :(')
        await ctx.send("I couldn't find a VALORANT profile with that name and/or tag. Try again. :( \nSome possible causes for this: \n1. The account does not exist. \n2. The account has not played competitive as yet. \n3. The accound has not played competitive in the past 20 games. (RIOT doesnt let me fetch that far :( - as yet.)")


@bot.command()
async def valm(ctx, *, arg:str):
    msg = await ctx.send(f'Your message has been registered and I\'m working hard to query, read, format, and send you the last match for ``{arg}``. Hang tight!')
    def agentImg(agent):
        Astra = 'https://img.redbull.com/images/c_crop,w_1620,h_1080,x_0,y_0,f_auto,q_auto/c_scale,w_1500/redbullcom/2021/3/25/wk6ik95vzmxyagx9md8e/valorant-agent-astra'
        Brimstone = 'https://res.allmacwallpaper.com/get/iMac-21-inch-5K-Retina-wallpapers/brimstone-valorant-4k-4096x2304/22319-13.jpg'
        Breach = 'https://i.ytimg.com/vi/qNviatS6riI/maxresdefault.jpg'
        Cypher = 'https://pbs.twimg.com/media/EVcDOuMXsAI2Y_z.jpg'
        Jett = 'https://static.wikia.nocookie.net/valorant/images/3/35/Jett_icon.png/revision/latest/scale-to-width-down/250?cb=20201128234156'
        Killjoy = 'https://img.redbull.com/images/c_crop,w_1080,h_720,x_0,y_0,f_auto,q_auto/c_scale,w_1500/redbullcom/2020/10/30/yrn6erzpnmlqnosjeaws/valorant-operator-killjoy'
        Omen = 'https://gamezo.co.uk/wp-content/uploads/2021/01/valorant-omen-uhdpaper.com-4K-5.2356-wp.thumbnail.jpg'
        Pheonix = 'https://boosting-ground.com/upload/206ceecc064d01d74e708bae5a67e7568914f5c2.jpeg'
        Raze = 'https://static.wikia.nocookie.net/valorant/images/b/b1/Suke-raze-keyart-final.jpg/revision/latest/scale-to-width-down/250?cb=20200508170424'
        Reyna = 'https://img.redbull.com/images/c_crop,x_611,y_0,h_2160,w_2520/c_fill,w_650,h_540/q_auto,f_auto/redbullcom/2020/6/3/ypiocflf3wcbeeyjyi5x/valorant'
        Sage = 'https://www.nme.com/wp-content/uploads/2020/06/061020-Valorant-Sage.jpeg'
        Skye = 'https://www.nme.com/wp-content/uploads/2020/10/100920-Valorant-Skye.jpg'
        Sova = 'https://gamezo.co.uk/wp-content/uploads/2020/11/Sova-Guide.png'
        Viper = 'https://www.nme.com/wp-content/uploads/2020/06/062320-Valorant-Viper-Riot-Games.jpg'
        Yoru = 'https://staticg.sportskeeda.com/editor/2021/01/f892e-16103844629156-800.jpg'

        if agent == 'Astra':
            return Astra
        elif agent == 'Brimstone':
            return Brimstone
        elif agent == 'Breach':
            return Breach
        elif agent == 'Cypher':
            return Cypher
        elif agent == 'Jett':
            return Jett
        elif agent == 'Killjoy':
            return Killjoy
        elif agent == 'Omen':
            return Omen
        elif agent == 'Pheonix':
            return Pheonix
        elif agent == 'Raze':
            return Raze
        elif agent == 'Reyna':
            return Reyna
        elif agent == 'Sage':
            return Sage
        elif agent == 'Skye':
            return Skye
        elif agent == 'Sova':
            return Sova
        elif agent == 'Viper':
            return Viper
        elif agent == 'Yoru':
            return Yoru
        
    newArg = arg.split('#')
    name = newArg[0]
    tag = newArg[1]
    async with ctx.typing():
        response = requests.get(f'https://api.henrikdev.xyz/valorant/v3/matches/na/{name}/{tag}')
        jsonR = response.json()

        players = jsonR['data']['matches'][0]['players']['all_players']
        for i in players:
            if i['name'] == name:
                embedM = discord.Embed(title=f'{arg}\'s last match:', description = i['currenttier_patched'])
                embedM.add_field(name='Character: ', value=i['character'])
                embedM.add_field(name='KDA: ', value=str(i['stats']['kills']) + '/' + str(i['stats']['deaths'])+ '/' +str(i['stats']['assists']))
                embedM.add_field(name='Score: ', value=i['stats']['score'], inline=True)
                embedM.set_thumbnail(url=str(agentImg(str(i['character']))))
    await ctx.send(embed=embedM)
    await msg.edit(content=f':smile: I successfully got last game stats for {arg}!')
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
    if ctx.message.author.id == 564466359107321856 and sudoPriv:
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
        if randomC == '✅' and positive > 0:
            await ctx.send('You guessed correctly!')
        elif randomC == '❎' and negative > 0:
            await ctx.send('You guessed correctly!')
        else:
            await ctx.send('You did not guess correctly.')
        
        for reaction in voteMsg.reactions:
            if reaction.emoji == '✅':
                positive = reaction.count - 1
            if reaction.emoji == '❎':
                negative = reaction.count - 1
    
            
    except:
        await ctx.send('An error occured.')


WHEN = time(13, 29, 0)  # 6:00 PM
channel_id = 801520877753597974 # Put your channel id here

async def called_once_a_day():
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id) 
    await channel.send(f"<@564466359107321856>, <@564562239739396098>, <@543866993602723843>, <@380761443479322624> This is an automated message to remind you all to take attendance at {WHEN} EDT. This message was set to send to <#{channel_id}> by <@564466359107321856>.")

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

@bot.command(name='join', help='Joins the voice channel.')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send('{} is not connected to a voice channel'.format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='leave', help='Leaves voice channel.')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play', help='play a youtube URL.')
async def play(ctx, url):
    if str(ctx.message.author.id) in sudoers and sudosContent == 'True':
        voice = get(bot.voice_clients, guild=ctx.guild)

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source=filename))
        await ctx.send('**Now playing** {}'.format(filename))
    else:
        await ctx.send(f'{ctx.message.author} is not in the sudoers file. This instance will be reported.')

@bot.command()
async def rmd(ctx, time, *, reason:str = ''):
    try:
        timeLen = len(time)
        if not len(reason):
            newReason = f'<@{ctx.message.author.id}>, you set a reminder ``{time}`` ago without a reason.'
        else: 
            newReason = f'<@{ctx.message.author.id}>, you set a reminder ``{time}`` ago with reason ``{reason}``'
        if timeLen == 3:
            await ctx.send(f'I\'m setting a reminder for ``{time}`` with reason ``{reason}``! :smile:')
            lastChar = time[-1]
            if lastChar == 'm':
                newTime = int(60*int(time[:2]))
                await asyncio.sleep(newTime)
                await ctx.send(newReason)
            elif lastChar == 's':
                newTime = int(time[:2])
                await asyncio.sleep(newTime)
                await ctx.send(newReason)
            elif lastChar == 'h':
                newTime = int(60*60*int(time[:1]))
                await asyncio.sleep(newTime)
                await ctx.send(newReason)
            else:
                await ctx.send('That amount of time is not supported!')
        elif timeLen == 2:
            await ctx.send(f'I\'m setting a reminder for ``{time}`` with reason ``{reason}``! :smile:')
            lastChar = time[-1]
            if lastChar == 'm':
                newTime = int(60*int(time[:1]))
                print(f'sleeping for {newTime} seconds.')
                await asyncio.sleep(newTime)
                await ctx.send(newReason)
            elif lastChar == 's':
                newTime = int(time[:1])
                await asyncio.sleep(newTime)
                await ctx.send(newReason)
            elif lastChar == 'h':
                newTime = int(60*60*int(time[:1]))
                await asyncio.sleep(newTime)
                await ctx.send(newReason)
            else:
                await ctx.send('That amount of time is not supported!')
        else:
            await ctx.send('Value ``time`` must be of length ``2``.')
    except:
        await ctx.send('An error occured in the command. Check usage, then try again.')


@bot.command()
async def whoami(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    
    secondFont = ImageFont.truetype("./fonts/Hind-Regular.ttf", 110)
    wanted = Image.open("./imgs/background.jpg")

    draw = ImageDraw.Draw(wanted)

    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((450, 450))
    secondText = f'{user.name}#{user.discriminator}'

    draw.text((150, 1075), secondText, (255, 255, 255), font=secondFont)

    wanted.paste(pfp, (250, 500))

    wanted.save("profile.jpg")
    
    await ctx.send(file = discord.File("profile.jpg"))

@bot.command()
async def braindead(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    braindead = Image.open("./imgs/braindead.jpg")
    
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((750, 750))

    braindead.paste(pfp, (850, 650))

    braindead.save("stupid.jpg")

    await ctx.send(file = discord.File("stupid.jpg"))


@bot.command()
async def gigachad(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    gigachad = Image.open("./imgs/gigachad.jpg")
    
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((250, 250))

    gigachad.paste(pfp, (250, 35))

    gigachad.save("chad.jpg")

    await ctx.send(file = discord.File("chad.jpg"))

@bot.command()
async def soyjak(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    soyjak = Image.open("./imgs/soyjak.jpg")
    
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((300, 300))

    soyjak.paste(pfp, (160, 190))

    soyjak.save("soy.jpg")

    await ctx.send(file = discord.File("soy.jpg"))


@bot.command()
async def talk(ctx, *, args):
    rs = RandomStuff(api_key= AI_API_KEY)
    response = rs.get_ai_response(args)
    await ctx.send(response)
    rs.close()

@bot.command()
async def test(ctx):
    print(sudosContent)
    if sudosContent == 'True' and str(ctx.author.id) in sudoers:
        await ctx.send('sudo works')
    
@bot.command()
async def gh(ctx):
    await ctx.send('https://github.com/5late/Pepe-Bot')

@bot.command()
async def bj(ctx):
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    faceCards = ['J','Q','K']
    playerCard = []
    dealerCard = []
    randomCard = random.choice(cards)
    shownCard = random.choice(cards)
    cdc1 = []
    cpc1 = []

    def calcCard(card, cpc):
        if card in faceCards:
            cpc += 10
        elif int(cpc) <= 10 and card == 'A':
            cpc += 11
        elif int(cpc) > 10 and card == 'A':
            cpc+= 1
        else:
            cpc+=int(card)
        print(cpc)
        cpc1.clear()
        cpc1.append(cpc)
        return cpc

    def intize(cpc, cdc):
        dealerCard.append(shownCard)
        dealerCard.append(randomCard)
        playerCard.append(randomCard)
        playerCard.append(randomCard)
        print(playerCard)
        print(shownCard)
        print(dealerCard)
        playerCount = int(cpc)
        dealerCount = int(cdc)
        for playerCardnow in playerCard:
            if playerCardnow in faceCards:
                playerCount += 10
            elif int(playerCount) <= 10 and playerCardnow == 'A':
                playerCount += 11
            elif int(playerCount) > 10 and playerCardnow == 'A':
                playerCount+= 1
            else:
                playerCount+=int(playerCardnow)
        print(playerCount)
        for dealerCardnow in dealerCard:
            if dealerCardnow in faceCards:
                dealerCount += 10
            elif int(dealerCount) <= 10 and dealerCardnow == 'A':
                dealerCount += 11
            elif int(dealerCount) > 10 and dealerCardnow == 'A':
                dealerCount+= 1
            else:
                dealerCount+=int(dealerCardnow)
        print(dealerCount)
        cpc1.clear()
        cdc1.clear()
        cdc1.append(dealerCount)
        cpc1.append(playerCount)

    intize(0,0)

    def checkGame():
        if cpc1[0] > 21:
            return True
        else:
            return False

    def check(author):
        def inner_check(ctx):
            return ctx.author == author and ctx.content == 'h' or 's'
        return inner_check
    await ctx.send(f'Your cards are {playerCard}. Do you want to hit or stand?')
    
    msg = await bot.wait_for('message', check=check(ctx.author), timeout=30)
    if msg.content == 'h':
        playerCard.append(randomCard)
        currentC = calcCard(playerCard[2],cpc1[0])
        ckGame = checkGame()
        if ckGame:
            await ctx.send(f'You busted! You pulled a {playerCard[2]}, bringing your total to {currentC}')
        else:
            await ctx.send(f'You took a {playerCard[2]} from the deck. Your new cards are: {playerCard}. Your total is {currentC}')
        
            msg2 = await bot.wait_for('message', check=check(ctx.author), timeout=30)
        
            if msg2.content == 'h':
                playerCard.append(randomCard)
                currentC = calcCard(playerCard[2],cpc1[0])
                ckGame = checkGame()
                if ckGame:
                    await ctx.send(f'You busted! You pulled a {playerCard[2]}, bringing your total to {currentC}')
                else:
                    await ctx.send(f'You took a {playerCard[2]} from the deck. Your new cards are: {playerCard}. Your total is {currentC}')
                    msg3 = await bot.wait_for('message', check=check(ctx.author), timeout=30)
                    
                    if msg3.content == 'h':
                        playerCard.append(randomCard)
                        currentC = calcCard(playerCard[2],cpc1[0])
                        ckGame = checkGame()
                        if ckGame:
                            await ctx.send(f'You busted! You pulled a {playerCard[2]}, bringing your total to {currentC}')
                        else:        
                            finalEmbed = discord.Embed(title='Black Jack', description=f'You win! You drew 5 cards without going over 21!')
                            finalEmbed.add_field(name='Your cards', value=playerCard)

                            await ctx.send(f'You took a {playerCard[2]} from the deck. Your new cards are: {playerCard}. Your total is {currentC}')
                        
                    elif msg3.content == 's':
                        await ctx.send(f'You stood. The dealers cards were: {dealerCard}.')
                
            elif msg2.content == 's':
                await ctx.send(f'You stood. The dealers cards were: {dealerCard}.')
            
    elif msg.content == 's':
        await ctx.send(f'You stood. The dealers cards were: {dealerCard}.')
                


if __name__ == "__main__":
    bot.loop.create_task(background_task())
    bot.run(DISCORD_TOKEN)