import discord
from discord.embeds import EmptyEmbed
from discord.utils import get
from discord.ext import commands
from datetime import datetime, time, timedelta
import json
import requests
import random
import asyncio
from dotenv import load_dotenv
import youtube_dl
import os
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import platform
import leaderboard
import careerF
import re
import checkshop
import lm
import mmrhistory
import livematch
import peakrank

load_dotenv()

intents = discord.Intents().all()

DISCORD_TOKEN = os.getenv("discord_token")
AI_API_KEY = os.getenv("ai_api_key")
TRN_API_KEY = os.getenv("trn_api_key")
USERNAME = os.getenv("username")
PASSWORD = os.getenv("password")
IP = os.getenv('ip')

bot = commands.Bot(
    command_prefix="=",
    description="A simple bot to learn python.",
    intents=intents,
    help_command=None,
)

deletedMsgs = []
deletedChnl = []
deletedAthr = []
editedMsgB = []
editedMsgA = []
editedAthr = []

youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    "source_address": "0.0.0.0",
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.1):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = ""
        self.volume = volume

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )
        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]
        filename = data["title"] if stream else ytdl.prepare_filename(data)
        return filename


@bot.event
async def on_ready():
    global botUptime
    botUptime = datetime.utcnow()
    print("Logged on as ")
    print(bot.user.name)
    print(bot.user.id)
    print("-----")


@bot.event
async def on_message_delete(message):
    deletedAthr.clear()
    deletedChnl.clear()
    deletedMsgs.clear()

    author = str(message.author)
    deletedAthr.append(author)

    channel = "<#" + str(message.channel.id) + ">: "
    deletedChnl.append(channel)

    content = str(message.content)
    deletedMsgs.append(content)


@bot.event
async def on_message_edit(message_before, message_after):
    matches = ['<:', ':>', '<a:']
    if message_before.author.id == 564584121582747659 and any(
            x in message_after.content for x in matches):
        await message_after.delete()
    editedMsgA.clear()
    editedMsgB.clear()
    editedAthr.clear()

    author = message_before.author
    editedAthr.append(author)

    msgb4 = message_before.content
    editedMsgB.append(msgb4)

    msga = message_after.content
    editedMsgA.append(msga)


@bot.event
async def on_message(message):
    matches = ['<:', ':>', '<a:']
    if message.author.id == 564584121582747659 and any(
            x in message.content for x in matches):
        await message.delete()

    await bot.process_commands(message)


@bot.command()
async def help(ctx, *, group=""):
    categories = [
        "calculator",
        "image manipulation",
        "valorant",
        "music",
        "misc"]
    fGroup = group.replace(" ", "-")
    if not group:
        helpEmbed = discord.Embed(
            title="Help Command",
            description="Use command ``=help {category}``")
        helpEmbed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url)
        helpEmbed.add_field(
            name="See all my commands!",
            value="[Click Here](https://github.com/5late/Pepe-Bot/blob/master/docs/commands.md)",
        )
        helpEmbed.add_field(
            name="Categories",
            value="calculator, image manipulation, valorant, music, misc",
        )
        helpEmbed.set_footer(text="Thanks :)")

        await ctx.send(embed=helpEmbed)
    elif group.lower() in categories:
        helpEmbed = discord.Embed(title=f"Help Command - {group.title()}")
        helpEmbed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url)
        helpEmbed.add_field(
            name=f"{group.title()} commands!",
            value=f"[Click Here](https://github.com/5late/Pepe-Bot/blob/master/docs/commands.md/#{fGroup})",
        )
        helpEmbed.set_footer(text="Thanks :)")
        await ctx.send(embed=helpEmbed)
    else:
        await ctx.send(f"No command group with name ``{group}`` found.")


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! Bot latency is ``{round((bot.latency * 1000), 1)}`` ms.")
    print(os.name)


@bot.command()
async def pwd(ctx):
    def getBotUptime():
        now = datetime.utcnow()
        delta = now - botUptime

        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if days:
            fmt = "``{d}`` days, ``{h}`` hours, ``{m}`` minutes, and ``{s}`` seconds."
        elif hours:
            fmt = "``{h}`` hours, ``{m}`` minutes, and ``{s}`` seconds."
        else:
            fmt = "``{m}`` minutes and ``{s}`` seconds."

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    if now.hour < 12:
        wordTime = "Good Morning"
    elif now.hour >= 12 and now.hour < 17:
        wordTime = "It's Afternoon"
    elif now.hour >= 17 and now.hour < 21:
        wordTime = "Good Evening"
    else:
        wordTime = "Night"

    if ctx.author.nick is None:
        name = ctx.author.name
    else:
        name = ctx.author.nick

    embedI = discord.Embed(
        title=f"{wordTime}, {name}",
        description="Let's check out some stats.",
    )
    embedI.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embedI.add_field(
        name="Running on Operating System:", value=f"``{platform.system()}``"
    )
    embedI.add_field(
        name="Version:",
        value=f"``{platform.release()}``",
        inline=True)
    embedI.add_field(name="Time:", value=f'``{current_time}``', inline=False)
    embedI.add_field(
        name="Bot Latency/Ping",
        value=f"``{round((bot.latency * 1000), 1)}`` ms",
        inline=True)
    embedI.add_field(name="Bot Uptime", value=getBotUptime(), inline=True)

    await ctx.send(embed=embedI)


@bot.command()
async def uptime(ctx):
    def getBotUptime():
        now = datetime.utcnow()
        delta = now - botUptime

        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if days:
            fmt = "``{d}`` days, ``{h}`` hours, ``{m}`` minutes, and ``{s}`` seconds."
        elif hours:
            fmt = "``{h}`` hours, ``{m}`` minutes, and ``{s}`` seconds."
        else:
            fmt = "``{m}`` minutes and ``{s}`` seconds."

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    await ctx.send(f'Bot has been online for {getBotUptime()}')


@bot.command()
async def ldm(ctx):
    try:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        embedVar = discord.Embed(
            title=deletedAthr[0], description=deletedMsgs[0], color=0xFF0000
        )
        embedVar.add_field(name="Time: ", value=current_time)
        embedVar.add_field(name="Channel: ", value=deletedChnl[0])

        await ctx.send(embed=embedVar)
    except BaseException:
        await ctx.send("I couldnt find any deleted messages. :(")


@bot.command()
async def lem(ctx):
    try:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        embedVar = discord.Embed(
            title="👁️Message Edit Watcher👁️", description=current_time
        )
        embedVar.add_field(name="Message Before: ", value=editedMsgB[0])
        embedVar.add_field(name="Message After: ", value=editedMsgA[0])
        embedVar.set_author(
            name=editedAthr[0],
            icon_url=editedAthr[0].avatar_url)

        await ctx.send(embed=embedVar)
    except BaseException:
        await ctx.send("I couldnt find any edited messages. :(")


@bot.command()
async def hello(message):
    await message.channel.send(f"Hello {message.author.name}!")


@bot.command()
async def dt(ctx):
    now = datetime.now()
    formatTime = now.strftime("%a, %B %d, %Y | %H:%M")
    await ctx.reply("It is: " + formatTime)


@bot.command()
async def delete(ctx, amount):
    try:
        amount = int(amount)
        if ctx.author.id == 342874810868826112:
            return
        else:
            if amount > 100:
                await ctx.send("Thats too many messages for me!")
            else:
                await ctx.channel.purge(limit=amount)

    except BaseException:
        ctx.send("An error occured.")


@bot.command()
async def add(ctx, *nums):
    result = 0
    for num in nums:
        try:
            result += int(num)

        except BaseException:
            await ctx.send("Numbers, please!")
            break
    await ctx.send("{} = {}".format((" + ".join(map(str, list(nums)))), result))


@bot.command()
async def sub(ctx, *nums):
    result = int(nums[0])
    newNums = nums[1:]
    for num in newNums:
        try:
            result -= int(num)
        except BaseException:
            await ctx.send("Whole numbers, please!")
            break
    await ctx.send(f"{str(result)}")


@bot.command()
async def dv(ctx, num1, num2):
    try:
        await ctx.send(f"{int(num1)/int(num2)}")

    except BaseException:
        await ctx.send("Numbers, please!")


@bot.command()
async def mul(ctx, *nums):
    result = 1
    for num in nums:
        try:
            result *= int(num)
        except BaseException:
            await ctx.send("Numbers, please!")
            break
    await ctx.send(f"{result}")


@bot.command()
async def keyword(ctx, *, word: str):
    # channel = bot.get_channel(ctx.channel.id)
    messages = await ctx.channel.history(limit=200).flatten()

    for msg in messages:
        if word in msg.content:
            await ctx.send(msg.jump_url)
            time.sleep(1.2)


@bot.command()
async def cry(ctx):
    servers = [754084714545152101, 839633894403997726, 814335750077153320]
    if ctx.guild.id not in servers:
        return await ctx.send('Sorry, this command is server specific. It is not meant for use outside of bot development! ||Features like this might become public soon, let me know what you think.||')
    await ctx.message.delete()
    await ctx.send("<:chriscry:758862800637657118>")
    if ctx.author.nick is None:
        await ctx.send(f"~~Called by {ctx.author.name}~~")
    else:
        await ctx.send(f"~~Called by {ctx.author.nick}~~")


@bot.command()
async def pog(ctx):
    await ctx.message.delete()
    await ctx.send("<:pog:766067548520448001>")
    if ctx.author.nick is None:
        await ctx.send(f"~~Called by {ctx.author.name}~~")
    else:
        await ctx.send(f"~~Called by {ctx.author.nick}~~")


@bot.command()
async def auth(ctx):
    await ctx.send('This command is a work in progress. We hope to have a future where this command can begin to automatically authorize trusted users. Check back later. (Error 3 || Error 410)')


