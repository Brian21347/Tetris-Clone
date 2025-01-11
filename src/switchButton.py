import pygame
from constants import *

class SwitchButton:
    def __init__(
        self, 
        screen: pygame.Surface, 
        position: Pii,
        size: Pii,
        text_options: list[str], 
        text_color: str, 
        background_color: str, 
        border_color: str, 
        border_width: int, 
        border_radius: int,
        fill_center: bool
    ) -> None:
        self.screen = screen
        self.position = position
        self.size = size
        
        self.text_options = text_options
        self.text_color = text_color
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.fill_center = fill_center
    
        self.font = pygame.font.SysFont("Roboto", 30)
        self.rect = pygame.rect.Rect(self.position, self.size)

        self.current_text_index = 0
    
    def draw(self):
        if self.fill_center and self.border_width > 0:
            pygame.draw.rect(self.screen, self.background_color, self.rect, 0, self.border_radius)
        pygame.draw.rect(self.screen, self.border_color, self.rect, self.border_width, self.border_radius)
        text = self.font.render(self.text_options[self.current_text_index], True, self.text_color)
        self.screen.blit(
            text, 
            [
                self.position[0] + (self.size[0] - text.get_width()) / 2, 
                self.position[1] + (self.size[1] - text.get_height()) / 2
            ]
        )
    
    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
                self.current_text_index += 1
                self.current_text_index %= len(self.text_options)
        
    def get_displayed_text(self) -> str:
        return self.text_options[self.current_text_index]
