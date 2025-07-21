import pygame
from constants import *
from util import add_pii, scale_pii
from screen import Screen


class Intro(Screen):
    def __init__(self):
        super().__init__()
        self.start_font = pygame.font.SysFont(FONT, TEXT_SIZE)
        self.start_text = self.start_font.render(START_PROMPT_TEXT, True, START_PROMPT_TEXT_COLOR)
        self.title_font = pygame.font.SysFont(FONT, TITLE_SIZE)
        self.title_text = self.title_font.render(TITLE, True, TITLE_TEXT_COLOR)

    def update(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.hide()
            self.send_action(Action.hide)

    def draw(self) -> None:
        self.screen.blit(
            self.title_text,
            add_pii(TITLE_CENTER_POSITION, scale_pii(self.title_text.get_size(), -1 / 2)),
        )

        self.screen.blit(
            self.start_text,
            add_pii(START_PROMPT_CENTER_POSITION, scale_pii(self.start_text.get_size(), -1 / 2)),
        )