def checkStatusCode(status: str, task: str):
    f = open('./logs/API.txt', 'a')
    now = datetime.now()
    formatTime = now.strftime("%a, %B %d, %Y | %H:%M")
    if status == "200":
        f.write(f'\nSuccesful query on task {task} at {formatTime}.')
    else:
        f.write(f'\nTask {task} returned error code {status} at {formatTime}.')
    f.close()


@commands.cooldown(1, 16, commands.BucketType.user)
@bot.command()
async def val(ctx, *, arg: str):
    async def mainValFetch(arg):
        newArg = arg.split("#")

        name = newArg[0].replace('\\', '')
        tag = newArg[1]

        msg = await ctx.send(
            "This request is processing. Please allow up to 10 seconds. Thanks."
        )
        firstResponse = requests.get(
            f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}"
        )
        jsonFR = firstResponse.json()
        print(jsonFR['status'])
        status = str(jsonFR['status'])
        checkStatusCode(status, "GET-ACCOUNT-PUUID-AND-LEVEL")
        if not status == "200":
            await msg.delete()
            return await ctx.send(f'Error occured - status code {status}. Case recorded.')
        puuid = jsonFR["data"]["puuid"]
        level = jsonFR["data"]["account_level"]

        response = requests.get(
            f"https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/na/{puuid}"
        )
        jsonR = response.json()
        checkStatusCode(jsonR['status'], "GET-ACCOUNT-MMR")
        if not jsonR['status'] == '200':
            return await ctx.send(f"Error occured - status code {jsonR['status']}. Case recorded.")

        ctp = int(jsonR["data"]["elo"])
        lgc = str(jsonR['data']['mmr_change_to_last_game'])
        rank = int(jsonR["data"]["currenttier"])
        iconFile2 = discord.File(
            f"imgs/icons/TX_CompetitiveTier_Large_{rank}.png",
            filename="icon.png")

        def last_2_digits_at_best(n):
            return float(
                str(n)[-3:]) if "." in str(n)[-2:] else int(str(n)[-2:])

        fElo = last_2_digits_at_best(jsonR["data"]["elo"])
        rank = jsonR["data"]["currenttierpatched"]

        if ctp > 1800:
            eloEnd = f"{rank} ({ctp})"
        else:
            eloEnd = f"{fElo}/100"

        if not lgc.startswith('-'):
            lgc = f"+{lgc}"
        else:
            lgc = lgc

        embedR = discord.Embed(
            title=name + "#" + tag,
            color=0x32a852,
        )
        embedR.set_thumbnail(url=f"attachment://icon.png")
        embedR.add_field(
            name='Rank: ',
            value=jsonR['data']['currenttierpatched'])
        embedR.add_field(name="Elo: ", value=eloEnd)
        embedR.add_field(name='Account Level: ', value=level)
        embedR.add_field(name="Last Game Change: ", value=lgc)
        embedR.set_footer(
            text='Bot maintained by Xurxx#7879. Level innacurate? Play a game and re-try.')

        await ctx.send(file=iconFile2, embed=embedR)
        await msg.edit(content="Stats queryied.")

    if '\\' not in arg and '//' in arg:
        distinguish = arg.split('//')
        if len(distinguish) > 5:
            return await ctx.send('Max player request of 5 at a time.')
        for player in distinguish:
            player.lstrip()
            player.rstrip()
            await mainValFetch(player)
    else:
        await mainValFetch(arg)


@val.error
async def mine_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'You are on cooldown! Retry in ``{error.retry_after:.1f}s``, please.')


@bot.command()
async def apistats(ctx):
    await ctx.send('Calibrating....')
    f = open('./logs/API.txt', 'r')
    lines = f.readlines()

    error_count = 0
    success_count = 0
    errors = []
    non_api_error_count = 0
    for line in lines:
        if "error" in line.strip():
            get_error_code = line.split('error code ')[1]
            error_code = get_error_code[:3]
            errors.append(error_code)
            if error_code == '404' or error_code == '409':
                error_count += 1
            else:
                error_count += 1
                non_api_error_count += 1
        else:
            success_count += 1
    errors_sorted = list(dict.fromkeys(errors))
    success_rate = round(
        (success_count / (error_count + success_count)) * 100, 2)
    return_rate = round(
        (success_count / (non_api_error_count + success_count)) * 100, 2)
    last_line = lines[-1]

    APIEmbed = discord.Embed(title='API Statistics', color=0x808080)
    APIEmbed.add_field(
        name='Request Success Rate',
        value=f"{success_rate}%")
    APIEmbed.add_field(name='API Return Rate', value=f"{return_rate}%")
    APIEmbed.add_field(
        name='Total Responses',
        value=error_count +
        success_count,
        inline=False)
    for errors_found in errors_sorted:
        APIEmbed.add_field(
            name=f"{errors_found} Responses",
            value=f"[{errors.count(errors_found)}](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)")

    APIEmbed.add_field(
        name='200 Responses',
        value=f"[{success_count}](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200)")

    f.seek(0)
    first_line = f.readline().strip()
    start_date = first_line.split('at')
    APIEmbed.add_field(
        name="Start Date",
        value=f"{start_date[1]} EDT",
        inline=False)
    APIEmbed.add_field(
        name='Last Request Returned:',
        value=last_line,
        inline=False)
    APIEmbed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/844337037830258730/261eeb44b174e3eff886f1f79ae29dee.png?size=256")

    await ctx.send(embed=APIEmbed)


@commands.cooldown(1, 16, commands.BucketType.user)
@bot.command()
async def valm(ctx, *, arg: str):
    await lm.lm(ctx, arg)


@valm.error
async def valm_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'You are on cooldown! Retry in ``{error.retry_after:.1f}s``, please.')


@bot.command()
async def career(ctx, *, args):
    authMessage = await ctx.send("Checking for authorization....")
    await careerF.career(ctx, args)
    await authMessage.delete()


@bot.command()
async def dur(ctx, *, arg):
    newArg = arg.split("#")
    name = newArg[0]
    tag = newArg[1]

    firstResponse = requests.get(
        f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}"
    )
    jsonFR = firstResponse.json()
    puuid = jsonFR["data"]["puuid"]
    response = requests.get(
        f'https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/na/{puuid}')
    jsonR = response.json()

    embedD = discord.Embed(
        title=f"Duration of past 5 games for {name}",
        color=0x00CCFF)
    for j in range(5):

        embedD.add_field(
            name=f"Match {j+1} Duration:",
            value=f"{int((jsonR['data'][j]['metadata']['game_length'])/1000)//60} minutes",
            inline=False,
        )

        embedD.add_field(
            name=f"Match {j+1} Date:",
            value=f"{jsonR['data'][j]['metadata']['game_start_patched']}",
            inline=False
        )

    await ctx.send(embed=embedD)


