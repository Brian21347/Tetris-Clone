"""
Steps:
    # Make an obj class  # obstacles
    #     Args:
    #         starting pos of block: tuple
    #         dim of block: tuple
    #         color: str, tuple
    #         alignment: 10

    # Make an UI class
    #     Args:
    #         starting pos of block: tuple
    #         dim of block: tuple
    #         background color: str, tuple
    #         text: Any
    #         text color: str, tuple
    #         text size: int
    #         image path: str

    # Make the Button and Slider classes that inherit from the UI class as well.

    Make a basic block class  # preview holding & up next
        Args:
            Pos of block: tuple
            Type of block: int
            Rotation: int
    Make a block class
        inherent from basic block
        Args:
            Starting pos of block: tuple
            Type of block: int
            Rotation: int
        Stats:
            Current pos of block: tuple
            Width of block: int
            Height of block: int
            Current rotation: int
            Possible rotations: int
        Methods:
            Hard drop(self) -> None
            Collision(self, obstacle group: pygame.group.AbstractGroup) -> None
            Moving(self, dir: tuple) -> None
            Rotation(self, how to rotate: bool) -> None
            Splitting(self) -> None

    Create the level function
        the level
            left arrow
                move left
            right arrow
                move right
            up arrow
                turn left
            down arrow
                move down
            z button
                turn right
            space
                hard drop
            escape
                exit
"""

import pygame
from enum import Enum
from typing import Any


class AlignmentTypes(Enum):
    center, c = 0, 0

    # corners
    topleft, tl = 1, 1
    topright, tr = 2, 2
    bottomleft, bl = 3, 3
    bottomright, br = 4, 4

    # center of sides
    midtop, mt = 5, 5
    midbottom, mb = 6, 6
    midleft, ml = 7, 7
    midright, mr = 8, 8

    # sides
    top, t = 9, 9
    bottom, b = 10, 10
    left, l = 11, 11
    right, r = 12, 12


class Obj(pygame.sprite.Sprite):
    def __init__(self,
                 pos: list | tuple,
                 dim: list | tuple,
                 color: str | list | tuple,
                 alignment: AlignmentTypes = AlignmentTypes.tl,
                 alpha: int = 255) -> None:
        """
        Sprite class for rectangular obstacles

        :param pos: Position of the sprite's rect based on alignment
        :param dim: The dimensions of the sprite
        :param color: The color of the sprite
        :param alignment: Where on the sprite is set to pos
        """
        super().__init__()

        # basic setup
        self.pos, self.dim, self.color, self.alignment = tuple(pos), dim, color, alignment

        # image & rect setup
        self.image = pygame.Surface(dim)
        self.set_color(color, alpha)
        self.rect = self.image.get_rect()

        # setting position
        self.set_pos(pos)

    def set_dim(self, dim):
        """Helper function that set's the sprite's dim"""
        self.dim = dim
        self.image = pygame.Surface(dim)
        self.set_color(self.color)

    def set_color(self, color: tuple | list, alpha: int = 255):
        """Helper function that set's the sprite's color"""
        self.color = color
        if isinstance(color, str):
            self.image.fill(color)
            return
        self.image.fill((color[0], color[1], color[2], alpha))

    def set_pos(self,
                pos: list | tuple | int | float,
                alignment: AlignmentTypes = None) -> None:
        """Setting self.pos to pos and setting a specific part of the sprite's rect based off its alignment"""
        if alignment: self.alignment = alignment
        if isinstance(pos, list | tuple):
            self.pos = tuple(pos)
        else:
            if self.alignment == AlignmentTypes.l or self.alignment == AlignmentTypes.r:
                self.pos = pos, self.pos[1]
            else:
                self.pos = self.pos[0], pos
        if self.alignment == AlignmentTypes.c:
            self.rect.center = self.pos

        # corners
        elif self.alignment == AlignmentTypes.tl:
            self.rect.topleft = self.pos
        elif self.alignment == AlignmentTypes.tr:
            self.rect.topright = self.pos
        elif self.alignment == AlignmentTypes.bl:
            self.rect.bottomleft = self.pos
        elif self.alignment == AlignmentTypes.br:
            self.rect.bottomright = self.pos

        # center of sides
        elif self.alignment == AlignmentTypes.mt:
            self.rect.midtop = self.pos
        elif self.alignment == AlignmentTypes.mb:
            self.rect.midbottom = self.pos
        elif self.alignment == AlignmentTypes.ml:
            self.rect.midleft = self.pos
        elif self.alignment == AlignmentTypes.mr:
            self.rect.midright = self.pos

        # sides
        elif self.alignment == AlignmentTypes.t:
            self.rect.top = self.pos[1]
        elif self.alignment == AlignmentTypes.b:
            self.rect.bottom = self.pos[1]
        elif self.alignment == AlignmentTypes.l:
            self.rect.left = self.pos[0]
        elif self.alignment == AlignmentTypes.r:
            self.rect.right = self.pos[0]


