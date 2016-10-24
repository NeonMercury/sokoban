#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import pygame
import pyganim
import pytmx

from src.states.state import State, StateType
from src.world.level import Level


class LoadingState(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load(self, argv):
        self.resources['animations'] = {}
        self.resources['images'] = {}
        self.resources['levels'] = {}
        self.resources['fonts'] = {}

        animations = self.resources['animations']
        images = self.resources['images']
        levels = self.resources['levels']
        fonts = self.resources['fonts']

        animations['player-mv-r'] = pyganim.getImagesFromSpriteSheet(
            'assets/sprites/sokoban/sprites.png',
            rects=[
                (320, 128, 42, 58),
                (320, 245, 42, 58),
            ])

        animations['player-mv-l'] = pyganim.getImagesFromSpriteSheet(
            'assets/sprites/sokoban/sprites.png',
            rects=[
                (320, 304, 42, 58),
                (320, 186, 42, 59),
            ])

        animations['player-mv-u'] = pyganim.getImagesFromSpriteSheet(
            'assets/sprites/sokoban/sprites.png',
            rects=[
                (362, 128, 37, 60),
                (362, 188, 37, 60),
            ])

        animations['player-mv-d'] = pyganim.getImagesFromSpriteSheet(
            'assets/sprites/sokoban/sprites.png',
            rects=[
                (320, 362, 37, 59),
                (357, 362, 37, 59),
            ])

        animations['player-idle'] = pyganim.getImagesFromSpriteSheet(
            'assets/sprites/sokoban/sprites.png',
            rects=[
                (362, 248, 37, 59),
            ])

        for root, dirs, files in os.walk('assets/levels'):
            for filename in files:
                if filename.lower().endswith('.tmx'):
                    level_name = filename[0:-4]
                    fullname = os.path.join(root, filename)
                    levels[level_name] = Level(fullname)

        fonts['main'] = pygame.font.Font('assets/fonts/pixel.ttf', 24)

    def update(self, dt):
        self.game.goto_state(StateType.menu)
