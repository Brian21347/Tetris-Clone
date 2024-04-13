import pygame
from constants import *
from blockGroup import BlockGroup
from block import Block


BlockId = tuple[tuple[Coordinate], Coordinate]


class TetrisBlock(BlockGroup):
    __player_controlled = False
    line_clears: int = 0

    BLOCKS: dict[int, BlockId] = {
        1: (
            # stores the relative positions based off of the top-left of the block
            ((0, 0), (1, 0), (1, 1), (2, 1)),
            # stores the center of the block
            (1, 0)
        ),
        2: (
            ((0, 1), (1, 1), (1, 0), (2, 0)),
            (1, 0)
        ),
        3: (
            ((0, 0), (0, 1), (1, 1), (2, 1)),
            (1, 1),
        ),
        4: (
            ((0, 1), (1, 1), (2, 1), (2, 0)),
            (1, 1),
        ),
        5: (
            ((0, 1), (1, 1), (1, 0), (2, 1)),
            (1, 1)
        ),
        6: (
            ((0, 0), (1, 0), (2, 0), (3, 0)),
            (1, 0)
        ),
        7: (
            ((0, 0), (0, 1), (1, 1), (1, 0)),
            (0, 0)  # no rotation point for the square block
        )
    }

    def __init__(self, screen: pygame.Surface, block_id: int):
        if block_id not in TetrisBlock.BLOCKS:
            raise ValueError("Block Id is not valid.")

        x_offset = (
            (FIELD_GRID_START[0] + FIELD_GRID_SIZE[0] / 2) //
            BLOCK_SIZE - TetrisBlock.BLOCKS[block_id][1][0] - 1
        ) * BLOCK_SIZE
        y_offset = FIELD_GRID_START[1]
        self.previous_time: int = pygame.time.get_ticks()

        super().__init__(
            screen,
            (
                Block(
                    (block[0] * BLOCK_SIZE + x_offset,
                     block[1] * BLOCK_SIZE + y_offset),
                    ASSET_PATH % block_id
                )
                for block in TetrisBlock.BLOCKS[block_id][0]
            )
        )

    def check_move_down(self):
        if (pygame.time.get_ticks() - self.previous_time > INITIAL_MOVEMENT_TIME /
                (LINE_CLEAR_SPEED_UP * TetrisBlock.line_clears // 10 + 1)):
            self.move_down()
            self.previous_time = pygame.time.get_ticks()

    def update(self, event: pygame.event.EventType):
        if not self.__player_controlled:
            return
        if event.type == pygame.KEYDOWN:
            direction: Coordinate = None
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                direction = -BLOCK_SIZE, 0
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                direction = BLOCK_SIZE, 0
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                direction = 0, -BLOCK_SIZE
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                direction = 0, BLOCK_SIZE
            if direction is not None:
                self.move(direction)

    def move(self, direction: Coordinate):
        [sprite.move(direction) for sprite in self.sprites()]

    def controlled(self):
        self.__player_controlled = True

    def uncontrolled(self):
        self.__player_controlled = False

    def is_controlled(self) -> bool:
        return self.__player_controlled

    def add_sprites_to(self, other: BlockGroup) -> None:
        other.add(*self.sprites())
        self.empty()

    def move_down(self):
        [sprite.move_down() for sprite in self.sprites()]