class UI(Obj):
    """Base class of all UI elements"""

    def __init__(self,
                 surface: pygame.Surface,
                 start_p: tuple | list,
                 dim: tuple | list,
                 to_return: Any = None,
                 text: Any = '',
                 image_path: str = '', *,
                 back_c: str | tuple | list = 'gray',
                 text_c: str | tuple | list = 'black',
                 text_s: int = 30,
                 tied_to_text: bool = False,
                 text_pos_change: tuple | list = (),
                 alignment: AlignmentTypes = AlignmentTypes.tl,
                 margin: int = 10,
                 alpha: int = 255) -> None:
        """
        :param surface: On what surface a UI element will be drawn on
        :param start_p: The top left of a UI element
        :param dim: The size of a UI element
        :param to_return: What a UI element will return if clicked
        :param text: The text a UI element displays, displays the text at the center of a UI element
        :param back_c: The background color of a UI element
        :param text_c: The color of the text of a UI element
        :param text_s: The size of the text of a UI element
        :param image_path: The path of an image the UI element displays
        :param tied_to_text: Whether the size of the UI element is the bounding box of the size of its text
        :param text_pos_change: Moves where the text is displayed on a UI element, i.e. moving it up 20 pixels
        :param margin: how much space is separates UI elements
        :param alignment: Where on the rectangle is set to the parameter 'start_p'
        :returns the parameter 'to_return'
        """
        super().__init__(start_p, dim, back_c, alignment, alpha)

        # basic setup
        self.surface = surface
        self.to_return = to_return
        self.text = text
        self.back_c = back_c
        self.text_c = text_c
        self.text_s = text_s
        self.image_path = image_path
        self.tied = tied_to_text
        self.text_pos_change = text_pos_change
        self.margin = margin

        # image setup
        if image_path:
            self.image_setup()
        if str(text):  # testing str text because text could be False without it, i.e. False or 0
            self.basic_image_setup()

        # set pos
        self.set_pos(self.pos)

    def set_return(self, to_return):
        self.to_return = to_return

    def check(self, event):
        """Run every tick."""
        if event.type == pygame.KEYDOWN:
            pass
        if event.button == pygame.MOUSEBUTTONDOWN:
            mous_p = pygame.mouse.get_pos()
            if not self.rect.collidepoint(mous_p):
                return
            if event.button == 1:  # left click
                mouse_p = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_p):
                    return self, self.to_return
            elif event.button == 3:  # right click
                pass
            elif event.button == 4:  # scroll up
                pass
            elif event.button == 5:  # scroll down
                pass

    def update(self, *, draw: bool = False, check_clicked: bool = False) -> Any:
        """Functionality that groups of UI elements would all want."""
        if draw:
            if str(self.text):
                self.disp_text()
            self.groups()[0].draw(self.surface)
        if check_clicked:
            mouse_p = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_p):
                return self, self.to_return

    def move(self, displacement: tuple | list):
        """Helper function that moves the position of the UI element by the parameter 'displacement'"""
        self.set_pos((self.pos[0] + displacement[0], self.pos[1] + displacement[1]))

    def disp_text(self) -> None:
        """Helper function that draws text."""
        disp_pos = self.rect.center[0] + self.text_pos_change[0], self.rect.center[1] + self.text_pos_change[1]
        text = pygame.font.Font("Fonts/Roboto-Light.ttf", self.text_s).render(
            str(self.text), True, self.text_c)
        text_rect = text.get_rect(center=disp_pos)
        if 0 < text_rect.bottom and text_rect.top < self.surface.get_height() and 0 < text_rect.right \
                and text_rect.left < self.surface.get_width():
            self.surface.blit(text, text_rect)

    def set_pos(self,
                pos: list | tuple | int | float,
                alignment: AlignmentTypes = None) -> None:
        super().set_pos(pos, alignment)
        rect = self.rect
        for i, sprite in enumerate(self.groups()[0]):
            sprite.rect.top = rect.bottom + self.margin
            sprite.rect = rect

    def image_setup(self) -> None:
        """Helper function that sets up the sprite's image when setting image to an imported image."""
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, self.dim)
        self.rect = self.image.get_rect()

    def basic_image_setup(self) -> None:
        """Helper function that sets up the sprite's image when setting image to a basic surface."""
        if self.tied:
            self.rect = pygame.font.Font("Fonts/Roboto-Light.ttf", self.text_s).render(
                str(self.text), True, self.text_c).get_rect()
            self.set_dim((self.rect.width + self.margin, self.rect.height + self.margin))
        else:
            self.image = pygame.Surface(self.dim)
        self.image.fill(self.back_c)
        self.rect = self.image.get_rect()


