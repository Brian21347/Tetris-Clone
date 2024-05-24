from os.path import join as join_path
BG_COLOR: str = "light gray"
GRID_COLOR: str = "black"
FRAME_RATE: int = 100
BLOCK_SIZE: int = 30
Coordinate = tuple[int, int]
SCREEN_SIZE: Coordinate = (BLOCK_SIZE * 20, BLOCK_SIZE * 26)

DELAY: int = 200
INTERVAL: int = 100

BLOCK_OUTLINE_SIZE: int = 5

IMAGE_ASSET_PATH: str = join_path("Assets", "images", "Tetris Block %s.png")
THEME_ASSET_PATH: str = join_path("Assets", "themes", "%s.mp3")

HOLD_GRID_START: Coordinate = (BLOCK_SIZE // 2, BLOCK_SIZE // 2 + BLOCK_SIZE)
HOLD_GRID_SIZE: Coordinate = (4 * BLOCK_SIZE, 4 * BLOCK_SIZE)

FIELD_GRID_START: Coordinate = (5 * BLOCK_SIZE, BLOCK_SIZE // 2 + BLOCK_SIZE)
FIELD_GRID_SIZE: Coordinate = (10 * BLOCK_SIZE, 24 * BLOCK_SIZE)

UPCOMING_GRID_START: Coordinate = (15 * BLOCK_SIZE + BLOCK_SIZE // 2, BLOCK_SIZE // 2 + BLOCK_SIZE)
UPCOMING_GRID_HIGHT: int = BLOCK_SIZE * 2
UPCOMING_GAP_SIZE: int = BLOCK_SIZE 
UPCOMING_NUMBER: int = 5

BLOCKS_TO_CLEAR_LINE: int = FIELD_GRID_SIZE[0] // BLOCK_SIZE

LINE_CLEAR_SPEED_UP: float = 0.3
INITIAL_MOVEMENT_TIME: int = 2000

POINTS = {
    0: 0,
    1: 40,
    2: 100,
    3: 300,
    4: 1200,
}

SCORE_COLOR: int = "gray"
SCORE_POSITION: Coordinate = (FIELD_GRID_START[0] + FIELD_GRID_SIZE[0] // 2, BLOCK_SIZE * .25)
