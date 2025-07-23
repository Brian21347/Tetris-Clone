import pygame
from collections.abc import Callable
from abc import ABC, abstractmethod
from constants import Action


class Screen(ABC):
    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()
        self._hidden = False
        self._groups: set["ScreenGroup"] = set()

    @abstractmethod
    def update(self, event: pygame.event.Event) -> None: ...

    @abstractmethod
    def draw(self) -> None: ...

    def send_action(self, action: Action):
        for group in self._groups.copy():
            group.receive_action(self, action)

    def hide(self):
        self._hidden = True

    def show(self):
        self._hidden = False

    def add_group(self, group: "ScreenGroup"):
        self._groups.add(group)

    def remove_group(self, group: "ScreenGroup"):
        if group in self._groups:
            self._groups.remove(group)


class ScreenGroup:
    def __init__(
        self,
        screens: set[Screen],
        screen_controller: Callable[["ScreenGroup", Screen, Action], None],
    ) -> None:
        self.screens = screens
        self.screen_controller = screen_controller
        for screen in self.screens:
            screen.add_group(self)

    def update(self, event: pygame.event.Event) -> None:
        for screen in self.screens:
            screen.update(event)

    def receive_action(self, screen: Screen, action: Action) -> None:
        self.screen_controller(self, screen, action)

    def draw(self) -> None:
        for screen in self.screens:
            screen.draw()

    def add(self, screen: Screen) -> bool:
        if screen in self.screens:
            return False
        self.screens.add(screen)
        screen.add_group(self)
        return True

    def remove(self, screen: Screen) -> bool:
        if screen not in self.screens:
            return False
        self.screens.remove(screen)
        screen.remove_group(self)
        return True
