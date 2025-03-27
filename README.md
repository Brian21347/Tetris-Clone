# Tetris-Clone
A simple Tetris clone with a changed color palette.

## Dependencies
* python3
* pygame
```
pip install pygame
```

## Installation
```
git clone https://github.com/Brian21347/Tetris-Clone.git
```

## Usage
From the `tetris` directory, run the following command:
```
python main.py
```
Edit the `constants.py` file to change settings. Editing `BLOCK_SIZE` will scale the size of the grid and screen.

## Features
- Change themes by clicking the button on the bottom left. Available themes are Piano, Music Box, and Strings. The themes are "Korobeiniki" rearranged by Gregor Quendel and which are provided for free [here](https://www.classicals.de/tetris-theme).
- Change the volume of the songs with the songs with by hovering over the volume button in the bottom left above the theme button and dragging the circle on the bar that extends from the right of the volume button. Click on the speaker to mute/unmute the music.

## Controls
`c`: Hold  
`z`: Rotate counter-clockwise  
`w`/`up arrow`: Rotate clockwise  
`a`/`left arrow`: Move block left  
`d`/`right arrow`: Move block right  
`s`/`down arrow`: Move block down one space  
`Space`: Hard drop the block
