# archer
Simple pygame program.

### Installation
To run the code:
- Make sure you have pipenv installed
- Navigate to the main folder and type `pipenv install`
- Type `pipenv run start` to open the program

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