@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command()
async def vala(ctx, *, arg):
    try:
        msg = await ctx.send(
            f"I'm fetching the five latest games from ``{arg}``'s match history."
        )

        def listToString(l):
            str1 = ""

            for ele in l:
                str1 += ele + " "
            return str1

        def shortenGamemode(mode):
            if str(mode) == "Competitive":
                return "Comp"
            elif str(mode) == "Normal":
                return "Unr"
            elif str(mode) == "Spike Rush":
                return "SpR"
            elif str(mode) == "Deathmatch":
                return "DM"
            elif str(mode) == "Replication":
                return "Repl"
            elif str(mode) == "Unrated":
                return "Unr"
            else:
                return "Unknown"

        kills = []
        deaths = []
        assists = []
        agents = []
        gamemode = []

        compKills = []
        compDeaths = []
        compAssists = []

        unrateKills = []
        unrateDeaths = []
        unrateAssists = []

        dmKills = []
        dmDeaths = []
        dmAssists = []

        replKills = []
        replDeaths = []
        replAssists = []

        fkills = []
        fdeaths = []
        fassists = []

        newArg = arg.split("#")
        name = newArg[0]
        tag = newArg[1]

        async with ctx.typing():
            firstResponse = requests.get(
                f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}"
            )
            jsonFR = firstResponse.json()
            checkStatusCode(jsonFR['status'], "GET-ACCOUNT-PUUID-AND-LEVEL")
            if not jsonFR['status'] == "200":
                return await ctx.send(f"Error occured - status code {jsonFR['status']}. Case recorded.")
            puuid = jsonFR["data"]["puuid"]
            response = requests.get(
                f'https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/na/{puuid}')
            jsonR = response.json()
            checkStatusCode(jsonR['status'], "GET-ACCOUNT-MATCHES")
            if not jsonR['status'] == "200":
                return await ctx.send(f"Error occured - status code {jsonR['status']}. Case recorded.")

            if jsonR["status"] == "200" or jsonR['status'] == 200:

                def checkForWeirdJSON(i):
                    if 'data' in jsonR['data'][i]:
                        secondData = True
                    else:
                        secondData = False

                    if secondData:
                        newPlayers = jsonR['data'][i]['data']['players']['all_players']
                        newMode = jsonR['data'][i]['data']['metadata']['mode']
                    else:
                        newPlayers = jsonR['data'][i]['players']['all_players']
                        newMode = jsonR['data'][i]['metadata']['mode']

                    return newPlayers, newMode

                await msg.edit(
                    content=f"I've fetched the last five games and ``{arg}``'s stats. I'm now averaging ``{arg}``'s perfomance..."
                )

                def mode(i):
                    players, newMode = checkForWeirdJSON(i)
                    try:
                        return newMode
                    except BaseException:
                        if KeyError:
                            return "Unknown"

                Count = []

                def initKD(i):
                    players, newMode = checkForWeirdJSON(i)
                    if newMode == "Competitive":
                        Count.append("comp")
                        for ii in players:
                            if ii["name"] == name or ii["name"] == name.title():
                                compKills.append(ii["stats"]["kills"])
                                compDeaths.append(ii["stats"]["deaths"])
                                compAssists.append(ii["stats"]["assists"])
                    elif newMode == "Normal":
                        Count.append("unrate")
                        for ii in players:
                            if ii["name"] == name or ii["name"] == name.title():
                                unrateKills.append(ii["stats"]["kills"])
                                unrateDeaths.append(ii["stats"]["deaths"])
                                unrateAssists.append(ii["stats"]["assists"])
                    elif (
                        newMode == "Deathmatch"
                    ):
                        Count.append("dm")
                        for ii in players:
                            if ii["name"] == name or ii["name"] == name.title():
                                dmKills.append(ii["stats"]["kills"])
                                dmDeaths.append(ii["stats"]["deaths"])
                                dmAssists.append(ii["stats"]["assists"])
                    elif (
                        newMode == "Replication"
                    ):
                        Count.append("repl")
                        for ii in players:
                            if ii["name"] == name or ii["name"] == name.title():
                                replKills.append(ii["stats"]["kills"])
                                replDeaths.append(ii["stats"]["deaths"])
                                replAssists.append(ii["stats"]["assists"])

                def getOverallKD(compNum, unrateNum, DMNum, replNum):
                    if compNum == 0:
                        compNum = 1
                    if unrateNum == 0:
                        unrateNum = 1
                    if DMNum == 0:
                        DMNum = 1
                    if replNum == 0:
                        replNum = 1

                    compKcounter = round(sum(compKills) / compNum)
                    compDcounter = round(sum(compDeaths) / compNum)
                    compAcounter = round(sum(compAssists) / compNum)

                    unratekcounter = round(sum(unrateKills) / unrateNum)
                    unratedcounter = round(sum(unrateDeaths) / unrateNum)
                    unrateacounter = round(sum(unrateAssists) / unrateNum)

                    dmkcounter = round(sum(dmKills) / DMNum)
                    dmdcounter = round(sum(dmDeaths) / DMNum)
                    dmacounter = round(sum(dmAssists) / DMNum)

                    replkcounter = round(sum(replKills) / replNum)
                    repldcounter = round(sum(replDeaths) / replNum)
                    replacounter = round(sum(replAssists) / replNum)

                    if compDcounter == 0:
                        compDcounter = 1
                    if unratedcounter == 0:
                        unratedcounter = 1
                    if dmdcounter == 0:
                        dmdcounter = 1
                    if repldcounter == 0:
                        repldcounter = 1

                    return (
                        f"{compKcounter}/{compDcounter}/{compAcounter}",
                        round(compKcounter / compDcounter, 2),
                        f"{unratekcounter}/{unratedcounter}/{unrateacounter}",
                        round(unratekcounter / unratedcounter, 2),
                        f"{dmkcounter}/{dmdcounter}/{dmacounter}",
                        round(dmkcounter / dmdcounter, 2),
                        f"{replkcounter}/{repldcounter}/{replacounter}",
                        round(replkcounter / repldcounter, 2),
                    )

                for i in range(5):
                    newPlayers, newMode = checkForWeirdJSON(i)
                    players = newPlayers
                    initKD(i)

                    for ii in players:
                        if ii["name"] == name or ii["name"] == name.title():
                            kills.append(ii["stats"]["kills"])
                            deaths.append(ii["stats"]["deaths"])
                            assists.append(ii["stats"]["assists"])
                            agents.append(ii["character"])
                            gamemode.append(shortenGamemode(mode(i)))

                cCount = Count.count("comp")
                uCount = Count.count("unrate")
                dCount = Count.count("dm")
                rCount = Count.count("repl")

                (
                    compKD,
                    compKDdec,
                    unrateKD,
                    unrateKDdec,
                    dmKD,
                    dmKDdec,
                    replKD,
                    replKDdec,
                ) = getOverallKD(cCount, uCount, dCount, rCount)

                kcounter = 0
                dcounter = 0
                acounter = 0
                kcounter += sum(kills)
                dcounter += sum(deaths)
                acounter += sum(assists)

                fkills.append(round(kcounter / 5))
                fdeaths.append(round(dcounter / 5))
                fassists.append(round(acounter / 5))

                if fkills[0] > fdeaths[0]:
                    color = 0x10B402
                elif fkills[0] < fdeaths[0]:
                    color = 0xDF0606
                else:
                    color = 0xD9D9D9

                finalKDA = f"{fkills[0]}/{fdeaths[0]}/{fassists[0]}"
                finalKDAdec = round(fkills[0] / fdeaths[0], 2)
                newAgent = listToString(agents)
                mostCommonAgent = max(agents, key=agents.count)
                iconFile = discord.File(
                    f"./imgs/agents/{mostCommonAgent}_icon.png")

                fembed = discord.Embed(
                    title=f"{arg} past agent performance",
                    description=f"{newAgent}",
                    color=color,
                )
                fembed.add_field(
                    name="Overall Average KDA",
                    value=f"{finalKDA} ({finalKDAdec})",
                    inline=True,
                )
                fembed.add_field(
                    name="Gamemodes: ",
                    value=listToString(gamemode),
                    inline=True)
                if cCount > 0:
                    fembed.add_field(
                        name="Average Competitive KDA",
                        value=f"{compKD} ({compKDdec})",
                        inline=False,
                    )
                if uCount > 0:
                    fembed.add_field(
                        name="Average Unrated KDA",
                        value=f"{unrateKD} ({unrateKDdec})",
                        inline=True,
                    )
                if dCount > 0:
                    fembed.add_field(
                        name="Average Deathmatch KDA",
                        value=f"{dmKD} ({dmKDdec})")
                if rCount > 0:
                    fembed.add_field(
                        name="Average Replication KDA",
                        value=f"{replKD} ({replKDdec})")
                fembed.set_thumbnail(
                    url=f"attachment://{mostCommonAgent}_icon.png")
                fembed.set_footer(
                    text=f"This is from {name}'s past 5 games only.")
                await ctx.send(file=iconFile, embed=fembed)
                await msg.edit(
                    content=f":smile: Here is the past five games of ``{arg}``, condensed!"
                )

            elif jsonR["status"] == "404":

                await msg.edit(content="Error 404")
                await ctx.send("That player was not found.")

            else:
                await msg.edit(content="An error occured. :(")
                await ctx.send("Try again, or check spelling, tag, etc.")
    except KeyError:
        await msg.edit(content="The server might be down. :pensive:")
        await ctx.send(
            "I didn't receive a response from the server. Try again in about 15 - 20 minutes."
        )
    except BaseException:
        await msg.edit(content='Error 2 || Error 404')
        await ctx.send("That player was not found.")


@vala.error
async def vala_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'You are on cooldown! Retry in ``{error.retry_after:.1f}s``, please.')


@bot.command()
async def lb(ctx, *, args):
    auth = [
        564466359107321856,
        323269361232248832,
        564584121582747659,
        564562239739396098,
        342874810868826112,
        380761443479322624,
        596819291290992640,
        349605838677082123]
    msg = await ctx.send('Checking authorization....')
    if ctx.author.id in auth:
        await msg.edit(content=f'Authorization as <@{ctx.author.id}> was successful. Please allow up to 15 seconds for this command to process.')
        await leaderboard.leaderBoard(ctx, args)
        await msg.delete()
    else:
        await msg.edit(content='Error 4 || Error 401')
        await ctx.send('You are not authorized to use this command. \nUse command ``=error 4`` to see more information.')


@bot.command()
async def valUpdates(ctx):
    msg = await ctx.send(
        "I'm fetching the latest game update, I will send the URL shortly..."
    )

    response = requests.get(
        "https://api.henrikdev.xyz/valorant/v1/website/en-us?filter=game_updates"
    )
    jsonR = response.json()

    firstArticle = jsonR["data"][0]

    embedU = discord.Embed(
        title=firstArticle["title"], url=firstArticle["url"], color=0x00DDFF
    )
    embedU.add_field(name="Date:", value=firstArticle["date"])
    embedU.set_footer(text="https://github.com/5late/Pepe-Bot")
    embedU.set_image(url=firstArticle["banner_url"])

    await ctx.send(embed=embedU)
    await msg.edit(content="Here's the latest patch notes for VALORANT:")


@bot.command()
async def ras(ctx, option=""):
    selectedAgent = []
    selectedAgentNF = []
    selectedAgent.clear()
    selectedAgentNF.clear()

    agentList = [
        "Astra",
        "Breach",
        "Skye",
        "Yoru",
        "Phoenix",
        "Brimstone",
        "Sova",
        "Jett",
        "Reyna",
        "Omen",
        "Viper",
        "Cypher",
        "Killjoy",
        "Sage",
        "Raze",
    ]
    agentListNF = [
        "Astra",
        "Brimstone",
        "Sova",
        "Jett",
        "Reyna",
        "Omen",
        "Viper",
        "Cypher",
        "Killjoy",
        "Sage",
        "Raze",
    ]

    selectedAgent.append(random.choice(agentList))
    selectedAgentNF.append(random.choice(agentListNF))

    first = selectedAgent[0]
    firstNF = selectedAgentNF[0]

    agentImgFile = discord.File(f"./imgs/agents/{first}_icon.png")
    agentImgNFFile = discord.File(f"./imgs/agents/{firstNF}_icon.png")
    embedN = discord.Embed(title="Random Agent Selector", description=first)
    embedN.set_thumbnail(url=f"attachment://{first}_icon.png")
    embedNF = discord.Embed(title="Random Agent Selector", description=firstNF)
    embedNF.set_thumbnail(url=f"attachment://{firstNF}_icon.png")

    if option == "nf":
        await ctx.send(embed=embedNF, file=agentImgNFFile)
    if not option:
        await ctx.send(embed=embedN, file=agentImgFile)


