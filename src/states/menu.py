#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.states.state import State, StateType


class MenuState(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, dt):
        self.game.goto_state(StateType.playing, self.game.get_level_name())
