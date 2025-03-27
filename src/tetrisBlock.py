import pygame
from constants import *
from blockGroup import BlockGroup
from block import Block
from math import sin, cos, pi
from util import add_vectors, scale_vector


BlockId = tuple[tuple[Pii], Pii]


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

    def __init__(
            self, 
            screen: pygame.Surface, 
            block_id: int, 
            obstacle_group: BlockGroup, 
            x_offset=None, 
            y_offset=None
        ) -> None:
        if block_id not in TetrisBlock.BLOCKS: raise ValueError("Block Id is not valid.")
        self.obstacle_group = obstacle_group
        self.block_id = block_id

        if not x_offset:
            # the x offset is: (⌊the middle of the grid / block size⌋ - x position of block second value) * block size
            x_offset = (
                (FIELD_GRID_START[0] + FIELD_GRID_SIZE[0] / 2) //
                BLOCK_SIZE - TetrisBlock.BLOCKS[block_id][1][0] - 1
            ) * BLOCK_SIZE
        if not y_offset: y_offset = FIELD_GRID_START[1]
        self.previous_time: int = pygame.time.get_ticks()

        blocks = [
            Block(
                add_vectors(scale_vector(block, BLOCK_SIZE), (x_offset, y_offset)),
                IMAGE_ASSET_PATH % block_id
            )
            for block in TetrisBlock.BLOCKS[block_id]
        ]

        super().__init__(screen, *(blocks))

    def check_move_down(self):
        movement_time = INITIAL_MOVEMENT_TIME / (LINE_CLEAR_SPEED_UP * (self.line_clears // 10) + 1)
        if pygame.time.get_ticks() - self.previous_time > movement_time: self.move_down()

    def update(self, event: pygame.event.EventType) -> int:
        if not self.__player_controlled: return
        score_bonus = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: score_bonus += self.hard_drop()
            direction: Pii = None
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                direction = -BLOCK_SIZE, 0
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                direction = BLOCK_SIZE, 0
            elif event.key == pygame.K_z:
                self.rotate(-1)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.rotate(1)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.move_down()
                score_bonus += 1
            if direction is not None: self.checked_move(direction)
        return score_bonus

    def hard_drop(self, do_kill=True) -> int:
        score_bonus = 0
        while self.move_down(do_kill): score_bonus += 1
        return score_bonus

    def checked_move(self, direction: Pii):
        self.move(direction)
        if self.collides():
            self.move((-direction[0], -direction[1]))

    def move(self, direction: Pii):
        [sprite.move(direction) for sprite in self.sprites()]

    def rotate(self, direction: int):
        positions = [sprite.position for sprite in self.sprites()]
        sin_val, cos_val = sin(pi * direction / 2), cos(pi * direction / 2)
        dx, dy = positions[1][0], positions[1][1]
        for i, position in enumerate(positions):
            x, y = position[0] - dx, position[1] - dy
            # rotate +/- 90 degrees
            new_position = (x * cos_val - y * sin_val + dx, x * sin_val + y * cos_val + dy)
            self.sprites()[i].set_position(new_position)
        # TODO: check for clipping between sprites after rotating
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

    def collides(self) -> bool:
        for sprite in self.sprites():
            if (sprite.position[0] < FIELD_GRID_START[0] or
                    sprite.position[0] >= FIELD_GRID_START[0] + FIELD_GRID_SIZE[0]):
                return True
            if sprite.position[1] >= FIELD_GRID_START[1] + FIELD_GRID_SIZE[1]:
                return True
            if pygame.sprite.spritecollide(sprite, self.obstacle_group, False):
                return True
        return False

    def set_topleft(self, position: Pii):
        top, left = self.screen.get_size()
        for sprite in self.sprites():
            top = min(sprite.position[1], top)
            left = min(sprite.position[0], left)
        self.move((position[0] - left, position[1] - top))

    def add_block(self, block_id: int):
        self.empty()
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
                IMAGE_ASSET_PATH % block_id
            )
                for block in TetrisBlock.BLOCKS[block_id])
        )

    def move_down(self, do_kill=True) -> bool:
        self.previous_time = pygame.time.get_ticks()
        self.move((0, BLOCK_SIZE))
        if self.collides():
            self.move((0, -BLOCK_SIZE))
            if do_kill: self.add_sprites_to(self.obstacle_group)
            return False
        return True

    def clone(self) -> 'TetrisBlock':
        cloned =  TetrisBlock(self.screen, self.block_id, self.obstacle_group)
        cloned.empty()
        for sprite in self.sprites():
            cloned.add_internal(Block(sprite.rect.topleft, IMAGE_ASSET_PATH % self.block_id))
        return cloned
