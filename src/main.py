import pygame
from game import Game
from constants import * 


# pygame init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Tetris")


pygame.key.set_repeat(250, 150)


# clock init
clock = pygame.time.Clock()


def main() -> None:
    Game(screen, clock).loop()


if __name__ == "__main__":
    main()
