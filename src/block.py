import pygame
from constants import *

class Block(pygame.sprite.Sprite):
    def __init__(self, position: Pii, image_path: str) -> None:
        super().__init__()
        self.position = position
        self.image = pygame.transform.scale(pygame.image.load(image_path), [BLOCK_SIZE, BLOCK_SIZE])
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
    
    def move_down(self) -> None:
        self.move((0, BLOCK_SIZE))
    
    def move(self, direction: Pii):
        self.position = self.rect.left + direction[0], self.rect.top + direction[1]
        self.rect.topleft = self.position
    
    def set_position(self, position: Pii):
        self.position = position
        self.rect.topleft = self.position
