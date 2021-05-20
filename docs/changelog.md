# PepeBot Changelog

### May 20 2021

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
    - Spammed "```"
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