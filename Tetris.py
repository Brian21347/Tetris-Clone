import sys
from random import randint
import pygame

'''
Don't have the following features yet:
   pausing
   showing upcoming blocks
   mouse controls
   -preview-
'''
# basic set up
pygame.init()
b_size = 50
height = 20 * b_size
width = 20 * b_size
screen = pygame.display.set_mode((width, height))
screen.fill('white')
pygame.display.update()
clock = pygame.time.Clock()


def i_size_change(b, t):
    if b != 5 and b != 7:
        if t % 2 == 0:
            image_size = 2 * b_size, 3 * b_size
        else:
            image_size = 3 * b_size, 2 * b_size
    elif b == 5:
        if t == 0:
            image_size = 1 * b_size, 4 * b_size
        else:
            image_size = 4 * b_size, 1 * b_size
    else:
        image_size = 2 * b_size, 2 * b_size
    return image_size


class TetrisBlock(pygame.sprite.Sprite):
    def __init__(self, which_block, pos):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(f'Assets/Tetris block {which_block} (0 turn).png'),
                                            i_size_change(which_block, 0))  # load image
        self.image.set_colorkey('white')  # tells pygame to make the color 'white' transparent
        self.rect = self.image.get_rect()  # set up rect value for the sprite
        self.rect.topleft = pos  # tells pygame where the sprite is
        self.mask = pygame.mask.from_surface(self.image)  # creates a mask for the sprite
        self.block = which_block  # allows me to access the variable which_block later
        self.turn = 0

    def update(self, direction=0, turn='', hold=False):
        global turn_g
        to_be = None  # if not turn command and not colliding with anything, to_be will not be used
        x, y = self.rect.topleft
        if turn:
            if turn == 'l':  # turn
                try:
                    self.image = pygame.transform.scale(
                        pygame.image.load(f'Assets/Tetris block {self.block} ({self.turn + 1} turn).png'),
                        i_size_change(self.block, self.turn + 1))
                    to_be = self.turn + 1
                except FileNotFoundError:
                    self.image = pygame.transform.scale(pygame.image.load(f'Assets/Tetris block {self.block} (0 turn).png'),
                                                        i_size_change(self.block, 0))
                    to_be = 0
                    # if there is no file then it must be turning from the highest value to the lowest
            else:
                try:
                    self.image = pygame.transform.scale(
                        pygame.image.load(f'Assets/Tetris block {self.block} ({self.turn - 1} turn).png'),
                        i_size_change(self.block, self.turn - 1))
                    to_be = self.turn - 1
                except FileNotFoundError:
                    if self.block in [1, 2, 5]:
                        multi = 1
                    elif self.block in [3, 4, 6]:
                        multi = 3
                    else:
                        multi = 0
                    self.image = pygame.transform.scale(
                        pygame.image.load(f'Assets/Tetris block {self.block} ({multi} turn).png'),
                        i_size_change(self.block, multi))
                    to_be = multi
                    # if there is no file then it must be turning from the lowest value to the highest
            self.image.set_colorkey('white')
        elif hold:
            self.rect.topleft = b_size, b_size
            if len(the_held) == 0:
                self.remove(the_block)
                new_block(0, 0, can_clear=False)
            else:
                the_held.sprite.rect.topleft = 10 * b_size, 0
                the_held.sprite.add(the_block)
            self.add(the_held)
            return
        elif direction == 2:  # right
            self.rect.topleft = x + b_size, y
        elif direction == 1:  # left
            self.rect.topleft = x - b_size, y
        elif direction == -1:  # soft drop
            self.rect.topleft = x, y + b_size
        elif direction == -2:  # hard drop
            self.hard_drop()
            # return self.block, self.turn
        self.mask = pygame.mask.from_surface(self.image)
        self.collision_check(direction, turn, x, y, to_be)  # checks if there is a collision if the action is done
        turn_g = self.turn

    def collision_check(self, direction, turn, x, y, to_be):
        if pygame.sprite.spritecollide(the_block.sprite, all_stopped, False, pygame.sprite.collide_mask) or \
                pygame.sprite.spritecollide(the_block.sprite, obstacles, False, pygame.sprite.collide_mask):
            if turn:
                self.image = pygame.transform.scale(
                    pygame.image.load(f'Assets/Tetris block {self.block} ({self.turn} turn).png'),
                    i_size_change(self.block, self.turn))
                self.image.set_colorkey('white')
            else:
                self.rect.topleft = x, y  # return the block to its previous position
                if direction == -1:
                    self.remove(the_block)  # hit bottem or another stopped block, so stop the block
                    self.splitting()
                    return
            self.mask = pygame.mask.from_surface(self.image)
        elif turn:
            self.turn = to_be

    def splitting(self):  # making a sprite into multiple single block sized sprite that can be removed
        x, y = self.rect.topleft
        b = self.block
        t = self.turn
        L = [[[[x, y + b_size], [x + b_size, y], [x + b_size, y + b_size], [x, y + 2 * b_size]],
              [[x, y], [x + b_size, y], [x + b_size, y + b_size], [x + 2 * b_size, y + b_size]]],
             [[[x, y], [x, y + b_size], [x + b_size, y + b_size], [x + b_size, y + 2 * b_size]],
              [[x + b_size, y], [x, y + b_size], [x + b_size, y + b_size], [x + 2 * b_size, y]]],
             [[[x, y], [x + b_size, y], [x + b_size, y + b_size], [x + b_size, y + 2 * b_size]],
              [[x, y + b_size], [x + b_size, y + b_size], [x + 2 * b_size, y], [x + 2 * b_size, y + b_size]],
              [[x, y], [x, y + b_size], [x, y + 2 * b_size], [x + b_size, y + 2 * b_size]],
              [[x, y], [x, y + b_size], [x + b_size, y], [x + 2 * b_size, y]]],
             [[[x, y], [x + b_size, y], [x, y + b_size], [x, y + 2 * b_size]],
              [[x, y], [x + b_size, y], [x + 2 * b_size, y], [x + 2 * b_size, y + b_size]],
              [[x + b_size, y], [x + b_size, y + b_size], [x, y + 2 * b_size], [x + b_size, y + 2 * b_size]],
              [[x, y], [x, y + b_size], [x + b_size, y + b_size], [x + 2 * b_size, y + b_size]]],
             [[[x, y], [x, y + b_size], [x, y + 2 * b_size], [x, y + 3 * b_size]],
              [[x, y], [x + b_size, y], [x + 2 * b_size, y], [x + 3 * b_size, y]]],
             [[[x, y], [x + b_size, y + b_size], [x, y + b_size], [x, y + 2 * b_size]],
              [[x, y], [x + b_size, y + b_size], [x + b_size, y], [x + 2 * b_size, y]],
              [[x + b_size, y], [x, y + b_size], [x + b_size, y + b_size], [x + b_size, y + 2 * b_size]],
              [[x + b_size, y], [x + b_size, y + b_size], [x, y + b_size], [x + 2 * b_size, y + b_size]]],
             [[[x, y], [x + b_size, y], [x, y + b_size], [x + b_size, y + b_size]]]]
        for _ in L[b - 1][t]:
            obstacle = Obstacle(0, 0, _, image_path=f'Assets/Tetris block {b}.png')
            all_stopped.add(obstacle)
            stopped_l[int(_[1] / b_size)].add(obstacle)

    def hard_drop(self):
        while not (pygame.sprite.spritecollide(the_block.sprite, all_stopped, False, pygame.sprite.collide_mask) or
                   pygame.sprite.spritecollide(the_block.sprite, obstacles, False, pygame.sprite.collide_mask)):
            x, y = self.rect.topleft
            self.rect.topleft = x, y + b_size
            self.mask = pygame.mask.from_surface(self.image)
        x, y = self.rect.topleft
        self.rect.topleft = x, y - b_size
        self.remove(the_block)
        self.splitting()


