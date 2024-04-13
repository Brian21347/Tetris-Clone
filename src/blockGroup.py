import pygame
from block import Block
from constants import *


class BlockGroup(pygame.sprite.Group):
    def __init__(self, screen: pygame.Surface, *blocks: Block):
        super().__init__(*blocks)
        self.screen = screen
    
    def remove_line(self):
        pass
    
    def update(self, *args):
        pass
    
    def draw(self):
        super().draw(self.screen)
