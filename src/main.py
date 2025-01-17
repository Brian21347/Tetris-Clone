# TODO: better rotation, smart mouse block placement
# Music from: https://www.classicals.de/tetris-theme

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
