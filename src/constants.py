from os.path import join as join_path
BG_COLOR: str = "light gray"
GRID_COLOR: str = "black"
FRAME_RATE: int = 100
BLOCK_SIZE: int = 40
Coordinate = tuple[int, int]
ASSET_PATH: str = join_path("Assets", "Tetris Block %s.png")

HOLD_GRID_START: Coordinate = (BLOCK_SIZE / 2, BLOCK_SIZE / 2)
HOLD_GRID_SIZE: Coordinate = (4 * BLOCK_SIZE, 4 * BLOCK_SIZE)

FIELD_GRID_START: Coordinate = (5 * BLOCK_SIZE, BLOCK_SIZE / 2)
FIELD_GRID_SIZE: Coordinate = (10 * BLOCK_SIZE, 24 * BLOCK_SIZE)

BLOCKS_TO_CLEAR_LINE: int = FIELD_GRID_SIZE[0] // BLOCK_SIZE

LINE_CLEAR_SPEED_UP: float = 0.3
INITIAL_MOVEMENT_TIME: int = 2000
