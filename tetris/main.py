# TODO: better rotation, smart mouse block placement
# Music from: https://www.classicals.de/tetris-theme


# TODO: include an editor to add custom blocks
#   - block shape + point of rotation
# TODO: fix bug where the blocks don't move up far enough for previews
# TODO: fix the rotation bugs where blocks move left or right in the air due to repeat rotation
# TODO: allow the users to choose their control settings

import pygame
import pygame.locals
from intro import Intro
from game import Game
from outro import Outro

from constants import *


# pygame init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
screen.set_alpha()
pygame.display.set_caption("Tetris Clone")
image = pygame.image.load(LOGO_PATH)
pygame.display.set_icon(image)


pygame.key.set_repeat(DELAY, INTERVAL)


clock = pygame.time.Clock()


def main() -> None:
    Intro(screen, clock).loop()
    while True:
        Game(screen, clock).loop()
        Outro(screen, clock).loop()


if __name__ == "__main__":
    try:
        main()
    except GameExit:
        exit(1)
