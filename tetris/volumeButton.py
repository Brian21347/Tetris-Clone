import pygame
from constants import *


class VolumeButton:
    def __init__(
        self, 
        screen: pygame.surface.Surface,
        position: Pii, 
        size: Pii,
        expand_rect: Pii,
        starting_volume: float,
        background_color: str,
        border_color: str,
        border_size: int,
        border_radius: int,
        fill_center: bool
    ) -> None:
        self.screen = screen
        self.position = position
        self.size = size
        self.expand_rect = expand_rect
        self.volume = starting_volume
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_size
        self.border_radius = border_radius
        self.fill_center = fill_center
        
        self.full_speaker = pygame.transform.scale(pygame.image.load(VOLUME_BUTTON_FULL), VOLUME_BUTTON_SPEAKER_SIZE)
        self.semi_speaker = pygame.transform.scale(pygame.image.load(VOLUME_BUTTON_SEMI), VOLUME_BUTTON_SPEAKER_SIZE)
        self.muted_speaker = pygame.transform.scale(pygame.image.load(VOLUME_BUTTON_MUTED), VOLUME_BUTTON_SPEAKER_SIZE)
        
        self.muted = False
        self.rect = pygame.rect.Rect(self.position, self.size)

        self.__start_hover = None
        self.__leave = 0
    
    @property
    def speaker_icon(self):
        if self.volume <= VOLUME_CLAMP or self.muted: return self.muted_speaker
        if self.volume < .5: return self.semi_speaker
        return self.full_speaker

    def update(self, event: pygame.event.EventType):
        x, y = pygame.mouse.get_pos()
        end_x_position = self.position[0] + self.size[0] + \
            (self.expand_rect[0] + VOLUME_BUTTON_CIRCLE_RADIUS if self.fill_percent != 0 else 0) + 10
        if self.position[0] < x - VOLUME_BUTTON_BAR_OFFSET < end_x_position \
            and self.position[1] < y < self.position[1] + self.size[1]:
            if self.__start_hover is None:
                self.__start_hover = pygame.time.get_ticks()
            self.__leave = None
        else:
            if self.__leave is None: 
                self.__leave = pygame.time.get_ticks()
            self.__start_hover = None
        if pygame.mouse.get_pressed()[0]:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
                self.muted = not self.muted
            if self.position[0] + self.size[0] < x - VOLUME_BUTTON_BAR_OFFSET < end_x_position \
                and self.position[1] < y < self.position[1] + self.size[1]:
                
                self.volume = (x - self.position[0] - self.size[0] - VOLUME_BUTTON_BAR_OFFSET) / self.expand_rect[0]
    
    def get_volume(self):
        return 0 if self.muted or self.volume < VOLUME_CLAMP else self.volume
    
    @property
    def fill_percent(self):
        curr_time = pygame.time.get_ticks()
        if self.__start_hover is None: 
            time_diff = curr_time - self.__leave
            if time_diff < VOLUME_BUTTON_DELAY:
                return (VOLUME_BUTTON_DELAY - time_diff) / VOLUME_BUTTON_DELAY
            return 0
        time_diff = curr_time - self.__start_hover - VOLUME_BUTTON_HOVER_DELAY
        if time_diff < VOLUME_BUTTON_DELAY:
            return time_diff / VOLUME_BUTTON_DELAY
        return 1 
    
    def draw(self):
        if self.fill_center and self.border_width > 0:
            pygame.draw.rect(self.screen, self.background_color, self.rect, 0, self.border_radius)
        pygame.draw.rect(self.screen, self.border_color, self.rect, self.border_width, self.border_radius)
        self.screen.blit(self.speaker_icon, [self.position[0] + self.size[0] / 2 - self.speaker_icon.get_width() / 2, self.position[1] + self.size[1] / 2 - self.speaker_icon.get_height() / 2])
        rect = pygame.Rect(
            [self.position[0] + self.size[0] + VOLUME_BUTTON_BAR_OFFSET, self.position[1] + self.size[1] / 2 - self.expand_rect[1] / 2], 
            [self.expand_rect[0] * self.fill_percent, self.expand_rect[1]]
        )
        pygame.draw.rect(self.screen, "dark gray", rect)
        if self.fill_percent < self.volume: return
        pygame.draw.circle(
            self.screen, 
            "black", 
            [
                self.position[0] + self.size[0] + self.expand_rect[0] * self.volume + VOLUME_BUTTON_BAR_OFFSET, 
                self.position[1] + self.size[1] / 2
            ], 
            VOLUME_BUTTON_CIRCLE_RADIUS
        )
