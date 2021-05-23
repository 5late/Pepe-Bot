 try:
    msg = await ctx.send(
              f"Your message has been registered and I'm working hard to query, read, format, and send you the last match for ``{arg}``. Hang tight!"
          )

          def mapImg(imap):
              if imap == "Haven":
                  return "https://static.wikia.nocookie.net/valorant/images/7/70/Loading_Screen_Haven.png/revision/latest/scale-to-width-down/1000?cb=20200620202335"
              elif imap == "Ascent":
                  return "https://static.wikia.nocookie.net/valorant/images/e/e7/Loading_Screen_Ascent.png/revision/latest/scale-to-width-down/1000?cb=20200607180020"
              elif imap == "Icebox":
                  return "https://static.wikia.nocookie.net/valorant/images/3/34/Loading_Icebox.png/revision/latest/scale-to-width-down/1000?cb=20201015084446"
              elif imap == "Split":
                  return "https://static.wikia.nocookie.net/valorant/images/d/d6/Loading_Screen_Split.png/revision/latest/scale-to-width-down/1000?cb=20200620202349"
              elif imap == "Bind":
                  return "https://static.wikia.nocookie.net/valorant/images/2/23/Loading_Screen_Bind.png/revision/latest/scale-to-width-down/1000?cb=20200620202316"
              elif imap == "Breeze":
                  return "https://www.ginx.tv/uploads2/Valorant/breeze_mapp.png"

          newArg = arg.split("#")
          name = newArg[0]
          tag = newArg[1]

          async with ctx.typing():
              response = requests.get(
                  f"https://api.henrikdev.xyz/valorant/v3/matches/na/{name}/{tag}"
              )
              jsonR = response.json()

              players = jsonR["data"]["matches"][0]["players"]["all_players"]
              convertD = datetime.fromtimestamp(
                  int(jsonR["data"]["matches"][0]["metadata"]["game_start"]) / 1000.0
              )
              finalT = convertD.strftime("%a, %b %d, %Y | %H:%M")

              def mode():
                  try:
                      return jsonR["data"]["matches"][0]["metadata"]["mode"]
                  except BaseException:
                      if KeyError:
                          return "Unknown"

              def map():
                  try:
                      return mapImg(
                          str(jsonR["data"]["matches"][0]["metadata"]["map"]))
                  except KeyError:
                      return "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/200px-Question_mark_%28black%29.svg.png"

              for i in players:
                  if i["name"] == name or i["name"] == name.title():
                      team = str(i["team"]).lower()
                      puuid = i["puuid"]
                      if str(mode()) == "Deathmatch":
                          if (jsonR["data"]["matches"][0]["rounds"]
                                  [0]["winning_team"] == puuid):
                              color = 0x10B402
                          elif (
                              not jsonR["data"]["matches"][0]["rounds"][0]["winning_team"]
                              == puuid
                          ):
                              color = 0xDF0606
                          else:
                              color = 0x3B3D3C
                          won = i["stats"]["kills"]
                          lost = i["stats"]["deaths"]

                      else:
                          if (
                              jsonR["data"]["matches"][0]["teams"][team]["rounds_won"]
                              > jsonR["data"]["matches"][0]["teams"][team]["rounds_lost"]
                          ):
                              color = 0x10B402
                          elif (
                              jsonR["data"]["matches"][0]["teams"][team]["rounds_won"]
                              < jsonR["data"]["matches"][0]["teams"][team]["rounds_lost"]
                          ):
                              color = 0xDF0606
                          else:
                              color = 0xD1D1D1
                          won = jsonR["data"]["matches"][0]["teams"][team]["rounds_won"]
                          lost = jsonR["data"]["matches"][0]["teams"][team]["rounds_lost"]

                      global iconFile
                      iconFile = discord.File(
                          f"./imgs/agents/{i['character']}_icon.png")
                      global embedM
                      embedM = discord.Embed(
                          title=f"{i['name']}#{i['tag']}'s last match:",
                          description=f"**{mode()}** | ***{won}-{lost}***",
                          color=color,
                      )
                      embedM.add_field(name="Character: ", value=i["character"])
                      embedM.add_field(
                          name="KDA: ",
                          value=str(i["stats"]["kills"])
                          + "/"
                          + str(i["stats"]["deaths"])
                          + "/"
                          + str(i["stats"]["assists"]),
                      )
                      embedM.add_field(
                          name="Combat Score: ",
                          value=int(i["stats"]["score"])
                          // int(
                              jsonR["data"]["matches"][0]["metadata"]["rounds_played"]
                          ),
                          inline=True,
                      )
                      embedM.add_field(name="Date:", value=finalT)
                      embedM.add_field(
                          name="Duration:",
                          value=f"{int((jsonR['data']['matches'][0]['metadata']['game_length'])/1000)//60} minutes",
                      )
                      embedM.set_thumbnail(
                          url=f"attachment://{i['character']}_icon.png")
                      embedM.set_image(url=str(map()))
                      if mode() == "Unknown":
                          embedM.set_footer(
                              text="Wondering what happened to mode/map? Run command ``=error 1``.")
                      else:
                          embedM.set_footer(
                              text="https://github.com/5late/Pepe-Bot")
                      await asyncio.sleep(1)
                      await ctx.send(file=iconFile, embed=embedM)
                      await msg.edit(
                          content=f":smile: I successfully got last game stats for {name}#{tag}!"
                      )
    except BaseException:
      await msg.edit(content="Error 2||Error 404 :(")
      await ctx.send("Use command ``=error 2`` to see more information.")
