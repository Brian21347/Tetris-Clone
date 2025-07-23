import pygame
from constants import *


FULL_SPEAKER = pygame.transform.scale(
    pygame.image.load(VOLUME_BUTTON_FULL), VOLUME_BUTTON_SPEAKER_SIZE
)
SEMI_SPEAKER = pygame.transform.scale(
    pygame.image.load(VOLUME_BUTTON_SEMI), VOLUME_BUTTON_SPEAKER_SIZE
)
NONE_SPEAKER = pygame.transform.scale(
    pygame.image.load(VOLUME_BUTTON_NONE), VOLUME_BUTTON_SPEAKER_SIZE
)
MUTED_SPEAKER = pygame.transform.scale(
    pygame.image.load(VOLUME_BUTTON_MUTED), VOLUME_BUTTON_SPEAKER_SIZE
)


class VolumeButton:
    def __init__(
        self,
        position: Pii,
        size: Pii,
        expand_rect: Pii,
        starting_volume: float,
        background_color: str,
        border_color: str,
        border_size: int,
        border_radius: int,
        fill_center: bool,
    ) -> None:
        self.screen = pygame.display.get_surface()
        self.position = position
        self.size = size
        self.expand_rect = expand_rect
        self.volume = starting_volume
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_size
        self.border_radius = border_radius
        self.fill_center = fill_center

        self.muted = False
        self.rect = pygame.rect.Rect(self.position, self.size)

        self.__start_hover = None
        self.__leave = 0
        self.__max_expansion = 0

    def update(self, event: pygame.event.EventType):
        mouse_x, _ = pygame.mouse.get_pos()
        if self.hovering_over_bar() or self.hovering_over_box():
            if self.__start_hover is None:
                self.__start_hover = pygame.time.get_ticks()
            self.__leave = None
        else:
            if self.__leave is None:
                self.__leave = pygame.time.get_ticks()
            self.__start_hover = None

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and self.hovering_over_box()
            and pygame.mouse.get_pressed()[0]
        ):
            self.muted = not self.muted
        if pygame.mouse.get_pressed()[0]:
            if self.hovering_over_bar():
                self.volume = (
                    max(mouse_x - self.position[0] - self.size[0] - VOLUME_BUTTON_BAR_OFFSET, VOLUME_CLAMP)
                    / self.expand_rect[0]
                )
                if self.volume <= VOLUME_CLAMP:
                    self.muted = True
                else:
                    self.muted = False

    @property
    def speaker_icon(self):
        if self.muted:
            return MUTED_SPEAKER
        if self.volume < VOLUME_CLAMP:
            return NONE_SPEAKER
        if self.volume < 0.5:
            return SEMI_SPEAKER
        return FULL_SPEAKER

    def get_volume(self):
        return 0 if self.muted or self.volume < VOLUME_CLAMP else self.volume

    def hovering_over_box(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def hovering_over_bar(self):
        end_x_position = (
            self.position[0]
            + self.size[0]
            + (
                self.expand_rect[0] + VOLUME_BUTTON_CIRCLE_RADIUS
                if self.volume_fill_percent != 0
                else 0
            )
        )
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (
            self.position[0] + self.size[0] <= mouse_x < end_x_position
            and self.position[1] <= mouse_y < self.position[1] + self.size[1]
        )

    @property
    def volume_fill_percent(self):
        """
        Returns the percent of the volume bar shown to the right of the speaker button. The value is between [0, 1].
        """
        curr_time = pygame.time.get_ticks()
        if self.__start_hover is None:
            assert self.__leave is not None
            time_after_mouse_left_ms = curr_time - self.__leave - BUTTON_LEAVE_DELAY_MS
            if time_after_mouse_left_ms < 0:
                return self.__max_expansion
            if time_after_mouse_left_ms < VOLUME_BUTTON_ANIMATION_TIME_MS:
                return (
                    VOLUME_BUTTON_ANIMATION_TIME_MS - time_after_mouse_left_ms
                ) / VOLUME_BUTTON_ANIMATION_TIME_MS
            return 0

        time_after_mouse_starts_hovering_ms = curr_time - self.__start_hover - BUTTON_HOVER_DELAY_MS
        if time_after_mouse_starts_hovering_ms < 0:
            self.__max_expansion = 0
            return 0
        if time_after_mouse_starts_hovering_ms < VOLUME_BUTTON_ANIMATION_TIME_MS:
            expansion_percent = (
                time_after_mouse_starts_hovering_ms / VOLUME_BUTTON_ANIMATION_TIME_MS
            )
            self.__max_expansion = max(self.__max_expansion, expansion_percent)
            return expansion_percent
        self.__max_expansion = 1
        return 1

    def draw(self):
        if self.fill_center and self.border_width > 0:
            pygame.draw.rect(self.screen, self.background_color, self.rect, 0, self.border_radius)
        pygame.draw.rect(
            self.screen, self.border_color, self.rect, self.border_width, self.border_radius
        )
        self.screen.blit(
            self.speaker_icon,
            [
                self.position[0] + self.size[0] / 2 - self.speaker_icon.get_width() / 2,
                self.position[1] + self.size[1] / 2 - self.speaker_icon.get_height() / 2,
            ],
        )
        volume_bar_rect = pygame.Rect(
            [
                self.position[0] + self.size[0] + VOLUME_BUTTON_BAR_OFFSET,
                self.position[1] + self.size[1] / 2 - self.expand_rect[1] / 2,
            ],
            [self.expand_rect[0] * self.volume_fill_percent, self.expand_rect[1]],
        )
        pygame.draw.rect(self.screen, "dark gray", volume_bar_rect)
        if self.volume_fill_percent < self.volume:
            return
        pygame.draw.circle(
            self.screen,
            "black",
            [
                self.position[0]
                + self.size[0]
                + self.expand_rect[0] * self.volume
                + VOLUME_BUTTON_BAR_OFFSET,
                self.position[1] + self.size[1] / 2,
            ],
            VOLUME_BUTTON_CIRCLE_RADIUS,
        )
