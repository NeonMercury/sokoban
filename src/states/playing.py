#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
import pytmx

from src.states.state import State, StateType
from src.statistics import Statistics

from src.world.bomb import Bomb
from src.world.collisionmap import CollisionType
from src.world.direction import Direction
from src.world.history import History, Moment
from src.world.player import Player


class PlayingState(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def entered_state(self, level='0-0'):
        assert level in self.resources['levels']

        self.stats = Statistics()
        self.level = self.resources['levels'][level].reload_level()
        self.player = Player(self.resources)

        self.player.set_tile_size(self.level.tilesize)
        self.player.x, self.player.y = self.level.spawn_point

        self.history = History()

    def keypressed(self, key, is_repeat):
        direction = None

        pressed = pygame.key.get_pressed()

        if pressed[self.app.settings.get_key('place-bomb')]:
            if key == self.app.settings.get_key('move-up'):
                direction = Direction.up
            elif key == self.app.settings.get_key('move-right'):
                direction = Direction.right
            elif key == self.app.settings.get_key('move-down'):
                direction = Direction.down
            elif key == self.app.settings.get_key('move-left'):
                direction = Direction.left

            if direction is not None:
                self._place_bomb(direction)
            return

        if key == self.app.settings.get_key('move-up'):
            direction = Direction.up
        elif key == self.app.settings.get_key('move-right'):
            direction = Direction.right
        elif key == self.app.settings.get_key('move-down'):
            direction = Direction.down
        elif key == self.app.settings.get_key('move-left'):
            direction = Direction.left
        elif key == self.app.settings.get_key('revert'):
            self._revert_game()
        elif key == self.app.settings.get_key('restart'):
            self._restart_level()
        elif key == self.app.settings.get_key('next-level') and not is_repeat:
            self._next_level()

        if direction is not None:
            stop = False
            if self.player.move(direction):
                target_x, target_y = self.player.target_x, self.player.target_y
                box_tx, box_ty = target_x, target_y

                box = self.level.get_box(target_x, target_y)
                if box is not None:
                    box.move(direction)
                    box_tx, box_ty = box.target_x, box.target_y

                box_col = self.level.get_collision_type(box_tx, box_ty)
                player_col = self.level.get_collision_type(target_x, target_y)

                if box_col != CollisionType.empty:
                    stop = True
                elif (
                        player_col != CollisionType.empty and
                        player_col != CollisionType.box
                     ):
                    stop = True

                if stop:
                    self.player.stop()
                    if box is not None:
                        box.stop()
                else:
                    self.stats.moves += 1
                    moment_data = {self.player: direction}
                    if box is not None:
                        moment_data[box] = direction
                    self.history.push(Moment(moment_data))

    def keyreleased(self, key):
        pass

    def update(self, dt):
        self.player.update(dt)
        self.level.update(dt)

        bonus = self.level.get_bonus(self.player.x, self.player.y)
        if bonus is not None:
            self._activate_bonus(bonus)

        if self.level.is_player_won():
            self._next_level()

    def draw(self):
        sw, sh = self.app.screen.get_size()
        x, y = self.player.get_center_position()

        x = -x + sw // 2 - self.player.w
        y = -y + sh // 2 - self.player.h

        self.level.draw(self.app.screen, x, y)
        self.player.draw(self.app.screen)

        self._print(10, 10, 'Moves: {0}'.format(self.stats.moves), 'main')
        self._print(10, 40, 'Undos: {0}'.format(self.stats.undos), 'main')

    def _print(self, x, y, text, font, color=(255, 255, 255)):
        assert font in self.resources['fonts']
        output = self.resources['fonts'][font].render(text, False, color)
        self.app.screen.blit(output, (x, y))

    def _next_level(self):
        if not self.game.next_level():
            self.app.terminate()
        else:
            level_name = self.game.get_level_name()
            self.game.goto_state(StateType.playing, level_name)

    def _restart_level(self):
        level_name = self.game.get_level_name()
        self.game.goto_state(StateType.playing, level_name)

    def _activate_bonus(self, bonus):
        bonus.object.visible = False
        if isinstance(bonus, Bomb):
            self.stats.bombs += 1

        self.level.remove_bonus(bonus)

    def _place_bomb(self, direction):
        if self.stats.bombs <= 0:
            return

        dx, dy = Direction.get_delta(direction)
        tx, ty = self.player.x + dx, self.player.y + dy

        col = self.level.get_collision_type(tx, ty)
        if col is not CollisionType.empty:
            return

        self.level.set_collision_type(tx, ty, CollisionType.bomb)

        self.stats.bombs -= 1

    def _revert_game(self):
        if self.stats.undos <= 0:
            return

        moment = self.history.peek()
        if moment is not None:
            directions = moment.directions
            for obj, direction in directions.items():
                if obj.is_moving():
                    return False

            for obj, direction in directions.items():
                inverted = Direction.get_inverted(direction)
                obj.move(inverted)

            self.stats.moves -= 1
            self.stats.undos -= 1

            self.history.pop()
