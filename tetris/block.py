import pygame
from constants import *
from util import add_pii


IMAGES = {
    i: pygame.transform.scale(pygame.image.load(IMAGE_ASSET_PATH % i), [BLOCK_SIZE, BLOCK_SIZE])
    for i in range(1, 8)
}


class Block(pygame.sprite.Sprite):
    def __init__(self, position: Pii, block_id: int) -> None:
        super().__init__()
        self.position = position
        self.image = IMAGES[block_id]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

    def move_down(self) -> None:
        self.move((0, BLOCK_SIZE))

    def move(self, direction: Pii):
        self.position = add_pii(self.rect.topleft, direction)
        self.rect.topleft = self.position

    def set_position(self, position: Pii):
        self.position = position
        self.rect.topleft = self.position
