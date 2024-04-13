import pygame
from block import Block
# from blockGroup import BlockGroup
from tetrisBlock import TetrisBlock
from constants import *


class Game:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock
        self.controlled_block = TetrisBlock(
            self.screen,
            7
        )
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
            self.draw()

    def draw(self) -> None:
        self.screen.fill(BG_COLOR)
        self.controlled_block.draw()
        self.draw_grid(HOLD_GRID_START, HOLD_GRID_SIZE)
        self.draw_grid(FIELD_GRID_START, FIELD_GRID_SIZE)
        pygame.display.flip()

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
