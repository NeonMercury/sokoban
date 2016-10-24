#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
import pyganim

from src.world.movable import Movable


class Player(Movable):
    def __init__(self, resources):
        super().__init__()

        self._initialize_animations(resources)

    def update(self, dt):
        old_moving = self.moving
        super().update(dt)
        if not self.moving and old_moving:
            self.animation.pause()
        elif self.moving:
            if self.dx == 1:
                self.set_animation('move-right')
            elif self.dx == -1:
                self.set_animation('move-left')
            elif self.dy == 1:
                self.set_animation('move-down')
            elif self.dy == -1:
                self.set_animation('move-up')
            self.animation.play()

    def get_center_position(self):
        x = self.x * self.tilesize + self.offset_x - self.w // 2
        y = self.y * self.tilesize + self.offset_y - self.h // 2
        return x, y

    def draw(self, surface):
        sw, sh = surface.get_size()

        x = (sw - self.w) // 2 + 11
        y = (sh - self.h) // 2 + 4

        if self.animation is not None:
            self.animation.blit(surface, (x, y))
        else:
            pygame.draw.rect(surface, (144, 72, 255), (x, y, self.w, self.h))

    def set_animation(self, name):
        assert name in self.animations
        self.animation = self.animations[name]

    def _initialize_animations(self, resources):
        anim_right = resources['animations']['player-mv-r']
        move_right_frames = list(zip(anim_right, [100 for i in anim_right]))

        anim_left = resources['animations']['player-mv-l']
        move_left_frames = list(zip(anim_left, [100 for i in anim_left]))

        anim_up = resources['animations']['player-mv-u']
        move_up_frames = list(zip(anim_up, [100 for i in anim_up]))

        anim_down = resources['animations']['player-mv-d']
        move_down_frames = list(zip(anim_down, [100 for i in anim_down]))

        anim_idle = resources['animations']['player-idle']
        move_idle_frames = list(zip(anim_idle, [100 for i in anim_idle]))

        self.animations = {
            'move-right': pyganim.PygAnimation(move_right_frames),
            'move-left': pyganim.PygAnimation(move_left_frames),
            'move-up': pyganim.PygAnimation(move_up_frames),
            'move-down': pyganim.PygAnimation(move_down_frames),
            'idle': pyganim.PygAnimation(move_idle_frames),
        }

        self.set_animation('idle')
        self.animation.play()