@bot.command()
async def turtles(ctx):
    turtles = [
        "https://cdn.britannica.com/s:800x450,c:crop/66/195966-138-F9E7A828/facts-turtles.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Florida_Box_Turtle_Digon3_re-edited.jpg/1200px-Florida_Box_Turtle_Digon3_re-edited.jpg",
        "https://c402277.ssl.cf1.rackcdn.com/photos/18349/images/hero_small/Sea_Turtle_Hol_Chan_Marine_Reserve_WW1105958.jpg?1576691810",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSuWcKOVFiz01awMOZ3mLV6v2WGERoBMlOFTGHcwBz6sRh7giXfYLRIt4KkjOsx8CLe1z0&usqp=CAU",
    ]
    randomTurtle = random.choice(turtles)

    names = [
        "Tom the Turtle",
        "Turtle the Turtle",
        "Tony the Turtle",
        "Terry the Turtle",
    ]
    randomName = random.choice(names)

    if (
        randomTurtle
        == "https://www.clipartmax.com/png/small/23-231233_i-like-being-a-naked-turtle-by-porygon2z-franklin-turtle-nude.png"
    ):
        randomName = "Franklin"

    turtleEmbed = discord.Embed(
        title=f"Hey there! I'm {randomName}",
        description="Here's a picture of me on vacation!",
        color=0x00CCFF,
    )
    turtleEmbed.set_image(url=randomTurtle)

    await ctx.send(embed=turtleEmbed)


@bot.command()
async def turtle(ctx):
    await ctx.message.delete()
    await ctx.send(
        "https://media.discordapp.net/attachments/801520877753597974/849115199838486539/turtle-removebg-preview_1.png?width=225&height=453"
    )


@bot.command(pass_context=True)
async def randomchoice(ctx, *, question):
    randomAnswers = [
        "Don't bother asking",
        "It will certainly happen",
        "Only to you.",
        "Maybe or maybe not",
    ]

    embed8 = discord.Embed(
        title="The Magic 8ball", description=random.choice(randomAnswers)
    )

    await ctx.send(embed=embed8)


bot.command(
    name="ball",
    pass_context=True,
)(randomchoice.callback)


@bot.command()
async def write(ctx, title: str, url: str):
    if ctx.message.author.id == 564466359107321856:

        def write_json(data, filename="clips.json"):
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)

        with open("clips.json") as json_file:
            data = json.load(json_file)

            temp = data["clips"]
            clips = {"title": title, "url": url}
            temp.append(clips)

        write_json(data)
    else:
        await ctx.send("You are not authorized to use this command.")


@bot.command()
async def read(ctx, title=""):
    servers = [754084714545152101, 839633894403997726, 814335750077153320]
    if ctx.guild.id not in servers:
        return await ctx.send('Sorry, this command is server specific. It is not meant for use outside of bot development! ||Features like this might become public soon, let me know what you think.||')
    if not title:
        clipEmbed = discord.Embed(
            title="Clips I've stored.",
            description="You can also use command ``=read {title}`` to see a specific clip.",
            color=0x00CCFF,
        )
        with open("clips.json") as f:
            data = json.load(f)
            dataClips = data["clips"]
        for i in dataClips:
            clipEmbed.add_field(
                name=i["title"],
                value=f"[Click Here]({i['url']})")

        clipEmbed.set_footer(
            text="As more clips are added, they'll show up here.")
        await ctx.send(embed=clipEmbed)
    else:
        with open("clips.json") as f:
            data = json.load(f)
            dataClips = data["clips"]

        for i in dataClips:
            if i["title"] == title:
                await ctx.send(i["url"])


@bot.command()
async def kissme(ctx):
    if (
        ctx.message.author.id == 543866993602723843
        or ctx.message.author.id == 564466359107321856
        or ctx.message.author.id == 564562239739396098
    ):
        await ctx.send("Ok <:happier:821406857678946394> , nht.")
        await ctx.author.send('Hi qt <:cutepepe:821408779279138887>, u lookin extra nice today <:happier:821406857678946394>. nht <:happy:816424699906752562>')
    else:
        await ctx.send("*Seen*")


@bot.command()
async def vote(ctx):
    voteMsg = await ctx.channel.send("This is a test message for reactions.")
    await voteMsg.add_reaction("✅")
    await voteMsg.add_reaction("❎")
    await asyncio.sleep(30)
    voteMsg = await voteMsg.channel.fetch_message(voteMsg.id)
    positive = 0
    negative = 0

    for reaction in voteMsg.reactions:
        if reaction.emoji == "✅":
            positive = reaction.count - 1
        if reaction.emoji == "❎":
            negative = reaction.count - 1

    print(
        f"Vote Result: {positive} postiive and {negative} negative reactions.")


@bot.command()
async def quiz(ctx):
    voteMsg = await ctx.channel.send("Check mark or X mark?")
    await voteMsg.add_reaction("✅")
    await voteMsg.add_reaction("❎")
    await asyncio.sleep(10)

    voteMsg = await voteMsg.channel.fetch_message(voteMsg.id)
    positive = 0
    negative = 0
    randomC = random.choice(["✅", "❎"])

    try:
        if randomC == "✅" and positive > 0:
            await ctx.send("You guessed correctly!")
        elif randomC == "❎" and negative > 0:
            await ctx.send("You guessed correctly!")
        else:
            await ctx.send("You did not guess correctly.")

        for reaction in voteMsg.reactions:
            if reaction.emoji == "✅":
                positive = reaction.count - 1
            if reaction.emoji == "❎":
                negative = reaction.count - 1

    except BaseException:
        await ctx.send("An error occured.")


WHEN = time(9, 28, 0)  # 6:00 PM
channel_id = 801520877753597974  # Put your channel id here


async def called_once_a_day():
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    await channel.send(
        f"<@564466359107321856>, <@564562239739396098>, <@543866993602723843>, <@380761443479322624> Automated message for **ATTENDANCE** set at {WHEN}. Run command ``=sl`` to get a DM with the attendance link. This message was set to send to <#{channel_id}> by 5|ate."
    )


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


@bot.command()
async def sl(ctx):
    ward = [
        564466359107321856,
        380761443479322624,
        543866993602723843,
        564562239739396098]
    if ctx.author.id in ward:
        await ctx.author.send('https://docs.google.com/forms/d/e/1FAIpQLSfSOKbZkUmo-zGRjuAl33WloeVJVNhJMzQdSqBmn3hPchi8OA/viewform')
    else:
        await ctx.author.send('no')


@bot.command(name="join", help="Joins the voice channel.")
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(
            "{} is not connected to a voice channel".format(ctx.message.author.name)
        )
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name="leave", help="Leaves voice channel.")
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name="play", help="play a youtube URL.")
async def play(ctx, url):
    if str(ctx.message.author.id):
        voice = get(bot.voice_clients, guild=ctx.guild)

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice.play(
                discord.FFmpegPCMAudio(
                    executable="/usr/bin/ffmpeg",
                    source=filename))
        await ctx.send("**Now playing** {}".format(filename))
    else:
        await ctx.send(
            f"{ctx.message.author} is not in the sudoers file. This instance will be reported."
        )


@bot.command()
async def rmd(ctx, time, *, reason: str = ""):
    try:
        timeLen = len(time)
        if not len(reason):
            newReason = f"<@{ctx.message.author.id}>, you set a reminder ``{time}`` ago without a reason."
        else:
            newReason = f"<@{ctx.message.author.id}>, you set a reminder ``{time}`` ago with reason ``{reason}``"
        if timeLen == 3:
            await ctx.send(
                f"I'm setting a reminder for ``{time}`` with reason ``{reason}``! :smile:"
            )
            lastChar = time[-1]
            if lastChar == "m":
                newTime = int(60 * int(time[:2]))
                await asyncio.sleep(newTime)
                await ctx.send(newReason)
            elif lastChar == "s":
                newTime = int(time[:2])
                await asyncio.sleep(newTime)
                await ctx.send(newReason)
            elif lastChar == "h":
                newTime = int(60 * 60 * int(time[:1]))
                await asyncio.sleep(newTime)
                await ctx.send(newReason)
            else:
                await ctx.send("That amount of time is not supported!")
        elif timeLen == 2:
            await ctx.send(
                f"I'm setting a reminder for ``{time}`` with reason ``{reason}``! :smile:"
            )
            lastChar = time[-1]
            if lastChar == "m":
                newTime = int(60 * int(time[:1]))
                print(f"sleeping for {newTime} seconds.")
                await asyncio.sleep(newTime)
                await ctx.send(newReason)
            elif lastChar == "s":
                newTime = int(time[:1])
                await asyncio.sleep(newTime)
                await ctx.send(newReason)
            elif lastChar == "h":
                newTime = int(60 * 60 * int(time[:1]))
                await asyncio.sleep(newTime)
                await ctx.send(newReason)
            else:
                await ctx.send("That amount of time is not supported!")
        else:
            await ctx.send("Value ``time`` must be of length ``2``.")
    except BaseException:
        await ctx.send("An error occured in the command. Check usage, then try again.")