class PreviewBlock(pygame.sprite.Sprite):
    def __init__(self, which_block):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(f'Assets/Tetris block {which_block} (0 turn).png'),
                                            i_size_change(which_block, 0))  # load image
        self.image.set_colorkey('white')  # tells pygame to make the color 'white' transparent
        self.rect = self.image.get_rect()  # set up rect value for the sprite
        self.rect.topleft = (10*b_size, 0)
        self.mask = pygame.mask.from_surface(self.image)  # creates a mask for the sprite

    def update(self, b, t):
        self.image = pygame.transform.scale(pygame.image.load(f'Assets/Tetris block {b} ({t} turn).png'),
                                            i_size_change(b, 0))
        while not (pygame.sprite.spritecollide(preview.sprite, all_stopped, False, pygame.sprite.collide_mask) or
                   pygame.sprite.spritecollide(preview.sprite, obstacles, False, pygame.sprite.collide_mask)):
            x, y = self.rect.topleft
            self.rect.topleft = x, y + b_size
            self.mask = pygame.mask.from_surface(self.image)
        x, y = self.rect.topleft
        self.rect.topleft = x, y - b_size


class Obstacle(pygame.sprite.Sprite):  # the boundaries to where the block cannot move to
    def __init__(self, width_o, height_o, pos, image_path='', color='white'):  # color is red for testing
        super().__init__()
        if image_path:
            self.image = pygame.transform.scale(pygame.image.load(image_path), (b_size, b_size))
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface((width_o, height_o))
            self.image.fill(color)
            self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        x, y = self.rect.topleft
        self.rect.topleft = x, y + b_size