class Button(UI):
    """
    Checks if a mouse is clicks the button
    Has params that tell what to check for

    """

    @property
    def allowed_group_movement(self) -> int:
        """Helper function that returns a list of how much the groups a button is a part of can move."""
        top = self.groups()[0].sprites()[0].rect.top
        screen_height = self.surface.get_height()
        return self.group_height + top - screen_height

    @property
    def group_height(self) -> int:
        """Helper function that returns a list of the heights of the groups a button is a part of."""
        return self.groups()[0].sprites()[-1].rect.bottom - self.groups()[0].sprites()[0].rect.top + 10


class ScrollBar(UI):
    def __init__(self,
                 surface: pygame.Surface,
                 start_p: tuple | list,
                 dim: tuple | list,
                 scroll_bar_dim: tuple | list,
                 controlled_g: Button,
                 to_return: Any = None,
                 text: Any = '', *,
                 scroll_bar_color: str | tuple | list = 'black',
                 back_c: str | tuple | list = 'gray',
                 text_c: str | tuple | list = 'white',
                 text_s: int = 30,
                 scroll_bar_pos: tuple | list = (),
                 text_pos_change: tuple | list = (),
                 alignment: AlignmentTypes = AlignmentTypes.tl,
                 orientation: int = 0,
                 alpha: int = 255) -> None:
        super(ScrollBar, self).__init__(surface, start_p, dim, to_return, text, back_c=back_c, text_c=text_c,
                                        text_s=text_s, text_pos_change=text_pos_change, alignment=alignment,
                                        alpha=alpha)
        # basic setup
        self.sb_dim = scroll_bar_dim
        self.controlled_b = controlled_g
        self.sb_pos = scroll_bar_pos
        self.sb_color = scroll_bar_color
        self.sb_image = pygame.Surface(self.sb_dim)
        self.sb_rect = self.sb_image.get_rect()
        self.sb_image.fill(scroll_bar_color)
        self.x_or_y = orientation

    @property
    def pos_ratio(self) -> float:
        return self.controlled_b.allowed_group_movement / (self.sb_dim[self.x_or_y] - self.dim[self.x_or_y])

    def match_g_pos(self):
        self.controlled_b.set_pos(self.rect.center[self.x_or_y] * self.pos_ratio)


class BasicBlock(pygame.sprite.Sprite):
    def __init__(self,
                 pos: list[int, int] | tuple[int, int],
                 block_id: int,
                 scaler: int,
                 rotation: int | None = 0) -> None:
        """
        Creating a basic tetris

        :param pos: Where the top left of the tetris block is
        :param block_id: Which block this is, needs to be a whole num
        :param scaler: How much the block's dim are multiplied by
        :param rotation: Which rotation of the block it is, needs to be a whole num
        """
        super().__init__()

        # error checking
        assert 8 > block_id > 0, "Invalid block id, block id ranges from 0 to 7."
        assert rotation is None or 4 >= rotation >= 0, "Invalid rotation, rotation needs to be a whole num."
        assert scaler > 0, "Invalid size, scaler needs to be a whole num."

        # basic setup
        self.pos = pos
        self.block_id = block_id
        self.rotation = rotation
        self.scaler = scaler
        self.rect = None
        self.mask = None

        # image setup
        self.set_image()

        # pos
        self.set_pos(self.pos)

    def set_image(self, block_id: int = '', rotation: int = '', alpha: int = 255) -> None:
        if str(block_id):
            self.block_id = block_id
        if str(rotation):
            self.rotation = rotation
        if self.rotation is None:
            image_path = f'Assets/Tetris block {self.block_id}.png'
        else:
            image_path = f'Assets/Tetris block {self.block_id} ({self.rotation} turn).png'
        self.image = pygame.transform.scale(pygame.image.load(image_path), [self.get_dim[0] * self.scaler,
                                                                            self.get_dim[1] * self.scaler])
        self.image.set_alpha(alpha)
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.set_pos(self.pos)

    def set_pos(self, pos) -> None:
        self.pos = pos
        self.rect.topleft = pos
        self.mask = pygame.mask.from_surface(self.image)

    @property
    def get_dim(self) -> list[int, int]:
        if self.rotation is None:
            return [1, 1]
        if self.block_id in range(6):
            if self.rotation % 2 == 0:
                return [2, 3]
            return [3, 2]
        if self.block_id == 6:
            if self.rotation == 0:
                return [1, 4]
            return [4, 1]
        return [2, 2]

    @property
    def allowed_rotation(self) -> int:
        if self.block_id in [1, 2, 6]:
            return 2
        if self.block_id == 7:
            return 1
        return 4

    @property
    def relative_pos(self):
        return int(self.pos[0] / self.scaler), int(self.pos[1] / self.scaler)


