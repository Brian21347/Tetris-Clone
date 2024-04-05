import pygame
from sys import exit
from random import randint
from TetrisClasses import Obj, Block, BasicBlock

# basic pygame setup
pygame.init()
block_size = 40
WIDTH, HEIGHT = 20 * block_size, 20 * block_size
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()

# creating a list that is used to keep track of things on screen
# False if there is not anything there, True is there is something
board: list[list[bool]] = []  # 10 columns and 20 rows
for _ in range(20):  # row
    board.append([])
    for _ in range(10):  # column
        board[-1].append(False)

# Obstacle group setup
obstacles_g = pygame.sprite.Group()
obstacles_l = [
    Obj([5 * block_size, 0], [block_size, HEIGHT], 'light gray'),
    Obj([16 * block_size, 0], [block_size, HEIGHT], 'light gray'),
    Obj([6 * block_size, 20 * block_size], [10 * block_size, block_size], 'light gray')
]
obstacles_g.add(obstacles_l)

# preview block setup
preview_g = pygame.sprite.GroupSingle()
preview_block = None

# moving tetris block setup
available = list(range(1, 8))
tetris_block = Block((10 * block_size, 0), available.pop(randint(0, len(available) - 1)), block_size, obstacles_g)
the_block = pygame.sprite.GroupSingle(tetris_block)
time_to_drop = 2
can_hold = False


def main():
    global can_hold, preview_block, time_to_drop, tetris_block
    pygame.key.set_repeat(250, 100)
    last_time = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_LEFT:
                    tetris_block.move([-1, 0])
                elif event.key == pygame.K_RIGHT:
                    tetris_block.move([1, 0])
                elif event.key == pygame.K_UP:
                    tetris_block.rotate(1)
                elif event.key == pygame.K_z:
                    tetris_block.rotate(-1)
                elif event.key == pygame.K_DOWN:
                    if not tetris_block.move():
                        new_block()
                elif event.key == pygame.K_SPACE:
                    tetris_block.hard_drop()
                    new_block()
                elif event.key == pygame.K_c and can_hold:
                    can_hold = False
                    if not preview_g:
                        tetris_block.remove(the_block)
                        tetris_block.set_pos([block_size, block_size])
                        tetris_block.add(preview_g)
                        preview_block = tetris_block
                        new_block()
                    else:
                        tetris_block.remove(the_block)
                        tetris_block.set_pos([block_size, block_size])
                        tetris_block.add(preview_g)

                        preview_block.set_pos([10*block_size, 0])
                        preview_block.add(the_block)

                        tetris_block_copy = tetris_block
                        tetris_block = preview_block
                        preview_block = tetris_block_copy
        if (pygame.time.get_ticks() - last_time) / 1000 > time_to_drop:  # moves at a decreasing time step
            if not tetris_block.move():  # seeing if the block moves
                new_block()  # doesn't move
            last_time = pygame.time.get_ticks()
            if time_to_drop > .2:
                time_to_drop -= .05
        screen.fill('light gray')
        the_block.draw(screen)
        obstacles_g.draw(screen)
        preview_g.draw(screen)
        grid()
        grid(block_size, 4 * block_size, block_size, block_size, 4 * block_size, block_size)
        pygame.display.update()
        clock.tick(30)


def new_block(preview=False):
    global tetris_block, the_block, available, can_hold
    if preview:
        for pos in tetris_block.split():
            board[pos[1]][pos[0] - 6] = True
        can_hold = True
    line_clear()
    if len(available) == 0:
        available = list(range(1, 8))
    tetris_block = Block((10 * block_size, 0), available.pop(randint(0, len(available) - 1)), block_size, obstacles_g)
    the_block.add(tetris_block)


def switch_preview_tetris_blocks():
    global preview_block, tetris_block
    copy_of_preview = preview_block
    preview_block = Block(
        [block_size, block_size], tetris_block.block_id, block_size, obstacles_g, tetris_block.rotation
    )
    if copy_of_preview:
        tetris_block = Block(
            (10 * block_size, 0), copy_of_preview.block_id, block_size, obstacles_g, preview_block.rotation
        )
        the_block.add(tetris_block)
    else:
        new_block()


def board_updater():
    global board
    board = []
    for _ in range(20):
        board.append([])
        for _ in range(10):
            board[-1].append(False)

    for index, sprite in enumerate(obstacles_g):
        if index < 3:
            continue
        pos = int(sprite.rect.top / block_size), int(sprite.rect.left / block_size)
        board[pos[0]][pos[1] - 6] = True


def line_clear():
    for i, row in enumerate(board):
        if [item for item in row if item is False]:
            # if there is one or more None types in a row it shouldn't be cleared
            continue

        for index, sprite in enumerate(obstacles_g):
            if index < 3:
                continue
            top = int(sprite.rect.top / block_size)
            if top == i:
                sprite.kill()
            elif top < i:
                sprite.rect.top += block_size
    board_updater()


def grid(xmin=6 * block_size, width=10 * block_size, xinterval=block_size, ymin=0, height=HEIGHT,
         yinterval=block_size):  # draws a grid
    xmax, ymax = xmin + width, ymin + height
    for x in range(xmin, xmax, xinterval):
        pygame.draw.line(screen, 'black', [x, ymin], [x, ymax])
    for y in range(ymin, ymax, yinterval):
        pygame.draw.line(screen, 'black', [xmin, y], [xmax, y])
    pygame.draw.line(screen, 'black', [xmax, ymin], [xmax, ymax])
    pygame.draw.line(screen, 'black', [xmin, ymax], [xmax, ymax])


if __name__ == '__main__':
    main()