dic = {(5 * b_size, 0): (b_size, 20 * b_size), (16 * b_size, 0): (b_size, 20 * b_size),  # the boundaries
       (6 * b_size, 20 * b_size): (10 * b_size, b_size)}
blocks = [1, 2, 3, 4, 5, 6, 7]  # to control randomness, there is a cycle
block = blocks.pop(randint(0, len(blocks) - 1))  # gets a random block and prevents it from being drawn again this cycle
the_block = pygame.sprite.GroupSingle(TetrisBlock(block, (10 * b_size, 0)))
turn_g = 0
the_held = pygame.sprite.GroupSingle()
all_stopped = pygame.sprite.Group()
preview = pygame.sprite.GroupSingle(PreviewBlock(block))
stopped_l = []
for _ in range(20):
    stopped_l.append(pygame.sprite.Group())
obstacles = pygame.sprite.Group()
for _1, _2 in dic.items():
    obstacles.add(Obstacle(_2[0], _2[1], _1, color='white'))
line_group = pygame.sprite.Group()
for _ in range(20):
    line_group.add(Obstacle(10 * b_size, b_size, (6 * b_size, _ * b_size), color='white'))


def main():
    global the_block, block, blocks, turn_g
    start = pygame.time.get_ticks()  # start time
    speed_d = 3000  # about 5 secs
    # check_entry(int, 'How fast in milliseconds would you like your controls to be repeated at?\n>>>')
    pygame.key.set_repeat(250, 100)
    # repeats the key that is pressed
    points = 0
    level = 0
    holdable = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # exit
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # exit
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:  # r turn
                    the_block.update(turn='l')
                elif event.key == pygame.K_z:  # l turn
                    the_block.update(turn='r')
                elif event.key == pygame.K_DOWN:  # soft drop
                    the_block.update(direction=-1)
                    level, speed_d, points, holdable = speed_increase(level, points, speed_d, holdable)
                elif event.key == pygame.K_SPACE:  # hard drop
                    the_block.update(direction=-2)
                    level, speed_d, points, holdable = speed_increase(level, points, speed_d, holdable)
                elif event.key == pygame.K_LEFT:  # left
                    the_block.update(direction=1)
                elif event.key == pygame.K_RIGHT:  # right
                    the_block.update(direction=2)
                elif event.key == pygame.K_c and holdable:
                    the_block.update(hold=True)
                    holdable = False
                preview.update(b=block, t=turn_g)
        if (pygame.time.get_ticks() - start) > speed_d:
            the_block.update(direction=-1)  # the moving clock
            start = pygame.time.get_ticks()
            level, speed_d, points, holdable = speed_increase(level, points, speed_d, holdable)
        screen.fill('white')  # rest screen
        the_block.draw(screen)  # draws the block that the player controls
        the_held.draw(screen)
        all_stopped.draw(screen)  # draws the blocks that are stopped
        obstacles.draw(screen)
        preview.draw(screen)
        make_text((17.1 * b_size, .25 * b_size), f'Points: {points}')
        make_text((17.1 * b_size, 1.25 * b_size), f'Level: {level}')
        grid()  # draws the grid on top of the blocks
        grid(b_size, 5 * b_size, b_size, b_size, 5 * b_size, b_size)
        pygame.display.flip()  # updates the screen
        clock.tick(60)  # controls frame rate


