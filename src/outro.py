import pygame
from sys import exit


class Outro:
    def __init__(
        self, 
        screen: pygame.Surface, 
        clock: pygame.time.Clock, 
        high_score: int
    ) -> None:
        self.screen = screen
        self.clock = clock
        self.high_score = high_score
        
    def loop(self) -> None:
        empty = pygame.surface.Surface(self.screen.get_size())
        empty.set_alpha(125)
        empty.fill("gray")
        self.screen.blit(empty, (0, 0))
        text = self.font.render("Game over", True, "black")
        self.screen.blit(
            text, 
            [
                self.screen.get_width() / 2 - text.get_width() / 2, 
                self.screen.get_height() / 2 - text.get_height() / 2
            ]
        )
        pygame.display.flip()
        exit(0)
        
    