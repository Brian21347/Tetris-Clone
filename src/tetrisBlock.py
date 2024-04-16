import pygame
from constants import *
from blockGroup import BlockGroup
from block import Block
from math import sin, cos, pi


BlockId = tuple[tuple[Coordinate], Coordinate]


class TetrisBlock(BlockGroup):
    __player_controlled = False
    line_clears: int = 0

    BLOCKS: dict[int, BlockId] = {
        1: (  # z block
            (0, 0), (1, 0), (1, 1), (2, 1),
        ),
        2: (  # reverse z block
            (0, 1), (1, 0), (1, 1), (2, 0),
        ),
        3: (  # reverse l block
            (0, 0), (1, 1), (0, 1), (2, 1),
        ),
        4: (  # l block
            (0, 1), (1, 1), (2, 1), (2, 0),
        ),
        5: (  # t block
            (0, 1), (1, 1), (1, 0), (2, 1),
        ),
        6: (  # line block
            (0, 0), (1, 0), (2, 0), (3, 0),
        ),
        7: (  # square block
            (0, 0), (0, 1), (1, 1), (1, 0),
        )
    }

    def __init__(self, screen: pygame.Surface, block_id: int, obstacle_group: BlockGroup):
        if block_id not in TetrisBlock.BLOCKS:
            raise ValueError("Block Id is not valid.")
        self.obstacle_group = obstacle_group
        self.block_id = block_id

        x_offset = (
            (FIELD_GRID_START[0] + FIELD_GRID_SIZE[0] / 2) //
            BLOCK_SIZE - TetrisBlock.BLOCKS[block_id][1][0] - 1
        ) * BLOCK_SIZE
        y_offset = FIELD_GRID_START[1]
        self.previous_time: int = pygame.time.get_ticks()

        super().__init__(
            screen,
            *(
                Block(
                    (block[0] * BLOCK_SIZE + x_offset,
                     block[1] * BLOCK_SIZE + y_offset),
                    ASSET_PATH % block_id
                )
                for block in TetrisBlock.BLOCKS[block_id]
            )
        )

    def check_move_down(self):
        if not (pygame.time.get_ticks() - self.previous_time > INITIAL_MOVEMENT_TIME /
                (LINE_CLEAR_SPEED_UP * TetrisBlock.line_clears // 10 + 1)):
            return
        self.move_down()

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
                self.rotate(1)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.move_down()
            if direction is not None:
                self.checked_move(direction)

    def checked_move(self, direction: Coordinate):
        self.move(direction)
        for sprite in self.sprites():
            if (sprite.position[0] < FIELD_GRID_START[0] or
                    sprite.position[0] >= FIELD_GRID_START[0] + FIELD_GRID_SIZE[0]):
                self.move((-direction[0], -direction[1]))
                break
            if (pygame.sprite.spritecollide(sprite, self.obstacle_group, False)):
                self.move((-direction[0], -direction[1]))
                break

    def move(self, direction: Coordinate):
        [sprite.move(direction) for sprite in self.sprites()]

    def rotate(self, direction: int):
        positions = [sprite.position for sprite in self.sprites()]
        s, c = sin(pi * direction / 2), cos(pi * direction / 2)
        dx, dy = positions[1][0], positions[1][1]
        for i, position in enumerate(positions):
            x, y = position[0] - dx, position[1] - dy
            # rotate +/- 90 degrees
            position = (x * c - y * s + dx, x * s + y * c + dy)
            self.sprites()[i].set_position((position[0], position[1]))
        for sprite in self.sprites():
            while sprite.position[0] < FIELD_GRID_START[0]:
                self.move((BLOCK_SIZE, 0))
            while sprite.position[0] >= FIELD_GRID_START[0] + FIELD_GRID_SIZE[0]:
                self.move((-BLOCK_SIZE, 0))

    def controlled(self):
        self.__player_controlled = True

    def uncontrolled(self):
        self.__player_controlled = False

    def is_controlled(self) -> bool:
        return self.__player_controlled

    def add_sprites_to(self, other: BlockGroup) -> None:
        other.add(*self.sprites())
        self.empty()

    def add_block(self, block_id: int):
        if block_id not in TetrisBlock.BLOCKS:
            raise ValueError("Block Id is not valid.")
        self.block_id = block_id
        x_offset = (
            (FIELD_GRID_START[0] + FIELD_GRID_SIZE[0] / 2) //
            BLOCK_SIZE - TetrisBlock.BLOCKS[block_id][1][0] - 1
        ) * BLOCK_SIZE
        y_offset = FIELD_GRID_START[1]
        self.previous_time: int = pygame.time.get_ticks()
        super().add(
            *(Block(
                (block[0] * BLOCK_SIZE + x_offset,
                 block[1] * BLOCK_SIZE + y_offset),
                ASSET_PATH % block_id
            )
                for block in TetrisBlock.BLOCKS[block_id])
        )

    def move_down(self):
        sprite: Block
        self.previous_time = pygame.time.get_ticks()
        self.move((0, BLOCK_SIZE))
        for sprite in self.sprites():
            if pygame.sprite.spritecollide(sprite, self.obstacle_group, False):
                self.move((0, -BLOCK_SIZE))
                self.add_sprites_to(self.obstacle_group)
                break
            if sprite.position[1] > FIELD_GRID_START[1] + FIELD_GRID_SIZE[1] - BLOCK_SIZE:
                self.move((0, -BLOCK_SIZE))
                self.add_sprites_to(self.obstacle_group)
                break
