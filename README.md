# Pinball Game

## Description

Welcome to our Pinball game, a modern take on the classic arcade game. The game begins with 5 balls. Players can launch a ball into the playfield by pressing the space bar. The objective is to accumulate as many points as possible. Achieving a score of 5000 points will release the next ball. Subsequent goals are set at 10000 points, 20000 points, and so on. The game only saves the highest score achieved by a player. To prevent cheating, our scoreboard and savegame data are stored as images.

## Starting the Game

You can start the Pinball game in two ways:

1. Run the `main` function directly.
2. Use the "Run Workspace" launch configuration provided for Visual Studio Code.

## Game Controls

- **Space**: Launch a ball (only if there are no balls currently in play)
- **Left/Right Arrow Keys**: Operate the flippers
- **Esc**: Access the pause menu

## Pause Menu

The pause menu allows you to adjust game settings or return to the Main Menu or Options Menu. When you exit to these menus, the current game state is saved and can be resumed later. The pause menu offers the following options:

- **Scale Application**: Adjust the game's scale to fit your screen.
- **Change Master Volume**: Modify the overall audio volume.
- **Change Music Volume**: Adjust the background music volume.
- **Change SFX Volume**: Alter the volume of sound effects.

## Scoring System

Points are earned by hitting various targets on the playfield. Accumulating a certain number of points will release the next ball into play.
- **Bounce Wall**: Each hit on a bounce wall awards between 10 and 25 points 
- **Bumper**: Hitting the bumpers can give either 50, 100, 150, or 200 points
- **Targets**: If all targets are hit, they collectively award 5000 points 
- **Spring**: Each spring hit gives 25 points, if the ball pases one

## Licensing

This project is licensed under the terms of the MIT License. This means that you are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, provided that the above copyright notice and this permission notice are included in all copies or substantial portions of the software. However, the software is provided "as is", without any warranty.

### Music

The background music used in this game is sourced from [this YouTube video](https://www.youtube.com/watch?v=dx6MIjAP0jk).

### Sound Effects

The sound effects in this game were created using [Sfxr](http://www.drpetter.se/project_sfxr.html) (the [web version](https://sfxr.me/)), a tool for generating sound effects, particularly for video games.

## Project Status

This project was developed as a university project and is currently considered finished. There are numerous issues with the implementation of the Entity Component System (ECS) that would require major refactoring to resolve. As such, further development has been halted. If you wish to fork this project or volunteer to maintain or own it, you are welcome to do so.
