import pygame
from constants import *


class Intro:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock
        self.start_font = pygame.font.SysFont(FONT, TEXT_SIZE)
        self.start_text = self.start_font.render(START_PROMPT_TEXT, True, START_PROMPT_TEXT_COLOR)
        self.title_font = pygame.font.SysFont(FONT, TITLE_SIZE)
        self.title_text = self.title_font.render(TITLE, True, TITLE_TEXT_COLOR)
    
    def loop(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise GameExit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise GameExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in [pygame.BUTTON_LEFT, pygame.BUTTON_MIDDLE, pygame.BUTTON_RIGHT]:
                        return
            self.draw()
    
    def draw(self) -> None:
        self.screen.fill(BG_COLOR)
        self.screen.blit(
            self.title_text,
            [
                TITLE_CENTER_POSITION[0] - self.title_text.get_width() / 2,
                TITLE_CENTER_POSITION[1] - self.title_text.get_height() / 2,
            ]
        )

        self.screen.blit(
            self.start_text,
            [
                START_PROMPT_CENTER_POSITION[0] - self.start_text.get_width() / 2,
                START_PROMPT_CENTER_POSITION[1] - self.start_text.get_height() / 2,
            ]
        )
        pygame.display.flip()
