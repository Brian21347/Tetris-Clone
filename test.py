import pygame
from sys import exit
from random import randint
from TetrisClasses import Obj, Block


# basic pygame setup
pygame.init()
block_size = 30
WIDTH, HEIGHT = 20 * block_size, 20 * block_size
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()

# creating a list that is used to keep track of things on screen
# False if there is not anything there, True is there is something
board = []  # 10 columns and 20 rows
for _ in range(20):  # row
    board.append([])
    for _ in range(10):  # column
        board[-1].append(False)

# Obstacle group setup
obstacles_g = pygame.sprite.Group()
obstacles_l = [
    Obj([5*block_size, 0], [block_size, HEIGHT], 'pink'),
    Obj([16*block_size, 0], [block_size, HEIGHT], 'pink'),
    Obj([6*block_size, 20*block_size], [10*block_size, block_size], 'pink')
]
obstacles_g.add(obstacles_l)

# preview block setup
preview_g = pygame.sprite.GroupSingle()

# moving tetris block setup
available = list(range(1, 8))
tetris_block = Block((10 * block_size, 0), available.pop(randint(0, len(available)-1)), block_size, obstacles_g)
the_block = pygame.sprite.GroupSingle(tetris_block)
time_to_drop = 2


def main():
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
                # movement controls
                if event.key == pygame.K_LEFT:  # left
                    tetris_block.move([-1, 0])
                elif event.key == pygame.K_RIGHT:  # right
                    tetris_block.move([1, 0])
                elif event.key == pygame.K_UP:  # rotate
                    tetris_block.rotate(1)
                elif event.key == pygame.K_z:
                    tetris_block.rotate(-1)
                elif event.key == pygame.K_DOWN:
                    tetris_block.move()
                elif event.key == pygame.K_SPACE:
                    tetris_block.hard_drop()
                    new_block()
        if (pygame.time.get_ticks() - last_time)/1000 > time_to_drop:  # moves at a decreasing timestep
            if not tetris_block.move():  # seeing if the block moves
                new_block()  # doesn't move
            last_time = pygame.time.get_ticks()
        screen.fill('light gray')
        the_block.draw(screen)
        obstacles_g.draw(screen)
        preview_g.draw(screen)
        grid()
        grid(block_size, 4*block_size, block_size, block_size, 4*block_size, block_size)
        pygame.display.update()
        clock.tick(30)


def new_block():
    global time_to_drop, tetris_block, the_block, available
    for pos in tetris_block.split():
        board[pos[1]][pos[0]-6] = True
    line_clear()
    if len(available) == 0:
        available = list(range(1, 8))
    tetris_block = Block((10 * block_size, 0), available.pop(randint(0, len(available)-1)), block_size, obstacles_g)
    the_block = pygame.sprite.GroupSingle(tetris_block)
    if time_to_drop > .2:
        time_to_drop -= .05


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
        pos = int(sprite.rect.top/block_size), int(sprite.rect.left/block_size)
        board[pos[0]][pos[1]-6] = True


def line_clear():
    for i, row in enumerate(board):
        print([item for item in row if item is False])
        if [item for item in row if item is False]:
            # if there is one or more None types in a row it shouldn't be cleared
            continue

        for index, sprite in enumerate(obstacles_g):
            if index < 3:
                continue
            top = int(sprite.rect.top/block_size)
            if top == i:
                sprite.kill()
            elif top < i:
                sprite.rect.top += block_size
    board_updater()


def grid(xmin=6 * block_size, width=10 * block_size, xinterval=block_size, ymin=0, height=HEIGHT,
         yinterval=block_size):  # draws a grid
    xmax, ymax = xmin+width, ymin+height
    for x in range(xmin, xmax, xinterval):
        pygame.draw.line(screen, 'black', [x, ymin], [x, ymax])
    for y in range(ymin, ymax, yinterval):
        pygame.draw.line(screen, 'black', [xmin, y], [xmax, y])
    pygame.draw.line(screen, 'black', [xmax, ymin], [xmax, ymax])
    pygame.draw.line(screen, 'black', [xmin, ymax], [xmax, ymax])


if __name__ == '__main__':
    main()
