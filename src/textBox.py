import pygame
from constants import *

class TextBox:
    def __init__(
        self, 
        screen: pygame.Surface, 
        position: Coordinate,
        size: Coordinate,
        text: str, 
        text_color: str, 
    ) -> None:
        self.screen = screen
        self.position = position
        self.size = size
        
        self.text = text
        self.text_color = text_color
    
        self.font = pygame.font.SysFont("Roboto", 30)
        self.rect = pygame.rect.Rect(self.position, self.size)

    def draw(self):
        text = self.font.render(self.text, True, self.text_color)
        self.screen.blit(
            text, 
            [
                self.position[0] + (self.size[0] - text.get_width()) / 2, 
                self.position[1] + (self.size[1] - text.get_height()) / 2
            ]
        )
