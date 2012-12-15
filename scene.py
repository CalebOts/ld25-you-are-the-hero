import pyglet
from player import Player

"""
    Scene:
        - if conditions met, add/remove event from pool
        - for each update, draw random event from pool, remove if necessary
        - draw events on screen
        """
class Scene(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(x = width // 2, y = height // 2)

    def action(self, action):
        state, action = action.split()
        self.player.action(state, action)

        print self.player.pressed

    def draw(self):
        self.player.draw()

    def update(self, dt):
        self.player.update(dt)

    def resize(self, width, height):
        self.height = height
        self.width = width
        self.player.set_position(width // 2, height // 2)
