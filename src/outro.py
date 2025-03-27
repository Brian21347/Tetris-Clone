import pygame
from constants import *
from util import add_vectors, scale_vector


class Outro:
    def __init__(
        self, 
        screen: pygame.Surface, 
        clock: pygame.time.Clock, 
    ) -> None:
        cover_screen = pygame.surface.Surface(screen.get_size())
        cover_screen.set_alpha(COVER_SCREEN_TRANSPARENCY)
        cover_screen.fill(COVER_SCREEN_COLOR)
        screen.blit(cover_screen, (0, 0))
        self.background = screen.copy()
        self.screen = screen
        self.clock = clock
        self.game_over_font = pygame.font.SysFont(FONT, GAME_OVER_SIZE)
        self.game_over_text = self.game_over_font.render(GAME_OVER_PROMPT_TEXT, True, GAME_OVER_TEXT_COLOR)
        self.restart_font = pygame.font.SysFont(FONT, TEXT_SIZE)
        self.restart_prompt_text = self.restart_font.render(RESTART_PROMPT_TEXT, True, RESTART_PROMPT_TEXT_COLOR)

    def loop(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise GameExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
            self.draw()

    def draw(self) -> None:
        self.screen.blit(self.background, [0, 0])
        self.screen.blit(
            self.game_over_text, 
            add_vectors(GAME_OVER_CENTER_POSITION, scale_vector(self.game_over_text.get_size(), -1/2)),
        )

        self.screen.blit(
            self.restart_prompt_text,
            add_vectors(RESTART_PROMPT_CENTER_POSITION, scale_vector(self.restart_prompt_text.get_size(), -1/2))
        )
        pygame.display.flip()