@bot.command()
async def whoami(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author

    secondFont = ImageFont.truetype("./fonts/Hind-Regular.ttf", 110)
    wanted = Image.open("./imgs/background.jpg")

    draw = ImageDraw.Draw(wanted)

    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((450, 450))
    secondText = f"{user.name}#{user.discriminator}"

    draw.text((150, 1075), secondText, (255, 255, 255), font=secondFont)

    wanted.paste(pfp, (250, 500))

    wanted.save("profile.jpg")

    await ctx.send(file=discord.File("profile.jpg"))


@bot.command()
async def braindead(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author

    braindead = Image.open("./imgs/braindead.jpg")

    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((750, 750))

    braindead.paste(pfp, (850, 650))

    braindead.save("stupid.jpg")

    await ctx.send(file=discord.File("stupid.jpg"))


@bot.command()
async def gigachad(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author

    gigachad = Image.open("./imgs/gigachad.jpg")

    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((250, 250))

    gigachad.paste(pfp, (250, 35))

    gigachad.save("chad.jpg")

    await ctx.send(file=discord.File("chad.jpg"))


@bot.command()
async def soyjak(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author

    soyjak = Image.open("./imgs/soyjak.jpg")

    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((300, 300))

    soyjak.paste(pfp, (160, 190))

    soyjak.save("soy.jpg")

    await ctx.send(file=discord.File("soy.jpg"))


@bot.command()
async def talk(ctx, *, args):
    await ctx.send('Error 3\nCommand currently unavailable.')
    '''rs = RandomStuff(api_key=AI_API_KEY)
    response = rs.get_ai_response(args)
    await ctx.send(response['message'])
    rs.close()'''


@bot.command()
@commands.is_owner()
async def test(ctx):
    await ctx.send("sudo works")


@bot.command()
async def gh(ctx):
    await ctx.send("https://github.com/5late/Pepe-Bot")


@bot.command()
async def bj(ctx):
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
    faceCards = ["J", "Q", "K"]
    playerCard = []
    dealerCard = []
    randomCard = random.choice(cards)
    shownCard = random.choice(cards)
    cdc1 = []
    cpc1 = []

    def calcCard(card, cpc):
        if card in faceCards:
            cpc += 10
        elif int(cpc) < 10 and card == "A":
            cpc += 11
        elif int(cpc) >= 10 and card == "A":
            cpc += 1
        elif card == 'a':
            cpc += 1
        else:
            cpc += int(card)
        # print(cpc)
        cpc1.clear()
        cpc1.append(cpc)
        return cpc

    def calcDealerCard(card, cdc):
        if card in faceCards:
            cdc += 10
        elif int(cdc) < 10 and card == "A":
            cdc += 11
        elif int(cdc) >= 10 and card == "A":
            cdc += 1
        elif card == 'a':
            cdc += 1
        else:
            cdc += int(card)
        # print(cdc)
        cdc1.clear()
        cdc1.append(cdc)
        return cdc

    def intize(cpc, cdc):
        dealerCard.append(shownCard)
        dealerCard.append(randomCard)
        playerCard.append(random.choice(cards))
        playerCard.append(random.choice(cards))
        #print('player cards are: ', playerCard)
        #print('shows card is', shownCard)
        #print('dealers cards is ', dealerCard)
        playerCount = int(cpc)
        dealerCount = int(cdc)
        for playerCardnow in playerCard:
            if playerCardnow in faceCards:
                playerCount += 10
            elif int(playerCount) < 10 and "A" in playerCard:
                playerCount += 11
            elif int(playerCount) >= 10 and "A" in playerCard:
                playerCount += 1
            else:
                playerCount += int(playerCardnow)
        for dealerCardnow in dealerCard:
            if dealerCardnow in faceCards:
                dealerCount += 10
            elif int(dealerCount) < 10 and dealerCardnow == "A":
                dealerCount += 11
            elif int(dealerCount) >= 10 and dealerCardnow == "A":
                dealerCount += 1
            else:
                dealerCount += int(dealerCardnow)
        cpc1.clear()
        cdc1.clear()
        cdc1.append(dealerCount)
        cpc1.append(playerCount)

    intize(0, 0)

    def checkGame(count):
        if count >= 21 and "A" in playerCard:
            i = 0
            for i in range(len(playerCard)):
                if playerCard[i] == 'A':
                    playerCard[i] = 'a'
            currentC = (count - 10)
            cpc1.clear()
            cpc1.append(currentC)
            #print('players cards are ', playerCard)

            if cpc1[0] > 21:
                return True
            elif cpc1[0] <= 21:
                return False
        elif count > 21:
            return True
        elif count <= 21:
            return False

    def checkDealerGame(count):
        if count >= 21 and "A" in dealerCard:
            i = 0
            for i in range(len(dealerCard)):
                if dealerCard[i] == 'A':
                    dealerCard[i] = 'a'
            currentC = (count - 10)
            cdc1.clear()
            cdc1.append(currentC)
            # print(dealerCard)

            if cdc1[0] > 21:
                return True
            elif count <= 21:
                return False
        elif count > 21:
            return True
        elif count <= 21:
            return False

    def check(author):
        def inner_check(ctx):
            return ctx.author == author and ctx.content == "h" or "s"

        return inner_check

    def listtoString(list):
        newString = ''
        for item in list:
            newString += f' ``{str(item)}`` '
        return newString

    currentC = calcCard(playerCard[0], 0) + calcCard(playerCard[1], 0)
    cpc1.clear()
    cpc1.append(currentC)

    first_bj_embed = discord.Embed(
        title=f'Blackjack Game for {ctx.author.nick}',
        description='``h`` or ``s`` to hit or stand',
        color=0xcee5e3)
    first_bj_embed.add_field(
        name=f'Your Cards: ``{currentC}``',
        value=f'{listtoString(playerCard)}')
    first_bj_embed.add_field(
        name=f'Dealer Cards: :thinking:',
        value=f'``{shownCard} ?``')

    await ctx.send(embed=first_bj_embed)

    msg = await bot.wait_for("message", check=check(ctx.author), timeout=30)
    if msg.content == "h":
        playerCard.append(random.choice(cards))
        ckGame = checkGame(cpc1[0])
        currentC = calcCard(playerCard[2], cpc1[0])
        ckGame = checkGame(cpc1[0])
        ckDGame = checkDealerGame(cdc1[0])
        if int(cdc1[0]) < 17:
            dealerCard.append(random.choice(cards))
            calcDealerCard(dealerCard[2], cdc1[0])
            if ckDGame and not ckGame:
                win_dealer_embed = discord.Embed(
                    title=f'{ctx.author.nick} Blackjack Game - **WIN**',
                    description='You won!',
                    color=0x12c92d)
                win_dealer_embed.add_field(
                    name=f'Your Cards: ``{cpc1[0]}``',
                    value=f'{listtoString(playerCard)}')
                win_dealer_embed.add_field(
                    name=f'Dealers Cards: ``{cdc1[0]}``',
                    value=f'{listtoString(dealerCard)}')
                return await ctx.send(embed=win_dealer_embed)

            elif ckDGame and ckGame:
                tie_dealer_embed = discord.Embed(
                    title=f'Blackjack Game - {ctx.author.nick} || **TIE**',
                    description='You tied.',
                    color=0xcee5e3)
                tie_dealer_embed.add_field(
                    name=f'Your Cards: ``{cpc1[0]}``',
                    value=f'{listtoString(playerCard)}')
                tie_dealer_embed.add_field(
                    name=f'Dealers Cards: ``{cdc1[0]}``',
                    value=f'{listtoString(dealerCard)}')

                return await ctx.send(embed=tie_dealer_embed)

            elif not ckDGame and ckGame:
                lose_dealer_embed = discord.Embed(
                    title=f'Blackjack Game - {ctx.author.nick} || **LOSE**',
                    description='You lose.',
                    color=0xcee5e3)
                lose_dealer_embed.add_field(
                    name=f'Your Cards: ``{cpc1[0]}``',
                    value=f'{listtoString(playerCard)}')
                lose_dealer_embed.add_field(
                    name=f'Dealers Cards: ``{cdc1[0]}``',
                    value=f'{listtoString(dealerCard)}')

                return await ctx.send(embed=lose_dealer_embed)

        if ckGame:
            busted_embed = discord.Embed(
                title=f'Blackjack Game - {ctx.author.nick} || **LOSS**',
                description='You lost.',
                color=0xc91e12)
            busted_embed.add_field(
                name=f'Your Cards: ``{cpc1[0]}``',
                value=f'{listtoString(playerCard)}')
            busted_embed.add_field(
                name=f'Dealers Cards: ``{cdc1[0]}``',
                value=f'{listtoString(dealerCard)}')
            await ctx.send(
                f"You busted! You pulled a {playerCard[2]}, bringing your total to {currentC}",
                embed=busted_embed
            )
        else:
            first_bj_embed = discord.Embed(
                title=f'Blackjack Game for {ctx.author.nick}',
                description='``h`` or ``s`` to hit or stand',
                color=0xcee5e3)
            first_bj_embed.add_field(
                name=f'Your Cards: ``{cpc1[0]}``',
                value=f'{listtoString(playerCard)}')
            first_bj_embed.add_field(
                name=f'Dealer Cards: :thinking:',
                value=f'``{shownCard} ?``')
            await ctx.send(
                f"You took a {playerCard[2]} from the deck.",
                embed=first_bj_embed
            )

            msg2 = await bot.wait_for("message", check=check(ctx.author), timeout=30)

            if msg2.content == "h":
                playerCard.append(random.choice(cards))
                ckGame = checkGame(cpc1[0])
                calcCard(playerCard[3], cpc1[0])
                ckGame = checkGame(cpc1[0])
                if int(cdc1[0]) < 17:
                    dealerCard.append(random.choice(cards))
                    calcDealerCard(dealerCard[2], cdc1[0])
                    ckDGame = checkDealerGame(cdc1[0])

                    if ckDGame and not ckGame:
                        win_dealer_embed = discord.Embed(
                            title=f'{ctx.author.nick} Blackjack Game - **WIN**',
                            description='You won!',
                            color=0x12c92d)
                        win_dealer_embed.add_field(
                            name=f'Your Cards: ``{cpc1[0]}``',
                            value=f'{listtoString(playerCard)}')
                        win_dealer_embed.add_field(
                            name=f'Dealers Cards: ``{cdc1[0]}``',
                            value=f'{listtoString(dealerCard)}')

                        return await ctx.send(embed=win_dealer_embed)

                    elif ckDGame and ckGame:
                        tie_dealer_embed = discord.Embed(
                            title=f'Blackjack Game - {ctx.author.name} || **TIE**',
                            description='You tied.',
                            color=0xcee5e3)
                        tie_dealer_embed.add_field(
                            name=f'Your Cards: ``{cpc1[0]}``',
                            value=f'{listtoString(playerCard)}')
                        tie_dealer_embed.add_field(
                            name=f'Dealers Cards: ``{cdc1[0]}``',
                            value=f'{listtoString(dealerCard)}')

                        return await ctx.send(embed=tie_dealer_embed)

                if ckGame:
                    busted_embed = discord.Embed(
                        title=f'Blackjack Game - {ctx.author.nick} || **LOSS**',
                        description='You lost.',
                        color=0xc91e12)
                    busted_embed.add_field(
                        name=f'Your Cards: ``{cpc1[0]}``',
                        value=f'{listtoString(playerCard)}')
                    busted_embed.add_field(
                        name=f'Dealers Cards: ``{cdc1[0]}``',
                        value=f'{listtoString(dealerCard)}')
                    await ctx.send(
                        f"You busted! You pulled a {playerCard[3]}, bringing your total to {cpc1[0]}",
                        embed=busted_embed
                    )
                else:
                    first_bj_embed = discord.Embed(
                        title=f'Blackjack Game for {ctx.author.nick}',
                        description='``h`` or ``s`` to hit or stand',
                        color=0xcee5e3)
                    first_bj_embed.add_field(
                        name=f'Your Cards: ``{cpc1[0]}``',
                        value=f'``{listtoString(playerCard)}``')
                    first_bj_embed.add_field(
                        name=f'Dealer Cards: :thinking:',
                        value=f'``{shownCard} ?``')

                    await ctx.send(
                        f"You took a {playerCard[3]} from the deck. Your new cards are: {playerCard}. Your total is {cpc1[0]}",
                        embed=first_bj_embed
                    )
                    msg3 = await bot.wait_for(
                        "message", check=check(ctx.author), timeout=30
                    )

                    if msg3.content == "h":
                        playerCard.append(random.choice(cards))
                        ckGame = checkGame(cpc1[0])
                        currentC = calcCard(playerCard[4], cpc1[0])
                        ckGame = checkGame(cpc1[0])
                        if int(cdc1[0]) < 17:
                            dealerCard.append(random.choice(cards))
                            calcDealerCard(dealerCard[2], cdc1[0])
                            ckDGame = checkDealerGame(cdc1[0])
                            if ckDGame and not ckGame:
                                win_dealer_embed = discord.Embed(
                                    title=f'{ctx.author.nick} Blackjack Game - **WIN**',
                                    description='You won!',
                                    color=0x12c92d)
                                win_dealer_embed.add_field(
                                    name=f'Your Cards: ``{cpc1[0]}``', value=f'{listtoString(playerCard)}')
                                win_dealer_embed.add_field(
                                    name=f'Dealers Cards: ``{cdc1[0]}``',
                                    value=f'{listtoString(dealerCard)}')

                                return await ctx.send(embed=win_dealer_embed)
                            elif ckDGame and ckGame:
                                tie_dealer_embed = discord.Embed(
                                    title=f'Blackjack Game - {ctx.author.name} || **TIE**',
                                    description='You tied.',
                                    color=0xcee5e3)
                                tie_dealer_embed.add_field(
                                    name=f'Your Cards: ``{cpc1[0]}``', value=f'{listtoString(playerCard)}')
                                tie_dealer_embed.add_field(
                                    name=f'Dealers Cards: ``{cdc1[0]}``',
                                    value=f'{listtoString(dealerCard)}')

                                return await ctx.send(embed=tie_dealer_embed)
                            if ckGame:
                                busted_embed = discord.Embed(
                                    title=f'Blackjack Game - {ctx.author.nick} || **LOSS**',
                                    description='You lost.',
                                    color=0xc91e12)
                                busted_embed.add_field(
                                    name=f'Your Cards: ``{cpc1[0]}``',
                                    value=f'{listtoString(playerCard)}')
                                busted_embed.add_field(
                                    name=f'Dealers Cards: ``{cdc1[0]}``',
                                    value=f'{listtoString(dealerCard)}')
                                await ctx.send(
                                    f"You busted! You pulled a {playerCard[4]}, bringing your total to {currentC}",
                                    embed=busted_embed
                                )
                            else:
                                finalEmbed = discord.Embed(
                                    title="Black Jack",
                                    description=f"You win! You drew 5 cards without going over 21!",
                                )
                                finalEmbed.add_field(
                                    name="Your cards", value=playerCard)

                                await ctx.send(
                                    f"You took a {playerCard[4]} from the deck. Your new cards are: {playerCard}. Your total is {currentC}", embed=finalEmbed
                                )

                    elif msg3.content == "s":
                        stand_and_lose = discord.Embed(
                            title=f'Blackjack Game - {ctx.author.nick} || **LOSE**',
                            description='You lose.',
                            color=0xc91e12)
                        stand_and_lose.add_field(
                            name=f'Your Cards: ``{cpc1[0]}``',
                            value=f'{listtoString(playerCard)}')
                        stand_and_lose.add_field(
                            name=f'Dealers Cards: ``{cdc1[0]}``',
                            value=f'{listtoString(dealerCard)}')

                        stand_and_tie = discord.Embed(
                            title=f'Blackjack Game - {ctx.author.nick} || **TIE**',
                            description='You tied.',
                            color=0xcee5e3)
                        stand_and_tie.add_field(
                            name=f'Your Cards: ``{cpc1[0]}``',
                            value=f'{listtoString(playerCard)}')
                        stand_and_tie.add_field(
                            name=f'Dealers Cards: ``{cdc1[0]}``',
                            value=f'{listtoString(dealerCard)}')

                        if cpc1[0] > cdc1[0]:
                            stand_and_win = discord.Embed(
                                title=f'Blackjack Game - {ctx.author.nick} || **WIN**',
                                description='You won!',
                                color=0x12c92d)
                            stand_and_win.add_field(
                                name=f'Your Cards: ``{cpc1[0]}``',
                                value=f'{listtoString(playerCard)}')
                            stand_and_win.add_field(
                                name=f'Dealers Cards: ``{cdc1[0]}``',
                                value=f'{listtoString(dealerCard)}')
                            await ctx.send(f"You stood and ***WON***.", embed=stand_and_win)
                        elif cdc1[0] > cpc1[0]:
                            await ctx.send(f'You stood and ***LOST***.', embed=stand_and_lose)
                        else:
                            await ctx.send(f'You stood and ***TIED***', embed=stand_and_tie)

            elif msg2.content == "s":
                stand_and_lose = discord.Embed(
                    title=f'Blackjack Game - {ctx.author.nick} || **LOSE**',
                    description='You lose.',
                    color=0xc91e12)
                stand_and_lose.add_field(
                    name=f'Your Cards: ``{cpc1[0]}``',
                    value=f'{listtoString(playerCard)}')
                stand_and_lose.add_field(
                    name=f'Dealers Cards: ``{cdc1[0]}``',
                    value=f'{listtoString(dealerCard)}')

                stand_and_tie = discord.Embed(
                    title=f'Blackjack Game - {ctx.author.nick} || **TIE**',
                    description='You tied.',
                    color=0xcee5e3)
                stand_and_tie.add_field(
                    name=f'Your Cards: ``{cpc1[0]}``',
                    value=f'{listtoString(playerCard)}')
                stand_and_tie.add_field(
                    name=f'Dealers Cards: ``{cdc1[0]}``',
                    value=f'{listtoString(dealerCard)}')
                if cpc1[0] > cdc1[0]:
                    stand_and_win = discord.Embed(
                        title=f'Blackjack Game - {ctx.author.nick} || **WIN**',
                        description='You won!',
                        color=0x12c92d)
                    stand_and_win.add_field(
                        name=f'Your Cards: ``{cpc1[0]}``',
                        value=f'{listtoString(playerCard)}')
                    stand_and_win.add_field(
                        name=f'Dealers Cards: ``{cdc1[0]}``',
                        value=f'{listtoString(dealerCard)}')
                    await ctx.send(f"You stood and ***WON***.", embed=stand_and_win)
                elif cdc1[0] > cpc1[0]:
                    await ctx.send(f'You stood and ***LOST***.', embed=stand_and_lose)
                else:
                    await ctx.send(f'You stood and ***TIED***', embed=stand_and_tie)

    elif msg.content == "s":
        stand_and_lose = discord.Embed(
            title=f'Blackjack Game - {ctx.author.nick} || **LOSE**',
            description='You lose.',
            color=0xc91e12)
        stand_and_lose.add_field(
            name=f'Your Cards: ``{cpc1[0]}``',
            value=f'{listtoString(playerCard)}')
        stand_and_lose.add_field(
            name=f'Dealers Cards: ``{cdc1[0]}``',
            value=f'{listtoString(dealerCard)}')

        stand_and_tie = discord.Embed(
            title=f'Blackjack Game - {ctx.author.nick} || **TIE**',
            description='You tied.',
            color=0xcee5e3)
        stand_and_tie.add_field(
            name=f'Your Cards: ``{cpc1[0]}``',
            value=f'{listtoString(playerCard)}')
        stand_and_tie.add_field(
            name=f'Dealers Cards: ``{cdc1[0]}``',
            value=f'{listtoString(dealerCard)}')
        if cpc1[0] > cdc1[0]:
            stand_and_win = discord.Embed(
                title=f'Blackjack Game - {ctx.author.nick} || **WIN**',
                description='You won!',
                color=0x12c92d)
            stand_and_win.add_field(
                name=f'Your Cards: ``{cpc1[0]}``',
                value=f'{listtoString(playerCard)}')
            stand_and_win.add_field(
                name=f'Dealers Cards: ``{cdc1[0]}``',
                value=f'{listtoString(dealerCard)}')
            await ctx.send(f"You stood and ***WON***.", embed=stand_and_win)
        elif cdc1[0] > cpc1[0]:
            await ctx.send(f'You stood and ***LOST***.', embed=stand_and_lose)
        else:
            await ctx.send(f'You stood and ***TIED***', embed=stand_and_tie)


@bot.command()
async def error(ctx, command=""):
    if not command:
        ctx.send(
            "Hey! This command provides in depth information about different errors. If you're looking for help, use the ``=help`` command instead!"
        )
    elif str(command) == "1":
        embedvalm = discord.Embed(
            title="VALM Error 1",
            description="``=valm`` is a command that lets you see someones past match!",
            color=0x00CCFF,
        )
        embedvalm.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url)
        embedvalm.add_field(
            name="Unknown Map/Gamemode",
            value="If you're wondering why your map image returned with a **?** instead of a map, it means that I could not find the map for that match. The same thing happens with the game mode. Unfortunately there is nothing I can do about this. :(",
            inline=False,
        )
        embedvalm.add_field(
            name="Timed out response",
            value="If you sent a request for your last match and the bot responded that it was querying it, but then did not send back the response, it means that it probably timed out. Sadly there is nothing I can do about this either. :(",
            inline=False,
        )
        embedvalm.add_field(
            name="How to help",
            value="If you know the reason for one of these errors, contact my owner ``Xurxx#7879``.",
        )
        embedvalm.set_footer(text="Thanks for your patience with me! :)")
        await ctx.send(embed=embedvalm)
    elif str(command) == "2":
        embedvalm2 = discord.Embed(
            title="Error 2 || Error 404",
            description="```css\nERROR 404```",
            color=0x00FFCC,
        )
        embedvalm2.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url)
        embedvalm2.add_field(
            name="Info",
            value="Error 2 || Error 404 is returned when the server could not find the player you are looking for. Check your spelling, and/or tag. The other reason is that the player has not played in a long time, and RIOT doesnt let me query that far :(.",
            inline=False,
        )
        embedvalm2.add_field(
            name="How to help",
            value="If you can help, contact ``Xurxx#7879``.",
            inline=False,
        )
        embedvalm2.set_footer(text="Thanks for your patience with me! :)")
        await ctx.send(embed=embedvalm2)
    elif str(command) == "3":
        embedvalm3 = discord.Embed(
            title="Error 3 || Error 410",
            description="```css\nERROR 410```",
            color=0x00CCFF,
        )
        embedvalm3.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url)
        embedvalm3.add_field(
            name="Info",
            value="Error 3 || Error 410 is returned when the bot command does not exist, or the command has not been implemented yet. ",
        )
        embedvalm3.add_field(
            name="What to do",
            value="Unfotunately, there is nothing you can do about the command. You can contact the owner to see when the command will be released, or what happened to it, tho.",
            inline=False,
        )
        embedvalm3.add_field(
            name="How to help",
            value="There isn't much you can do to help. heh.",
            inline=False,
        )
        embedvalm3.set_footer(text="Thanks for your patience with me! :)")
        await ctx.send(embed=embedvalm3)
    elif str(command) == "4":
        embedvalm4 = discord.Embed(
            title="Error 4 || Error 401",
            description="```css\nERROR 401```",
            color=0x00CCFF,
        )
        embedvalm4.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url)
        embedvalm4.add_field(
            name="Info",
            value="Error 4 || Error 401 is returned when you do not have authorization to use a command.",
        )
        embedvalm4.add_field(
            name="What to do",
            value="Unfotunately, there is nothing you can do about the command. You can contact the owner to see how to gain authorization. Auto-authorization is a future project.",
            inline=False,
        )
        embedvalm4.add_field(
            name="How to help",
            value="There is not anything you can do to help. Heh.",
            inline=False,
        )
        embedvalm4.set_footer(text="Thanks for your patience with me! :)")
        await ctx.send(embed=embedvalm4)
    elif str(command) == '5':
        embedvalm5 = discord.Embed(
            title='Error 5 || Error 400',
            description='```css\nERROR 400```',
            color=0x00CCFF)
        embedvalm5.add_field(
            name='Info',
            value='Error 5 || Error 400 is returned when the content type is not supported.',
            inline=False)
        embedvalm5.add_field(
            name='What to do',
            value='Re-send the command with a supported content type.',
            inline=False)
        embedvalm5.add_field(
            name='How to help',
            value='If you know how to support certain content types, you can contact the owner.',
            inline=False)
        embedvalm5.set_footer(text='Thanks for your patience with me! :)')
        await ctx.send(embed=embedvalm5)


