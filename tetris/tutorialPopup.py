import pygame
from constants import *
from text import Text


class TutorialPopup:
    def __init__(self) -> None:
        self.display_screen = pygame.display.get_surface()
        self.__hidden = False

        self.__cover_screen = pygame.surface.Surface(self.display_screen.get_size())
        self.__cover_screen.set_alpha(COVER_SCREEN_TRANSPARENCY)
        self.__cover_screen.fill(COVER_SCREEN_COLOR)

        self.rect = pygame.Rect(
            (SCREEN_WIDTH // 2 - 6 * BLOCK_SIZE, SCREEN_HEIGHT // 2 - 10 * BLOCK_SIZE),
            (12 * BLOCK_SIZE, 20 * BLOCK_SIZE),
        )

    def update(self):
        if self.__hidden:
            return

    def draw(self):
        if self.__hidden:
            return
        self.display_screen.blit(self.__cover_screen, (0, 0))

        # draw background rect
        pygame.draw.rect(
            self.display_screen, BG_COLOR, self.rect, border_radius=BUTTON_BORDER_RADIUS
        )
        pygame.draw.rect(
            self.display_screen,
            BUTTON_BORDER_COLOR,
            self.rect,
            BUTTON_BORDER_SIZE,
            BUTTON_BORDER_RADIUS,
        )

    def show(self):
        self.__hidden = False

    def hide(self):
        self.__hidden = True
