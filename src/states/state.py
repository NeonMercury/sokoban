#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum


class StateType(Enum):
    loading = 0
    menu = 1
    playing = 2


class State:
    def __init__(self, app, game, resources):
        self.app = app
        self.game = game
        self.resources = resources

    def load(self, argv):
        pass

    def update(self, dt):
        pass

    def draw(self):
        pass

    def keypressed(self, key, is_repeat):
        pass

    def keyreleased(self, key):
        pass

    def quit(self):
        pass

    def entered_state(self):
        pass

    def exited_state(self):
        pass