@bot.command()
async def changelog(ctx, arg=""):
    if not arg:
        await ctx.send(
            "This command is used to send the changelog of a recent update. I try to keep this as up to date as possible, but you can also check https://github.com/5late/Pepe-Bot for updates and/or more information. Thanks. :)"
        )
    elif arg == "latest":
        msg = await ctx.send("I'm fetching the latest update for PepeBot. Hang tight.")
        await asyncio.sleep(2)
        await msg.edit(content="Error 3 || Error 410")
        await ctx.send("This command is currently not ready. Check back later.")
        await ctx.send("You can run ``=error 3`` for more information.")
    elif arg == 'cb':
        msg2 = await ctx.send('Checking for authorization....')

        cauth = [564466359107321856]
        if ctx.author.id in cauth:
            await msg2.edit(content=f'Successfully authorized as <@{ctx.author.id}>. Fetching changelog....')
            f = open('./docs/changelog.md', 'r')
            code_block = f.read()
            await ctx.send(f'```{code_block[:1990]}....```')
        else:
            await msg2.edit(content=f'Error 4 || Error 401')
            await ctx.send(f'Your ID is not recognized.\nYou can run ``=error 4`` for more information.')
    elif arg == 'f':
        msg3 = await ctx.send('Checking for authorization....')

        fauth = [564466359107321856]
        if ctx.author.id in fauth:
            await msg3.edit(content=f'Successfully authorized as <@{ctx.author.id}>. Fetching changelog....')
            changelogFile = discord.File('./docs/changelog.md')
            await ctx.send(file=changelogFile)
        else:
            await msg3.edit(content=f'Error 4 || Error 401')
            await ctx.send(f'Your ID is not recognized.\nYou can run ``=error 4`` for more information.')
    else:
        await ctx.send(
            f"I don't know what ``{arg}`` is. The arguments I currently accept are: ``latest``, ``cb`` and ``f``."
        )


