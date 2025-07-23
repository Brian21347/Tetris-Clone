# TODO: better rotation, smart mouse block placement
# Music from: https://www.classicals.de/tetris-theme


# TODO: include an editor to add custom blocks
#   - block shape + point of rotation
# TODO: fix bug where the blocks don't move up far enough for previews
# TODO: fix the rotation bugs where blocks move left or right in the air due to repeat rotation
# TODO: allow the users to choose their control settings

import pygame
import sys
from typing import NoReturn
from intro import Intro
from game import Game
from outro import Outro
from screen import Action, Screen, ScreenGroup

from constants import *


# pygame init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Tetris Clone")
image = pygame.image.load(LOGO_PATH)
pygame.display.set_icon(image)


pygame.key.set_repeat(DELAY, INTERVAL)


clock = pygame.time.Clock()


def screen_controller(group: ScreenGroup, updated_screen: Screen, action: Action):
    if type(updated_screen) == Intro:
        assert action == Action.hide
        group.add(Game())
        group.remove(updated_screen)
    elif type(updated_screen) == Game:
        assert action == Action.hide
        group.add(Outro())
        group.remove(updated_screen)
    elif type(updated_screen) == Outro:
        assert action == Action.hide
        group.add(Game())
        group.remove(updated_screen)


screens = ScreenGroup({Intro()}, screen_controller)


def main() -> NoReturn:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            screens.update(event)
        screen.fill(BG_COLOR)
        screens.draw()
        pygame.display.flip()
        clock.tick(FRAME_RATE)


if __name__ == "__main__":
    main()
