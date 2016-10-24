#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
import pytmx
from pytmx.util_pygame import load_pygame

from src.world.bomb import Bomb
from src.world.box import Box
from src.world.collisionmap import CollisionMap, CollisionType


class Level:
    def __init__(self, filename):
        self.filename = filename
        self.reload_level()

    def reload_level(self):
        self.data = load_pygame(self.filename)

        assert self.data.tilewidth == self.data.tileheight

        self.bombs = {}
        self.boxes = {}
        self.targets = []

        self.bonuses = []

        self.tilesize = self.data.tilewidth

        self.spawn_point = (0, 0)

        self._process_level_info()
        self._initialize_collision_map()

        self.bonuses = self.bombs

        return self

    def has_box(self, x, y):
        return False if self.get_box(x, y) is None else True

    def get_box(self, x, y):
        for _, box in self.boxes.items():
            if box.x == x and box.y == y:
                return box
        return None

    def has_bomb(self, x, y):
        return False if self.get_bomb(x, y) is None else True

    def get_bomb(self, x, y):
        for _, bomb in self.bombs.items():
            if bomb.x == x and bomb.y == y:
                return bomb
        return None

    def has_bonus(self, x, y):
        return False if self.get_bonus(x, y) is None else True

    def get_bonus(self, x, y):
        for _, bonus in self.bonuses.items():
            if bonus.x == x and bonus.y == y:
                return bonus
        return None

    def remove_bonus(self, bonus):
        if bonus in self.bonuses:
            print('removed1')
            self.bonuses.remove(bonus)

        if bonus in self.bombs:
            print('removed2')
            self.bombs.remove(bonus)

    def get_collision_type(self, x, y):
        x, y = int(x), int(y)
        if self.has_box(x, y):
            return CollisionType.box
        return self.collision_map.get_collision_type(x, y)

    def update(self, dt):
        for _, box in self.boxes.items():
            box.update(dt)

    def draw(self, surface, offset_x=0, offset_y=0):
        for layer in self.data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    surface.blit(image, (offset_x + x * self.data.tilewidth,
                                         offset_y + y * self.data.tileheight))
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for object in layer:
                    if object.visible and object.image is not None:
                        x, y = object.x, object.y
                        if object in self.boxes:
                            x += self.boxes[object].offset_x
                            y += self.boxes[object].offset_y
                        surface.blit(object.image, (offset_x + x,
                                                    offset_y + y))
            elif isinstance(layer, pytmx.TiledImageLayer):
                pass

    def is_player_won(self):
        for target in self.targets:
            x = int(target.x / self.tilesize)
            y = int(target.y / self.tilesize)
            box = self.get_box(x, y)
            if box is None or target.name != box.object.name:
                return False

        return True

    def _process_level_info(self):
        for layer in self.data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                pass
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for object in layer:
                    if object.type == 'box':
                        self.boxes[object] = Box(self.data, object)
                    elif object.type == 'bomb':
                        self.bombs[object] = Bomb(self.data, object)
                    elif object.type == 'target':
                        self.targets.append(object)
                    elif object.type == 'player':
                        self.spawn_point = (object.x / self.tilesize,
                                            object.y / self.tilesize)
                        object.visible = False
            elif isinstance(layer, pytmx.TiledImageLayer):
                pass

    def _initialize_collision_map(self):
        collisions = []

        cols_layer = None

        for layer in self.data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == 'collisions':
                    cols_layer = layer
                    break

        if cols_layer is not None:
            collisions = [(o.x, o.y, o.width, o.height)
                          for o in cols_layer]

        self.collision_map = CollisionMap(self.data.width, self.data.height,
                                          self.data.tilewidth, collisions)
