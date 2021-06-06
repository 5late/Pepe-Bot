# PepeBot Changelog

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
