# archer
Written in 2018, this is my first "real" program. While I've come a long way
since this, it's fun to look back! archer is built on PyGame, and is an
arcade-style game where the objective is to dodge the projectiles shot at you
by enemy Cubes while also destroying as many Cubes as you can.

### Installation
To play the game:
- Download the newest installer from the [releases page](https://github.com/brycenaddison/archer/releases/)
- Just run the installer! All dependencies are included and installed for you.

To run the code in Python:
- Make sure you have a version of Python 3.6 or newer installed
- Make sure you have pipenv installed
- Navigate to the main folder and type `pipenv install --python [YOUR_VERSION]`
- Type `pipenv run archer` to open the program

### Controls
`esc`: Quit

`tab`: Pause

`←/→ or a/d`: Move left/right

`Space`: Shoot (capped at 7.5 shots/sec)

`Shift`: Dash (1.5 second cooldown)

`Enter`: Start

### Enemies
**Red** 1 hit to kill, 1 shot per 2 seconds

**Green** 1 hit to kill, 1 shot per 2.5 seconds, gives 1 health on kill

**Yellow** 3 hits to kill, 1 shot per 1.5 seconds (turns orange at 2 hits and red at 1 hit)

**Purple** 1 hit to kill, 1 shot per second, moves from side to side

**Blinking** If not killed in time, take 4 damage

**Yellow/Gray** Dodge the red line!
