#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame

from src.game import Game
from src.settings import Settings
from src.states.state import StateType


class Application:
    def __init__(self):
        pygame.init()
        self.terminated = False
        self.clock = pygame.time.Clock()

        self.settings = Settings()

        self.game = Game(self)

        video_flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        if self.settings.is_fullscreen():
            video_flags |= pygame.FULLSCREEN

        self.surface = pygame.display.set_mode(self.settings.get_window_size(),
                                               video_flags)
        self.screen = pygame.surface.Surface(self.surface.get_size())

        self.game.goto_state(StateType.loading)

        pygame.key.set_repeat(50, 30)

    def load(self, argv):
        return self.game.load(argv)

    def update(self, dt):
        return self.game.update(dt)

    def draw(self):
        return self.game.draw()

    def keypressed(self, key, is_repeat):
        return self.game.keypressed(key, is_repeat)

    def keyreleased(self, key):
        return self.game.keyreleased(key)

    def quit(self):
        return self.game.quit()

    def terminate(self):
        self.terminated = not self.quit()

    def run(self):
        keys = {}

        while not self.terminated:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    self.keypressed(event.key, event.key in keys)
                    keys[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.keyreleased(event.key)
                    keys.pop(event.key, None)

            dt = self.clock.tick(1000) / 1000

            self.update(dt)

            self.screen.fill((0, 0, 0))

            self.draw()

            self.surface.blit(self.screen, (0, 0))

            pygame.display.flip()

        pygame.quit()
        return 0
