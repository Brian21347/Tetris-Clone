# TODO: score, music, hold, better rotation, next blocks, smart mouse block placement
# Music from: https://www.classicals.de/tetris-theme

import pygame
from game import Game
from constants import * 


# pygame init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
screen.set_alpha()
pygame.display.set_caption("Tetris")


pygame.key.set_repeat(DELAY, INTERVAL)


# clock init
clock = pygame.time.Clock()


def main() -> None:
    Game(screen, clock).loop()


if __name__ == "__main__":
    main()