@bot.command()
async def tempfc(ctx, arg):
    try:
        newArg = arg.split('F')
        C = round(((int(newArg[0]) - 32) / 1.8), 2)
        TempEmbed = discord.Embed(title='Fareinheit to Celcius Converter')
        TempEmbed.add_field(name='Input:', value=f'{newArg[0]}F', inline=True)
        TempEmbed.add_field(name='Output:', value=f'{C}C', inline=True)
        await ctx.send(embed=TempEmbed)
    except ValueError:
        await ctx.send('Value must be of type ``num``.')


@bot.command()
async def compsci(ctx):
    servers = [754084714545152101, 839633894403997726, 814335750077153320]
    if ctx.guild.id not in servers:
        return await ctx.send('Sorry, this command is server specific. It is not meant for use outside of bot development! ||**Features like this might become public soon, let me know what you think.**||')
    await ctx.send(f'Here is the boiler plate comments for compsci. Put this at the top of your file!```//Course Code:  ICS 2O1 \n//Submitted to:  Ms Chan \n//By:  \n//Date: \n//Program Name: \n//Description: \
``` <@{ctx.author.id}>, make sure you actually fill it out <:kek:814531183533883402>')


@bot.command()
async def search(ctx, *, args):
    await ctx.send('Error 3\n Command currently unavailable.')
'''
    embedSearch = discord.Embed(
        title=f'Search Results for {args}',
        description=f'6 Results for {args}')
    result = google.search(args, 2)
    for i in range(6):
        new_name = f'{result[i].name[:35]}...'
        embedSearch.add_field(
            name=f'{new_name}:',
            value=f'[Click Here]({result[i].google_link})')
    embedSearch.set_author(
        name=ctx.author.name,
        icon_url=ctx.author.avatar_url)
    embedSearch.set_footer(text='6 top Google Results')

    await ctx.send(embed=embedSearch)
'''


@commands.cooldown(1, 600, commands.BucketType.user)
@bot.command()
async def report(ctx, *, args):
    await ctx.send('I\'ve received your message! I\'m now transporting the message to my bot dev. Thanks for your help <:happy:816424699906752562>')

    now = datetime.now()
    formatTime = now.strftime("%a, %B %d, %Y | %H:%M")
    bugReport = discord.Embed(
        title='Bug Report!',
        description=f'``{formatTime}``')
    bugReport.add_field(name='Reporter', value=ctx.author.name)
    bugReport.add_field(name='Server', value=ctx.guild.name)
    bugReport.add_field(name='Report', value=f'```{args}```', inline=False)
    bugReport.set_footer(text=f'Author ID is: {ctx.author.id}')

    dev = bot.get_user(564466359107321856)
    await dev.send(embed=bugReport)


@report.error
async def report_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'You are on cooldown! Retry in ``{error.retry_after:.1f}s``, please.')


@bot.command()
async def rr(ctx):
    rickRollEmbed = discord.Embed(
        title='Welcome to Rusty Ricks Residence!',
        description='Our server is a safe space where we are all inclusive, accepting, and kind. As such, before you join our server, you must read and accept our rules. At the end of the rules, there is a link to access the server.',
        color=0xf5ef3b)
    rickRollEmbed.set_author(name='Admin', icon_url=ctx.author.avatar_url)
    rickRollEmbed.add_field(
        name='Rules',
        value=f'[Click Here!](https://tinyurl.com/rustyrickrules)')
    rickRollEmbed.set_footer(
        text='Bot created and maintained by Xurxx#7879',
        icon_url='https://www.streamscheme.com/wp-content/uploads/2020/04/poggers.png')

    await ctx.send(embed=rickRollEmbed)


