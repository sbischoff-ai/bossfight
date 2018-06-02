# -*- coding: utf-8 -*-
'''
Defines the controls for the player character.
'''

import pyglet
import cocos
from cocos.director import director
from pyglet.window import key

BASE_SPEED = 300

class ControllableNode(cocos.cocosnode.CocosNode):
    '''
    A *CocosNode* that can be controlled by the player.
    Controllable Nodes automatically react to Controller or Mouse & Keyboard input.
    If you use multiple inheritance, inherit from *ControllableNode* before any third party
    (and thus possibly non-cooperative) base classes. (This class **is** cooperative btw.)
    '''

    def __init__(self, position=(0, 0), joystick=None, mouse_and_keyboard=True, speed=BASE_SPEED):
        super().__init__()
        self.position = position
        self.joystick = joystick
        if joystick is None:
            try:
                self.joystick = pyglet.input.get_joysticks()[0]
            except IndexError:
                print('Controller not found.')
        if self.joystick is not None:
            self.joystick.push_handlers(self)
            try:
                self.joystick.open(window=director.window)
            except OSError:
                pass # Controller was already openend
        if mouse_and_keyboard:
            self.keyboard = key.KeyStateHandler()
            director.window.push_handlers(self.keyboard)
        else:
            self.keyboard = None
        self.speed = speed
        self.velocity = (0, 0)
        self.do(cocos.actions.Move())
        self.schedule(self._update_movement)

    def _update_movement(self, dt):
        velocity = cocos.euclid.Vector2(0, 0)
        if self.joystick is None or \
          self.joystick.x*self.joystick.x + self.joystick.y*self.joystick.y < 0.05 and \
          self.keyboard is not None:
            if self.keyboard[key.UP]:
                velocity += (0, 1)
            if self.keyboard[key.DOWN]:
                velocity -= (0, 1)
            if self.keyboard[key.RIGHT]:
                velocity += (1, 0)
            if self.keyboard[key.LEFT]:
                velocity -= (1, 0)
            velocity.normalize()
        else:
            velocity += (self.joystick.x, -self.joystick.y)
            velocity *= velocity.magnitude_squared()
            if velocity.magnitude_squared() > 1.0:
                # This can never be True on physical analog sticks,
                # but should still be checked, as the driver theoretically allows this.
                velocity.normalize()
        velocity *= self.speed
        self.velocity = velocity.xy