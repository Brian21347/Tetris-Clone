import pygame
from constants import *
from util import add_pii, scale_pii

class TextBox:
    def __init__(
        self, 
        screen: pygame.Surface, 
        position: Pii,
        size: Pii,
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
            add_pii(self.position, scale_pii(self.size, 1/2), scale_pii(text.get_size(), -1/2))
        )
