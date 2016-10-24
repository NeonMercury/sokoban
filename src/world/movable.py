#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

from src.world.direction import Direction


class Movable:
    def __init__(self, speed=300):
        self.speed = speed

        self.tilesize = 0
        self.w, self.h = self.tilesize, self.tilesize

        self.x, self.y = 0, 0

        self.moving = False
        self.last_direction = None

        self.dx, self.dy = 0, 0
        self.offset_x, self.offset_y = 0, 0
        self.target_x, self.target_y = 0, 0

    def is_moving(self):
        return self.moving

    def get_last_direction(self):
        return self.last_direction

    def set_tile_size(self, size):
        self.tilesize = size
        self.w, self.h = self.tilesize, self.tilesize

    def move(self, direction):
        if not self.moving:
            self.moving = True
            self.dx, self.dy = Direction.get_delta(direction)
            self.target_x = self.x + self.dx
            self.target_y = self.y + self.dy
            self.offset_x, self.offset_y = 0, 0

            self.last_direction = direction
            return True

        return False

    def stop(self, finish_on_target=False):
        if self.moving:
            self.moving = False
            self.offset_x = 0
            self.offset_y = 0

            if finish_on_target:
                self.x, self.y = self.target_x, self.target_y

    def update(self, dt):
        if self.moving:
            self.offset_x += self.speed * self.dx * dt
            self.offset_y += self.speed * self.dy * dt

            target_x_px = self.target_x * self.tilesize
            target_y_px = self.target_y * self.tilesize

            current_x_px = self.x * self.tilesize + self.offset_x
            current_y_px = self.y * self.tilesize + self.offset_y

            dx = math.fabs(target_x_px - current_x_px)
            dy = math.fabs(target_y_px - current_y_px)

            EPS = self.tilesize * 0.05

            if dx < EPS and dy < EPS:
                self.stop(True)
