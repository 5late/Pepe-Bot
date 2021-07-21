# PepeBot Changelog

## Jul 14 2021

### Updated ``=checkapi`` command!

- Added check of latest request

### Return of ``=valm`` command!

- Use ``=valm USERNAME#TAG`` to get the last match stats of a player
- Cooldown of 16 seconds

## Jul 13 2021

### Updated ``=val`` command!

- Get up to 5 players ranks at once!
- Split the players with ``\\`` between each player
- Max of FIVE players
- Circumvent the 16 second cooldown using this new way.

# IF PLAYER HAS ``//`` IN NAME:

- Use '\' key to "escape" the ``/``.
- Ex:
    ``=val thelegend\//27#1234``
- (you cannot use multiple people if one of them has ``//`` in their name)

## Jul 8 2021

### New ``=level`` command!

- Check people's VALORANT level from Discord!
#### I'm well aware of a bug causing it to appear uncentered, I cannot do much for it unfortunately.

### New ``=checkapi`` command!

- See how the api has been performing on PepeBot!
- The command shows error counts, error codes, and success rates.
- It also shows a start date from which caching began.

## Jul 7 2021

### New ``=val`` command!

- ``=val`` v2 is out!
    - New fresh color
    - Support for Account Level
    - Redesigned embed
    - Disclaimer in footer
- ``career`` is much stricter access
- ``career`` now clears first 2 messages on success (less spammy)
- Reduced cooldown from 30 >> 16 seconds

## Jul 5 2021

### Patches

- Patched a bug with starting the bot
- Removed commands ``=talk`` and ``=search``

### NOTICE: 

**I had to rollback this changelog so it is slightly inaccurate and missing data from Jun 14-Jul 5, sorry.**
**Stable Release soon**

## Jun 14 2021

### Bug Fixes

- Fixed a ``=vala`` bug where Unrated games would show as Unknown

## Jun 11 2021

### New Command

- Added a rule command (rr) ~~you might want to test it~~

### Jun 9 2021

### Major Bug Fixes

- Fixed bug with ``=lb``
- Rewrote the ``=lb`` command, so it works well now

### Bug Fixes

- Fixed a bug where ``=changelog cb`` command would be over 2000 chars, now should send 1990, then ``....``

### Report command

- Report bugs to the dev with the ``=report BUG HERE`` command!

### Jun 7 2021

### Major Bug Fixes

- Issued a much more permanent fix for ``=vala`` and ``=career`` commands
- Issued a bug fix for certain other commands

- VAL COMMAND may not work!
    - This is an API ISSUE.
        - There is nothing I can do to fix this, as the API is the one with the problem, not me.


### Jun 6 2021

### Lots of new features

- Added features for different commands
- Various bug fixes
- WIP bug fix for vala and career, might be an api issue
- WIP bug fix for github push, should be simple fix

### May 20 2021

### Updates to Leaderboard auth-ed command

- The leaderboard command has always been authorized users only.
- You can now get the leaderboard of any of your past 5 games! 
    - To do this, you will now have to use command ``=lb PLAYER#TAG#GAMENUMBER`` 
    <sub>(Note: Game number must be between 1-5)</sub>
- This continues in this update, but to authorized users, the leaderboard now is much cleaner.
- The leaderboard colors have been uplifted as well.
- Fixed bug where everyone had the same amount of kills and deaths.
- Started working on auth command (wow!)

### New Command

**TEMPERATURE COMMAND** 

- Added Fareinheit to Celcius coverter 
    - ``=tempfc NUM``

- Still in testing, will add to [documentation](./commands.md) later

### May 18 2021

### Bug Fixes

- Fixed a bug where the combat score would divide by the first match round number rather than the current one (Deathmatch games were most affected.)
- Fixed a bug where leaderboards showed:
    - One player only
    - One team only
    - Spammed "` ` `"
    - Spammed "','"
    - Did not return anything
    - Had [] wrapped around the players
    - Had players prefixed with "#"
- Fixed bug where Error commands returned different information
- Fixed by where Error commands contained command names (this was intentional but now is much smoother)
- Fixed bugs with vala
- Fixed bugs where bot would return errors on valm commands
- Fixed bug where wrong errors would return on valm commands

## Release 0.1

**Release 0.1 notes can be found [here](https://github.com/5late/Pepe-Bot/releases/tag/v0.1)**
