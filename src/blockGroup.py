import pygame
from block import Block
from constants import *
from collections import defaultdict


class BlockGroup(pygame.sprite.Group):
    def __init__(self, screen: pygame.Surface, *blocks: Block):
        super().__init__(*blocks)
        self.screen = screen
    
    def check_lines(self):
        blocks_by_line: defaultdict[int, list[Block]] = defaultdict(list)
        for sprite in self.sprites():
            blocks_by_line[sprite.position[1]].append(sprite)
        for _, blocks in blocks_by_line.items():
            if len(blocks) == BLOCKS_TO_CLEAR_LINE:
                [block.kill() for block in blocks]
    
    def update(self, *args):
        pass
    
    def draw(self):
        super().draw(self.screen)
