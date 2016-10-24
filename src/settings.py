#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame


class Settings:
    def __init__(self):
        self.data = {
            'window': {
                'width': 800,
                'height': 600,
                'fullscreen': False,
            },
            'keys': {
                'move-up': pygame.K_UP,
                'move-right': pygame.K_RIGHT,
                'move-down': pygame.K_DOWN,
                'move-left': pygame.K_LEFT,
                'place-bomb': pygame.K_SPACE,
                'restart': pygame.K_r,

                'revert': pygame.K_BACKSPACE,
                'next-level': pygame.K_n,
            },
        }

    def get_window_size(self):
        return self.data['window']['width'], self.data['window']['height']

    def is_fullscreen(self):
        return self.data['window']['fullscreen']

    def get_key(self, name):
        assert name in self.data['keys']
        return self.data['keys'][name]