class Block(BasicBlock):
    def __init__(self,
                 pos: list[int, int] | tuple[int, int],
                 block_id: int,
                 scaler: int,
                 obstacles: pygame.sprite.Group,
                 rotation: int | None = 0) -> None:
        # basic setup
        self.obstacles = obstacles
        super(Block, self).__init__(pos, block_id, scaler, rotation)

    def collision_check(self) -> bool:
        if pygame.sprite.spritecollide(self, self.obstacles, False):
            # noinspection PyTypeChecker
            if pygame.sprite.spritecollide(self, self.obstacles, False, pygame.sprite.collide_mask):
                return True
        return False

    def move(self, direction=(0, 1)) -> bool:
        direction = direction[0] * self.scaler, direction[1] * self.scaler
        self.set_pos([self.pos[0] + direction[0], self.pos[1] + direction[1]])
        self.set_image()
        if self.collision_check():
            self.set_pos([self.pos[0] - direction[0], self.pos[1] - direction[1]])
            self.set_image()
            return False
        return True

    def rotate(self, direction) -> bool:
        """Rotates the block cw if dir is pos, ccw if dir is neg."""
        self.set_image(rotation=(self.rotation + direction) % self.allowed_rotation)
        if self.collision_check():
            self.set_image(rotation=(self.rotation - direction) % self.allowed_rotation)
            return False
        return True

    def hard_drop(self):
        while True:
            if not self.move():
                break
        self.split()

    def split(self) -> list[list[int]]:
        x, y = int(self.pos[0] / self.scaler), int(self.pos[1] / self.scaler)
        conversion: dict[int: list[list[list[int, int]]]] = {
            1: [
                [[x, y + 1], [x + 1, y], [x + 1, y + 1], [x, y + 2]],
                [[x, y], [x + 1, y], [x + 1, y + 1], [x + 2, y + 1]]
            ],
            2: [
                [[x, y], [x, y + 1], [x + 1, y + 1], [x + 1, y + 2]],
                [[x + 1, y], [x, y + 1], [x + 1, y + 1], [x + 2, y]]
            ],
            3: [
                [[x, y], [x + 1, y], [x + 1, y + 1], [x + 1, y + 2]],
                [[x, y + 1], [x + 1, y + 1], [x + 2, y], [x + 2, y + 1]],
                [[x, y], [x, y + 1], [x, y + 2], [x + 1, y + 2]],
                [[x, y], [x, y + 1], [x + 1, y], [x + 2, y]]
            ],
            4: [
                [[x, y], [x + 1, y], [x, y + 1], [x, y + 2]],
                [[x, y], [x + 1, y], [x + 2, y], [x + 2, y + 1]],
                [[x + 1, y], [x + 1, y + 1], [x, y + 2], [x + 1, y + 2]],
                [[x, y], [x, y + 1], [x + 1, y + 1], [x + 2, y + 1]]
            ],
            5: [
                [[x, y], [x + 1, y + 1], [x, y + 1], [x, y + 2]],
                [[x, y], [x + 1, y + 1], [x + 1, y], [x + 2, y]],
                [[x + 1, y], [x, y + 1], [x + 1, y + 1], [x + 1, y + 2]],
                [[x + 1, y], [x + 1, y + 1], [x, y + 1], [x + 2, y + 1]]
            ],
            6: [
                [[x, y], [x, y + 1], [x, y + 2], [x, y + 3]],
                [[x, y], [x + 1, y], [x + 2, y], [x + 3, y]]
            ],
            7: [[[x, y], [x + 1, y], [x, y + 1], [x + 1, y + 1]]]
        }
        to_add = [[cords[0], cords[1]] for cords in conversion[self.block_id][self.rotation]]
        for x, y in to_add:
            block = BasicBlock(
                [x * self.scaler, y * self.scaler], self.block_id, self.scaler, rotation=None
            )
            self.obstacles.add(block)
        self.kill()
        return to_add
