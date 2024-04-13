import pygame
from game import Game


# pygame init
pygame.init()
screen = pygame.display.set_mode([800, 1000], pygame.RESIZABLE)
pygame.display.set_caption("Tetris")


pygame.key.set_repeat(250, 150)


# clock init
clock = pygame.time.Clock()


def main() -> None:
    Game(screen, clock).loop()


if __name__ == "__main__":
    main()
