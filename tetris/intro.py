import pygame
from constants import *
from util import add_pii, scale_pii
from screen import Screen
from textBox import TextBox
from tutorialPopup import TutorialPopup


class Intro(Screen):
    def __init__(self):
        super().__init__()
        self.title_font = pygame.font.SysFont(FONT, TITLE_SIZE)
        self.title_text = self.title_font.render(TITLE, True, TITLE_TEXT_COLOR)
        self.start_font = pygame.font.SysFont(FONT, TEXT_SIZE)
        self.start_text = self.start_font.render(START_PROMPT_TEXT, True, START_PROMPT_TEXT_COLOR)
        self.tutorial_box = TextBox(TUTORIAL_BUTTON_START, TUTORIAL_BUTTON_SIZE, TUTORIAL_TEXT, TUTORIAL_TEXT_COLOR)
        self.tutorial_popup: TutorialPopup | None = None
        self.__is_focused = True

    def update(self, event: pygame.event.Event):
        if not self.__is_focused:
            return
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                self.hide()
                self.send_action(Action.hide)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT and self.tutorial_box.rect.collidepoint(pygame.mouse.get_pos()):
                self.__is_focused = False
                self.tutorial_popup = TutorialPopup()

    def draw(self) -> None:
        self.screen.blit(
            self.title_text,
            add_pii(TITLE_CENTER_POSITION, scale_pii(self.title_text.get_size(), -1 / 2)),
        )

        self.screen.blit(
            self.start_text,
            add_pii(START_PROMPT_CENTER_POSITION, scale_pii(self.start_text.get_size(), -1 / 2)),
        )

        self.screen.blit(
            self.start_font.render(str(pygame.time.get_ticks() // 1000), True, START_PROMPT_TEXT_COLOR),
            (0, 0)
        )
        
        self.tutorial_box.draw()
        if self.tutorial_popup is not None:
            self.tutorial_popup.draw()