@bot.command()
async def ui(ctx, member: discord.Member = ''):
    if not member:
        user = ctx.author
    else:
        user = member

    pfp = user.avatar_url
    is_bot = user.bot
    start_date = user.created_at.strftime('%b, %d, %Y')
    name = user.name
    tag = user.discriminator
    nickname = user.display_name

    if not is_bot:
        is_bot_string = 'This user is not a bot.'
    else:
        is_bot_string = 'Beep. Boop. This user is a bot.'

    finalEmbed = discord.Embed(
        title=f'User Information: {name}#{tag}',
        description=is_bot_string,
        color=0x00FFCC)
    finalEmbed.add_field(name='User Creation Date', value=start_date)
    finalEmbed.add_field(name='Nickname', value=nickname)
    finalEmbed.set_thumbnail(url=pfp)

    await ctx.send(embed=finalEmbed)


@bot.command()
async def dankmeme(ctx):
    response = requests.get('https://www.reddit.com/r/dankmemes/hot/.json')
    jsonR = response.json()

    random_number = random.randint(0, 10)
    print(jsonR)
    url = jsonR['data']['children'][0]['data']['url']

    title = jsonR['data']['children'][0]['data']['title']

    meme = discord.Embed(title=title)
    meme.set_image(url=url)

    await ctx.send(embed=meme)


@bot.command()
async def kim(ctx):
    await ctx.send('https://www.youtube.com/watch?v=5vABZIO9yqw')


@bot.command()
async def apologize(ctx):
    await ctx.send(f'<@{ctx.author.id}>:')
    await ctx.send("```I made a severe and continuous lapse in my judgement, and I don’t expect to be forgiven. I’m simply here to apologise.\nWhat we came across in the woods that day was obviously unplanned. The reactions you saw on tape were raw; they were unfiltered. None of us knew how to react or how to feel. I should have never posted the video. I should have put the cameras down and stopped recording what we were going through.\nThere's a lot of things I should have done differently but I didn't. And for that, from the bottom of my heart, I am sorry.\nI want to apologise to the internet. I want to apologise to anyone who has seen the video. I want to apologise to anyone who has been affected or touched by mental illness, or depression, or suicide. But most importantly I want to apologise to the victim and his family.\nFor my fans who are defending my actions, please don't. I don’t deserve to be defended. My goal with my content is always to entertain; to push the boundaries, to be all-inclusive. In the world live in, I share almost everything I do. The intent is never to be heartless, cruel, or malicious.\nLike I said I made a huge mistake. I don’t expect to be forgiven, I’m just here to apologise.\nIm ashamed of myself. I’m disappointed in myself. And I promise to be better. I will be better. Thank you.```")


@bot.command()
async def shop(ctx):
    is_server = False
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        is_server = True
        await ctx.send('While I will continue, for privacy reasons it is best that you DM me, rather than use a server. Keep your passwords hidden!')

    def check(author):
        def inner_check(ctx):
            return ctx.author == author

        return inner_check
    await ctx.send('Please send your USERNAME now.')
    msg = await bot.wait_for("message", check=check(ctx.author), timeout=30)
    new_username = msg.content
    await ctx.send('Please send your PASSWORD now.')
    msg2 = await bot.wait_for("message", check=check(ctx.author), timeout=30)
    new_password = msg2.content

    if is_server:
        await msg2.delete()
        fake = await ctx.send('h')
        await fake.delete()

    shop = checkshop.check_item_shop(
        username=new_username,
        password=new_password)
    time_left = shop[4]
    time_left = time_left // 60  # convert to minutes
    time_left_word = "minutes"
    if time_left >= 60:
        time_left = time_left // 60  # convert to hours
        time_left_word = "hour(s)"
    shop_embed = discord.Embed(
        title=f'Shop for {new_username}',
        description=f'You have {time_left} {time_left_word} left until your shop resets.')
    for item in shop:
        if isinstance(item, str):
            shop_embed.add_field(name='In your SHOP', value=item)
            shop_embed.set_footer(
                text='Your username and password are not ever logged in our systems.')

    await ctx.send(embed=shop_embed)


@bot.command()
async def level(ctx, *, arg):
    newArg = arg.split("#")
    name = newArg[0]
    tag = newArg[1]

    msg = await ctx.send(f'Got it! I\'m fetching the level for {name}#{tag}...')
    firstResponse = requests.get(
        f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}"
    )
    jsonFR = firstResponse.json()
    checkStatusCode(jsonFR['status'], "GET-ACCOUNT-PUUID-AND-LEVEL")
    if not jsonFR['status'] == "200":
        return await ctx.send(f"Error occured - status code {jsonFR['status']}. Case recorded.")
    await msg.edit(content='Fetched level!')
    await asyncio.sleep(0.5)
    puuid = jsonFR['data']['puuid']
    account_level = jsonFR["data"]["account_level"]
    account_img = f"./imgs/account-img/{account_level // 20}.png"

    await msg.edit(content='Fetching player card...')
    secondResponse = requests.get(
        f"https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/na/{puuid}"
    )
    jsonSR = secondResponse.json()
    checkStatusCode(jsonSR['status'], "GET-PLAYER-MATCHES")
    if not jsonSR['status'] == "200":
        return await ctx.send(f"Error occured - status code {jsonSR['status']}. Case recorded.")
    players = jsonSR['data'][0]['players']['all_players']

    for player in players:
        if player['puuid'] == puuid:
            the_player_card = player['player_card']

    await msg.edit(content='Fetched player card!')
    await asyncio.sleep(0.5)

    player_card = Image.open(f"./imgs/PlayerCards/{the_player_card}.tga.png")
    player_card = player_card.resize((57, 57))

    await msg.edit(content='Magically generating image...')
    await asyncio.sleep(0.5)

    background = Image.open(account_img)
    background.paste(player_card, (35, 30))
    font = ImageFont.truetype('./fonts/coolvetica rg.ttf', 25)

    draw = ImageDraw.Draw(background)

    text = f'{account_level}'

    draw.text((55, 85), text, (255, 255, 255), font=font)

    background.save("./imgs/account-img/result.png")
    await ctx.send(file=discord.File(fp='./imgs/account-img/result.png', filename=f'{name}-account-level.png'))
    await msg.edit(content='All done! :smile:')


@bot.command()
async def gottem(ctx):
    await ctx.send('https://www.youtube.com/watch?v=-15VC4Yxzys')


@bot.command()
async def guides(ctx):
    split_v1 = str(ctx.message.attachments).split("filename='")[1]
    filename = str(split_v1).split("' ")[0]
    # saves the file
    await ctx.message.attachments[0].save(fp="guides/{}".format(filename))
    await ctx.send('Downloaded file successfully.')
    full_file = f'guides/{filename}'
    with open(full_file, 'rb') as f:
        files = {'file': open(full_file, 'rb')}
        r = requests.post(IP, files=files)
    await ctx.send(f'Successfully send {filename} to the VPS. Watch <#761409251348185088> for the update to https://5late.github.io/guides .')


@commands.cooldown(1, 16, commands.BucketType.user)
@bot.command()
async def mmr(ctx, *, args):
    try:
        msg = await ctx.send(content='Processing...')
        await mmrhistory.mmrhistory(ctx, args)
        await msg.delete()
    except BaseException:
        print(file='./error_output.txt')


@mmr.error
async def mine_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'You are on cooldown! Retry in ``{error.retry_after:.1f}s``, please.')


@bot.command()
async def peak(ctx, *, args):
    await ctx.send('Processing...')
    await peakrank.peak(ctx, args)


@bot.command()
async def track(ctx, *, args):
    msg = await ctx.send(content='Processing...')
    await livematch.livematch(ctx, args)
    await msg.delete()


@bot.command()
async def beta(ctx, arg=''):
    if arg == '':
        await ctx.send('**Beta testing**\nA command that is in beta may become unstable/not respond at any time. It is a way for me to test a command/log stats/see if its useful. All *you* need to do is use the command now and then, and thats it!\nIf you choose to join, thanks! :punch:')
    else:
        await ctx.send(f'**Beta testing command** ``{arg}``\nA command that is in beta may become unstable/not respond at any time. It is a way for me to test a command/log stats/see if its useful. All *you* need to do is use the command now and then, and thats it!\nIf you choose to join, thanks! :punch:')

@bot.command()
async def checkapi(ctx):
    msg = await ctx.send('I\'m checking each main endpoint...')
    account_response_check = '❌ - Returned Error'
    match_response_check = '❌ - Returned Error'
    mmr_response_check = '❌ - Returned Error'
    
    account_response = requests.get('https://api.henrikdev.xyz/valorant/account/Raj/1337')
    account_response = account_response.json()
    
    if account_response:
        account_response_check = '✅ - Returned 200'
        await msg.edit(content='Account Endpoint returned 200.')
    
    match_response = requests.get('https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/na/01066651-f9b0-55c0-8d3d-674c65351821')
    match_response = match_response.json()
    
    if match_response:
        match_response_check = '✅ - Returned 200'
        await msg.edit(content='Match Endpoint returned 200.')

    mmr_response = requests.get('https://api.henrikdev.xyz/valorant/v2/mmr/na/raj/1337')
    mmr_response = mmr_response.json()
    
    if mmr_response:
        mmr_response_check = '✅ - Returned 200'
        await msg.edit(content='MMR Endpoint returned 200.')

    embed = discord.Embed(title='Check API Endpoints', description='Tested mmr, match and account endpoints.')
    embed.add_field(name='Account Endpoint', value=account_response_check)
    embed.add_field(name='Match Endpoint', value=match_response_check)
    embed.add_field(name='MMR Endpoint', value=mmr_response_check)
    embed.set_footer(text='API stats have moved to =apistats')

    await msg.delete()
    await ctx.send(embed=embed)


if __name__ == "__main__":
    # bot.loop.create_task(background_task())
    bot.run(DISCORD_TOKEN)
