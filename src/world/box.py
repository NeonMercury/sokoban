#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.world.movable import Movable


class Box(Movable):
    def __init__(self, level, object):
        super().__init__()

        self.set_tile_size(level.tilewidth)

        self.object = object
        self.x = object.x // self.tilesize
        self.y = object.y // self.tilesize

    def update(self, dt):
        old_moving = self.moving
        super().update(dt)
        if old_moving and not self.moving:
            self.object.x = self.x * self.tilesize
            self.object.y = self.y * self.tilesize
