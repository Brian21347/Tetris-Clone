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

SWITCH_BUTTON_START: Coordinate = [BLOCK_SIZE / 2, SCREEN_SIZE[1] - 2 * BLOCK_SIZE]
SWITCH_BUTTON_SIZE: Coordinate = [BLOCK_SIZE * 4, 1.5 * BLOCK_SIZE]
SWITCH_BUTTON_THEMES: list[str] = ["Piano", "Music Box", "Strings"]
SWITCH_BUTTON_TEXT_COLOR: str = "black"
SWITCH_BUTTON_BACKGROUND_COLOR: str = "light gray"
SWITCH_BUTTON_BORDER_COLOR: str = "dark gray"
SWITCH_BUTTON_BORDER_SIZE: str = 3
SWITCH_BUTTON_BORDER_RADIUS: int = 10
SWITCH_BUTTON_FILL_CENTER: bool = True

VOLUME_BUTTON_START: Coordinate = [BLOCK_SIZE / 2, SCREEN_SIZE[1] - 5 * BLOCK_SIZE]
VOLUME_BUTTON_SIZE: Coordinate = [BLOCK_SIZE * 1.5, 1.5 * BLOCK_SIZE]
VOLUME_BUTTON_EXPAND_RECT: int = [2 * BLOCK_SIZE, 2]
VOLUME_BUTTON_CIRCLE_RADIUS: int = 5
VOLUME_BUTTON_STARTING_VOLUME: float = 1
VOLUME_BUTTON_FULL: str = join_path("Assets", "images", "Speaker 1.png")
VOLUME_BUTTON_SEMI: str = join_path("Assets", "images", "Speaker 2.png")
VOLUME_BUTTON_MUTED: str = join_path("Assets", "images", "Speaker 3.png")
VOLUME_BUTTON_SPEAKER_SIZE: Coordinate = [BLOCK_SIZE, BLOCK_SIZE]
VOLUME_BUTTON_BACKGROUND_COLOR: str = "light gray"
VOLUME_BUTTON_BORDER_COLOR: str = "dark gray"
VOLUME_BUTTON_BORDER_SIZE: int = 3
VOLUME_BUTTON_BORDER_RADIUS: int = 10
VOLUME_BUTTON_BAR_OFFSET: int = 5
VOLUME_CLAMP: float = 0.017
VOLUME_BUTTON_HOVER_DELAY: int = 300
VOLUME_BUTTON_DELAY: int = 150
VOLUME_BUTTON_FILL_CENTER: bool = True

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

class GameExit(Exception):
    pass
