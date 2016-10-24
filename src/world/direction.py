#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum


class Direction(Enum):
    up = 0
    right = 1
    down = 2
    left = 3

    @staticmethod
    def get_delta(direction):
        deltas = {
            Direction.up: (0, -1),
            Direction.right: (1, 0),
            Direction.down: (0, 1),
            Direction.left: (-1, 0),
        }

        assert direction in deltas
        return deltas[direction]

    @staticmethod
    def get_inverted(direction):
        inverted = {
            Direction.up: Direction.down,
            Direction.right: Direction.left,
            Direction.down: Direction.up,
            Direction.left: Direction.right,
        }

        assert direction in inverted
        return inverted[direction]
