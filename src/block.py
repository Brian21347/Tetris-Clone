import pygame
from constants import *

class Block(pygame.sprite.Sprite):
    
    def __init__(self, position: Coordinate, image_path: str) -> None:
        super().__init__()
        self.position = position
        self.image = pygame.transform.scale(pygame.image.load(image_path), [BLOCK_SIZE, BLOCK_SIZE])
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
    
    def move_down(self) -> None:
        self.rect.move_ip([0, BLOCK_SIZE])
    
    def move(self, direction: Coordinate):
        self.position = self.rect.left + direction[0], self.rect.top + direction[1]
        self.rect.topleft = self.position
    
    def set_position(self, position: Coordinate):
        self.position = position
        self.rect.topleft = self.position
