import pygame
from constants import *
from util import add_pii, scale_pii
from screen import Screen


class Outro(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.screen = pygame.display.get_surface()
        cover_screen = pygame.surface.Surface(self.screen.get_size())
        cover_screen.set_alpha(COVER_SCREEN_TRANSPARENCY)
        cover_screen.fill(COVER_SCREEN_COLOR)
        self.screen.blit(cover_screen, (0, 0))
        self.background = self.screen.copy()
        self.game_over_font = pygame.font.SysFont(FONT, GAME_OVER_SIZE)
        self.game_over_text = self.game_over_font.render(
            GAME_OVER_PROMPT_TEXT, True, GAME_OVER_TEXT_COLOR
        )
        self.restart_font = pygame.font.SysFont(FONT, TEXT_SIZE)
        self.restart_prompt_text = self.restart_font.render(
            RESTART_PROMPT_TEXT, True, RESTART_PROMPT_TEXT_COLOR
        )

    def update(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.hide()
            self.send_action(Action.hide)

    def draw(self) -> None:
        self.screen.blit(self.background, [0, 0])
        self.screen.blit(
            self.game_over_text,
            add_pii(GAME_OVER_CENTER_POSITION, scale_pii(self.game_over_text.get_size(), -1 / 2)),
        )

        self.screen.blit(
            self.restart_prompt_text,
            add_pii(
                RESTART_PROMPT_CENTER_POSITION,
                scale_pii(self.restart_prompt_text.get_size(), -1 / 2),
            ),
        )
