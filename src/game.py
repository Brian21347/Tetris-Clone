import pygame
from blockGroup import BlockGroup
from tetrisBlock import TetrisBlock
from block import Block
from random import shuffle
from constants import *


class Game:
    held: TetrisBlock
    upcomming: list[TetrisBlock] = []


    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock
        self.obstacle_group = BlockGroup(self.screen)
        self.controlled_block = TetrisBlock(
            self.screen,
            7,
            self.obstacle_group
        )
        self.queue = []
        self.add_to_queue()
        self.add_to_queue()
        self.controlled_block.controlled()

    def loop(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                self.controlled_block.update(event)
            self.controlled_block.check_move_down()

            if not self.controlled_block.sprites():  # check if the block was placed
                self.controlled_block.add_block(self.queue.pop(0))
                if len(self.queue) <= 7:
                    self.add_to_queue()
                self.controlled_block.line_clears += self.obstacle_group.check_lines()
            
            self.draw()

    def show_preview(self) -> None:
        preview_block = self.controlled_block.clone()
        preview_block.hard_drop(kill=False)
        for sprite in preview_block.sprites():
            sprite: Block
            img = self.controlled_block.sprites()[0].image
            rect = pygame.rect.Rect(*sprite.rect.topleft, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(self.screen, img.get_at([0, 0]), rect, BLOCK_OUTLINE_SIZE)

    def draw(self) -> None:
        self.screen.fill(BG_COLOR)
        self.obstacle_group.draw()
        self.controlled_block.draw()
        self.show_preview()
        self.draw_grid(HOLD_GRID_START, HOLD_GRID_SIZE)
        self.draw_grid(FIELD_GRID_START, FIELD_GRID_SIZE)
        pygame.display.flip()

    def add_to_queue(self):
        l = list(range(1, 8))
        shuffle(l)
        self.queue.extend(l)

    def update(self) -> None:
        self.clock.tick(FRAME_RATE)

    def draw_grid(self, starting_position: Coordinate, size: Coordinate) -> None:
        for x in range(0, size[0] + 1, BLOCK_SIZE):
            x += starting_position[0]
            pygame.draw.line(self.screen, GRID_COLOR, (x,
                             starting_position[1]), (x, starting_position[1] + size[1]))
        for y in range(0, size[1] + 1, BLOCK_SIZE):
            y += starting_position[1]
            pygame.draw.line(self.screen, GRID_COLOR,
                             (starting_position[0], y), (starting_position[0] + size[0], y))
