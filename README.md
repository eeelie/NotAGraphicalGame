# NotAGraphicalGame

This repository implements a two-player 'Eight Ball Pool' game in python. The game uses simplified physics to simulate a real game of pool and animates each turn for you. The game can be played from the command line and should work on macos, windows, and ubuntu operating systems.

## How to play the game

To play the game, open a terminal and naviagte to the src directory of this repository. Once in the src directory, run the LetsPlayPool.py file using the following command:

```bash
python LetsPlayPool.py
```

The game will then prompt each player for their name by asking "Player 1, what's your name?" and then "Player 2, what's your name?" Input your player  names by typing in a name and hitting the enter key. Each player will be assigned a team, either solids or stripes. To play, on your turn, you will input a velocity and an angle in degrees. The angles are oriented in the standard orientation where 0 degrees would shoot the cue directly to the right, 90 degreees to the top of the pool table, 180 degrees to the left, and 270 degrees to the bottom of the table. Negative degrees can be used.

After each turn, an animation will pop up. If you are on a Mac and having trouble with the animation not refreshing with the new turn, you can close and reopen the file and the new animation should appear. You can find the animation file in the src directory.

## Additional Files

If you are a new user and want to further develop the code, a noxfile is provided to run the current set of tests. This file can be run using the following command:

```bash
nox -s tests
```
