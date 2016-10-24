#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum


class CollisionType(Enum):
    empty = 0
    static = 1
    box = 2
    bomb = 3


class CollisionMap:
    def __init__(self, width, height, tilesize, collisions):
        self.width, self.height = width, height

        self.cols = [
            [
                CollisionType.empty
                for j in range(height)
            ] for i in range(width)
        ]

        for col in collisions:
            x_from = int(col[0] // tilesize)
            y_from = int(col[1] // tilesize)
            x_to = int(col[2] // tilesize + x_from)
            y_to = int(col[3] // tilesize + y_from)

            for i in range(x_from, x_to):
                for j in range(y_from, y_to):
                    self.cols[i][j] = CollisionType.static

    def get_collision_type(self, x, y):
        if 1 <= x < self.width and 1 <= y < self.height:
            return self.cols[x][y]
        return CollisionType.static

    def set_collision_type(self, x, y, type_):
        if 1 <= x < self.width and 1 <= y < self.height:
            self.cols[x][y] = type_
