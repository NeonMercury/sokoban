#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame

from src.states.state import StateType

from src.states.loading import LoadingState
from src.states.menu import MenuState
from src.states.playing import PlayingState


class Game:
    def __init__(self, app):
        self.app = app

        self.levels = [
            '0-0', '0-1', '0-2', '0-3', '0-4',
            '0-5', '0-6',
        ]
        self.level_index = 0

        self.resources = {}

        state_arguments = {
            'game': self,
            'app': self.app,
            'resources': self.resources,
        }

        self.states = {
            StateType.loading: LoadingState(**state_arguments),
            StateType.menu: MenuState(**state_arguments),
            StateType.playing: PlayingState(**state_arguments),
        }

        self.state = None

    def get_level_name(self):
        return self.levels[self.level_index]

    def next_level(self):
        if self.level_index >= len(self.levels) - 1:
            return False

        self.level_index += 1
        return True

    def goto_state(self, state_type, *args, **kwargs):
        assert state_type in self.states
        if self.state is not None:
            self.state.exited_state()
        self.state = self.states[state_type]
        self.state.entered_state(*args, **kwargs)

    def load(self, argv):
        if self.state is not None:
            return self.state.load(argv)

    def update(self, dt):
        if self.state is not None:
            return self.state.update(dt)

    def draw(self):
        if self.state is not None:
            return self.state.draw()

    def keypressed(self, key, is_repeat):
        if key == pygame.K_ESCAPE:
            self.app.terminate()

        if self.state is not None:
            return self.state.keypressed(key, is_repeat)

    def keyreleased(self, key):
        if self.state is not None:
            return self.state.keyreleased(key)

    def quit(self):
        if self.state is not None:
            return self.state.quit()
