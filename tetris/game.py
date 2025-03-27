import pygame
from blockGroup import BlockGroup
from tetrisBlock import TetrisBlock
from block import Block
from random import shuffle
from constants import *
from volumeButton import VolumeButton
from switchButton import SwitchButton
from textBox import TextBox


class Game:
    held: TetrisBlock = None
    just_held: bool = False
    
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock
        self.obstacle_group = BlockGroup(self.screen)
        self.controlled_block = TetrisBlock(
            self.screen,
            7,
            self.obstacle_group
        )

        self.grid_screen = pygame.surface.Surface(SCREEN_SIZE).convert_alpha()
        self.grid_screen.fill([0, 0, 0, 0])
        self.draw_grid(HOLD_GRID_START, HOLD_GRID_SIZE)
        self.draw_grid(FIELD_GRID_START, FIELD_GRID_SIZE)
        for y in range(UPCOMING_NUMBER):
            self.draw_grid(
                [UPCOMING_GRID_START[0], UPCOMING_GRID_START[1] + (UPCOMING_GAP_SIZE + UPCOMING_GRID_HIGHT) * y], 
                [4 * BLOCK_SIZE, 2 * BLOCK_SIZE]
            )

        self.queue: list[TetrisBlock] = []
        self.add_to_queue()
        self.add_to_queue()
        self.controlled_block.controlled()

        self.score = 0
        self.font = pygame.font.SysFont("Roboto", 30)

        self.switch_button = SwitchButton(
            self.screen, 
            SWITCH_BUTTON_START, 
            SWITCH_BUTTON_SIZE, 
            SWITCH_BUTTON_THEMES, 
            SWITCH_BUTTON_TEXT_COLOR, 
            SWITCH_BUTTON_BACKGROUND_COLOR, 
            SWITCH_BUTTON_BORDER_COLOR, 
            SWITCH_BUTTON_BORDER_SIZE, 
            SWITCH_BUTTON_BORDER_RADIUS, 
            SWITCH_BUTTON_FILL_CENTER
        )
        
        self.volume_button = VolumeButton(
            self.screen, 
            VOLUME_BUTTON_START,
            VOLUME_BUTTON_SIZE,
            VOLUME_BUTTON_EXPAND_RECT,
            VOLUME_BUTTON_STARTING_VOLUME,
            VOLUME_BUTTON_BACKGROUND_COLOR,
            VOLUME_BUTTON_BORDER_COLOR,
            VOLUME_BUTTON_BORDER_SIZE,
            VOLUME_BUTTON_BORDER_RADIUS,
            VOLUME_BUTTON_FILL_CENTER
        )

        self.text_buttons = [
            TextBox(
                self.screen,
                start,
                TEXT_BUTTON_SIZE,
                text,
                TEXT_BUTTON_TEXT_COLOR,
            ) 
            for start, text in zip(TEXT_BUTTON_STARTS, TEXT_BUTTON_TEXTS)
        ]
        
        self.theme = "Piano"
        
        pygame.mixer.music.load(THEME_ASSET_PATH % self.theme)
        pygame.mixer.music.play(-1)  # play infinitely

    def loop(self) -> int:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise GameExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise GameExit
                    if event.key == pygame.K_c and not self.just_held:
                        self.hold()
                self.score += self.controlled_block.update(event)
                if self.held is not None: self.held.update(event)

                self.volume_button.update(event)
                pygame.mixer.music.set_volume(self.volume_button.get_volume())

                self.switch_button.update(event)
                if self.switch_button.get_displayed_text() != self.theme:
                    self.theme = self.switch_button.get_displayed_text()
                    pygame.mixer.music.load(THEME_ASSET_PATH % self.theme)
                    pygame.mixer.music.play(-1)  # play infinitely
            self.controlled_block.check_move_down()

            if not self.controlled_block.sprites():  # check if the block was placed
                if not self.add_block(): 
                    pygame.mixer.music.fadeout(1)
                    return self.score
            self.draw()

    def add_block(self) -> None:
        self.just_held = False
        self.controlled_block.add_block(self.queue.pop(0).block_id)
        if self.controlled_block.collides(): 
            return False
        for sprite in self.queue:
            sprite.move([0, -UPCOMING_GRID_HIGHT - UPCOMING_GAP_SIZE])
        if len(self.queue) <= 7:
            self.add_to_queue()
        line_clears = self.obstacle_group.check_lines()
        self.controlled_block.line_clears += line_clears
        self.score += POINTS[line_clears] * (self.controlled_block.line_clears // 10 + 1)
        return True

    def hold(self) -> None:
        if self.held is not None:
            tmp = self.held.block_id
            self.held = TetrisBlock(self.screen, self.controlled_block.block_id, self.obstacle_group)
            self.controlled_block.add_block(tmp)
        else:
            self.held = TetrisBlock(self.screen, self.controlled_block.block_id, self.obstacle_group)
            self.add_block()

        self.held.uncontrolled()
        self.held.set_topleft(HOLD_GRID_START)
        self.just_held = True

    def show_preview(self) -> None:
        preview_block = self.controlled_block.clone()
        preview_block.hard_drop(do_kill=False)
        controlled_block_positions = [
            controlled_block_sprite.position for controlled_block_sprite in self.controlled_block.sprites()
        ]
        for sprite in preview_block.sprites():
            if sprite.position in controlled_block_positions:
                continue
            sprite: Block
            img = self.controlled_block.sprites()[0].image
            rect = pygame.rect.Rect(*sprite.rect.topleft, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(self.screen, img.get_at([0, 0]), rect, BLOCK_OUTLINE_SIZE)

    def draw(self) -> None:
        self.screen.fill(BG_COLOR)
        if self.held is not None: 
            self.held.draw()
        self.obstacle_group.draw()
        self.controlled_block.draw()
        self.show_preview()
        [sprite.draw() for sprite in self.queue[:5]]
        self.screen.blit(self.grid_screen, [0, 0])
        self.switch_button.draw()
        self.volume_button.draw()
        for text_button in self.text_buttons:
            text_button.draw()
        
        line_clears = self.controlled_block.line_clears
        score_texts = [self.font.render(text, True, SCORE_COLOR) for text in [f"{self.score:,}", f"{int(line_clears // 10):,}", f"{line_clears:,}"]]
        for text, start_pos in zip(score_texts, SCORE_STARTS):
            self.screen.blit(
                text,
                [
                    start_pos[0] + (SCORE_SIZE[0] - text.get_width()) / 2,
                    start_pos[1] + (SCORE_SIZE[1] - text.get_height()) / 2,
                ]
            )
        pygame.display.flip()

    def add_to_queue(self):
        block_ids = list(range(1, 8))
        shuffle(block_ids)
        for block_id in block_ids:
            self.queue.append(
                TetrisBlock(
                    self.screen, block_id, self.obstacle_group, 
                    x_offset=UPCOMING_GRID_START[0], 
                    y_offset=UPCOMING_GRID_START[1] + len(self.queue) * (UPCOMING_GRID_HIGHT + UPCOMING_GAP_SIZE)
                ) 
            )

    def update(self) -> None:
        self.clock.tick(FRAME_RATE)

    def draw_grid(self, starting_position: Pii, size: Pii) -> None:
        for x in range(0, size[0] + 1, BLOCK_SIZE):
            x += starting_position[0]
            pygame.draw.line(self.grid_screen, GRID_COLOR, (x,
                             starting_position[1]), (x, starting_position[1] + size[1]))
        for y in range(0, size[1] + 1, BLOCK_SIZE):
            y += starting_position[1]
            pygame.draw.line(self.grid_screen, GRID_COLOR,
                             (starting_position[0], y), (starting_position[0] + size[0], y))
