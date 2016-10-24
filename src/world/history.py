#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Moment:
    def __init__(self, directions):
        self.directions = directions


class History:
    def __init__(self):
        self.data = []

    def push(self, moment):
        self.data.append(moment)

    def pop(self, remove=True):
        if not self.data:
            return None
        return self.data.pop() if remove else self.data[-1]

    def peek(self):
        return self.pop(False)