def speed_increase(level, points, speed_d, holdable):
    points, Bool = new_block(points, level)
    if Bool and speed_d > 250:  # only when going down can the block change
        level += 1  # faster
    speed_d = 3000 - 25 * level
    if Bool:
        holdable = True
    return level, speed_d, points, holdable


def new_block(points, level, can_clear=True):
    global blocks, block, the_block
    if len(the_block) == 0:
        if not blocks:  # if blocks run out (one cycle finished) replenish the blocks
            blocks = [1, 2, 3, 4, 5, 6, 7]
        block = blocks.pop(randint(0, len(blocks) - 1))
        the_block = pygame.sprite.GroupSingle(TetrisBlock(block, (10 * b_size, 0)))
        if can_clear:
            if pygame.sprite.spritecollide(the_block.sprite, all_stopped, False):
                print(f'You lost\nYou got {points} point(s) over {level} level(s)')
                sys.exit()
            points = line_clear(level, points)
        preview.update(b=block, t=0)
        return points, True
    return points, False


def line_clear(level, points):
    counter2 = 0
    L = []
    for _y in range(20):  # from 0 to 19
        counter = 0
        for _x in range(6, 16):  # from 6 to 15
            if screen.get_at((_x * b_size + 1, _y * b_size + 1)) != (255, 255, 255):  # to check that a line is full
                counter += 1
        if counter == 10:
            L.append(_y)
    for _ in L:
        pygame.sprite.spritecollide(line_group.sprites()[_], all_stopped, True)  # to remove the sprites
        # in the full line
    for _0 in L:
        counter2 += 1
        for i in range(_0 - 1, -1, -1):  # from y to 0
            stopped_l[i].update()  # moves down one block the above for loop has no issues (for line clearing)
            # not syncing error
    if counter2 == 1:
        points += 40 * (int(level / 10) + 1)
    elif counter2 == 2:
        points += 100 * (int(level / 10) + 1)
    elif counter2 == 3:
        points += 300 * (int(level / 10) + 1)
    elif counter2 > 3:
        points += 1200 * (int(level / 10) + 1)
    return points


def make_text(pos, what, size=b_size / 2):
    text = pygame.font.SysFont('arial', int(size)).render(str(what), True, 'black')
    screen.blit(text, text.get_rect(topleft=pos))


def grid(xmin=6 * b_size, xmax=width - 4 * b_size, xinterval=b_size, ymin=0, ymax=height,
         yinterval=b_size):  # draws a grid
    for x in range(xmin, xmax, xinterval):
        for y in range(ymin, ymax, yinterval):
            x2 = x + b_size
            y2 = y + b_size
            pygame.draw.line(screen, 'black', [x, y], [x2, y], 1)
            pygame.draw.line(screen, 'black', [x, y], [x, y2], 1)
    pygame.draw.line(screen, 'black', [xmax, ymin], [xmax, ymax])
    pygame.draw.line(screen, 'black', [xmin, ymax], [xmax, ymax])


def check_entry(target_type, good, bad='Please try again'):
    while True:
        try:
            variable = target_type(input(good))
            break
        except ValueError:
            print(bad)
    return target_type(variable)


if __name__ == "__main__":
    main()
