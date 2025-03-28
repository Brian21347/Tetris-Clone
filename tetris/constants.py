from os.path import join as join_path

LOGO_PATH: str = join_path("Assets", "images", "Logo.png")
BG_COLOR: str = "light gray"
FRAME_RATE: int = 100
BLOCK_SIZE: int = 25
Pii = tuple[int, int] | list[int, int]
SCREEN_WIDTH: int = BLOCK_SIZE * 20
SCREEN_HEIGHT: int = BLOCK_SIZE * 26
SCREEN_SIZE: Pii = (SCREEN_WIDTH, SCREEN_HEIGHT)
FONT: str = "Roboto"
TEXT_SIZE: int = 30

# intro config
TITLE_CENTER_POSITION: Pii = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 2 * BLOCK_SIZE)
TITLE: str = "A Tetris Clone"
TITLE_TEXT_COLOR: str = "black"
TITLE_SIZE: int = 60

START_PROMPT_CENTER_POSITION: Pii = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 3 * BLOCK_SIZE)
START_PROMPT_TEXT: str = "Click anywhere to start!"
START_PROMPT_TEXT_COLOR: str = "black"

# outro config
COVER_SCREEN_TRANSPARENCY: int = 125  # this is out of 255
COVER_SCREEN_COLOR: str = "gray"

GAME_OVER_PROMPT_TEXT: str = "Game over"
GAME_OVER_SIZE: int = 60
GAME_OVER_TEXT_COLOR: str = "black"
GAME_OVER_CENTER_POSITION: Pii = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - BLOCK_SIZE)

RESTART_PROMPT_TEXT: str = "Click anywhere to play again!"
RESTART_PROMPT_TEXT_COLOR: str = "black"
RESTART_PROMPT_CENTER_POSITION: Pii = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + BLOCK_SIZE)

# game config
GRID_COLOR: str = "black"
DELAY: int = 200
INTERVAL: int = 100

BLOCK_OUTLINE_SIZE: int = 5

IMAGE_ASSET_PATH: str = join_path("Assets", "images", "Tetris Block %s.png")
THEME_ASSET_PATH: str = join_path("Assets", "themes", "%s.mp3")

HOLD_GRID_START: Pii = (BLOCK_SIZE // 2, 1.5 * BLOCK_SIZE)
HOLD_GRID_SIZE: Pii = (4 * BLOCK_SIZE, 2 * BLOCK_SIZE)

FIELD_GRID_START: Pii = (5 * BLOCK_SIZE, 1.5 * BLOCK_SIZE)
FIELD_GRID_SIZE: Pii = (10 * BLOCK_SIZE, 24 * BLOCK_SIZE)

UPCOMING_GRID_START: Pii = (15.5 * BLOCK_SIZE, 1.5 * BLOCK_SIZE)
UPCOMING_GRID_HIGHT: int = BLOCK_SIZE * 2
UPCOMING_GAP_SIZE: int = int(0.5 * BLOCK_SIZE)
UPCOMING_NUMBER: int = 5

SWITCH_BUTTON_START: Pii = [BLOCK_SIZE / 2, SCREEN_HEIGHT - 2 * BLOCK_SIZE]
SWITCH_BUTTON_SIZE: Pii = [BLOCK_SIZE * 4, 1.5 * BLOCK_SIZE]
SWITCH_BUTTON_THEMES: list[str] = ["Piano", "Music Box", "Strings"]
SWITCH_BUTTON_TEXT_COLOR: str = "black"
SWITCH_BUTTON_BACKGROUND_COLOR: str = "light gray"
SWITCH_BUTTON_BORDER_COLOR: str = "dark gray"
SWITCH_BUTTON_BORDER_SIZE: str = 3
SWITCH_BUTTON_BORDER_RADIUS: int = 10
SWITCH_BUTTON_FILL_CENTER: bool = True

VOLUME_BUTTON_START: Pii = [BLOCK_SIZE / 2, SCREEN_HEIGHT - 5 * BLOCK_SIZE]
VOLUME_BUTTON_SIZE: Pii = [BLOCK_SIZE * 1.5, 1.5 * BLOCK_SIZE]
VOLUME_BUTTON_EXPAND_RECT: int = [2 * BLOCK_SIZE, 2]
VOLUME_BUTTON_CIRCLE_RADIUS: int = 5
VOLUME_BUTTON_STARTING_VOLUME: float = 1
VOLUME_BUTTON_FULL: str = join_path("Assets", "images", "Speaker 1.png")
VOLUME_BUTTON_SEMI: str = join_path("Assets", "images", "Speaker 2.png")
VOLUME_BUTTON_MUTED: str = join_path("Assets", "images", "Speaker 3.png")
VOLUME_BUTTON_SPEAKER_SIZE: Pii = [BLOCK_SIZE, BLOCK_SIZE]
VOLUME_BUTTON_BACKGROUND_COLOR: str = "light gray"
VOLUME_BUTTON_BORDER_COLOR: str = "dark gray"
VOLUME_BUTTON_BORDER_SIZE: int = 3
VOLUME_BUTTON_BORDER_RADIUS: int = 10
VOLUME_BUTTON_BAR_OFFSET: int = 5
VOLUME_CLAMP: float = 0.017
VOLUME_BUTTON_HOVER_DELAY: int = 300
VOLUME_BUTTON_DELAY: int = 150
VOLUME_BUTTON_FILL_CENTER: bool = True

TEXT_BUTTON_STARTS: list[Pii] = [
    [BLOCK_SIZE, 0.5 * BLOCK_SIZE], 
    [16 * BLOCK_SIZE, 0.5 * BLOCK_SIZE], 
    [BLOCK_SIZE, 7.5 * BLOCK_SIZE], 
    [BLOCK_SIZE, 9.5 * BLOCK_SIZE], 
    [BLOCK_SIZE, 11.5 * BLOCK_SIZE]
]
TEXT_BUTTON_SIZE: list[Pii]  = [3 * BLOCK_SIZE, BLOCK_SIZE]
TEXT_BUTTON_TEXTS: list[str] = ["Held", "Next", "Score", "Level", "Lines"]
TEXT_BUTTON_TEXT_COLOR: str = "black"

SCORE_COLOR: int = "dark gray"
SCORE_STARTS: list[Pii] = [[BLOCK_SIZE, 8.5 * BLOCK_SIZE], [BLOCK_SIZE, 10.5 * BLOCK_SIZE], [BLOCK_SIZE, 12.5 * BLOCK_SIZE]]
SCORE_SIZE: Pii = (3 * BLOCK_SIZE, BLOCK_SIZE)

BLOCKS_TO_CLEAR_LINE: int = FIELD_GRID_SIZE[0] // BLOCK_SIZE

LINE_CLEAR_SPEED_UP: float = 0.3
INITIAL_MOVEMENT_TIME: int = 1000

POINTS = {
    0: 0,
    1: 40,
    2: 100,
    3: 300,
    4: 1200,
    5: 6000,  # added to support user created blocks later
}


class GameExit(Exception):
    pass
