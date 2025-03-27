import pygame
from block import Block
from constants import *
from collections import defaultdict


class BlockGroup(pygame.sprite.Group):
    def __init__(self, screen: pygame.Surface, *blocks: Block):
        super().__init__(*blocks)
        self.screen = screen
    
    def check_lines(self) -> int:
        line_clears = 0
        
        # removal
        blocks_by_line: defaultdict[int, list[Block]] = defaultdict(list)
        for sprite in self.sprites(): blocks_by_line[sprite.position[1]].append(sprite)
        removed_lines = set()
        for i, blocks in blocks_by_line.items():
            if len(blocks) != BLOCKS_TO_CLEAR_LINE: continue
            removed_lines.add(i)
            line_clears += 1
            [block.kill() for block in blocks]

        # movement
        blocks_by_line: defaultdict[int, list[Block]] = defaultdict(list)
        for sprite in self.sprites(): blocks_by_line[sprite.position[1]].append(sprite)
        for i in removed_lines:
            for j, blocks in blocks_by_line.items():
                if j > i: continue
                [block.move_down() for block in blocks]
        
        return line_clears
    
    def draw(self):
        super().draw(self.screen)
