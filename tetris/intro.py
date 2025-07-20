import pygame
from constants import *
from util import add_pii, scale_pii


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
                        # just go to the main game loop if any mouse button was pressed
                        return
            self.draw()
    
    def draw(self) -> None:
        self.screen.fill(BG_COLOR)
        self.screen.blit(
            self.title_text,
            add_pii(TITLE_CENTER_POSITION, scale_pii(self.title_text.get_size(), -1/2))
        )

        self.screen.blit(
            self.start_text,
            add_pii(START_PROMPT_CENTER_POSITION, scale_pii(self.start_text.get_size(), -1/2))
        )
        pygame.display.flip()
