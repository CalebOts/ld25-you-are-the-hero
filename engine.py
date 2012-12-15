import pyglet
from player import Player

class Engine(object):
    def __init__(self):
        self.player = Player()

    def action(self, action):
        state, obj, action = action.split()
        if obj == "player":
            self.player.action(state, action)

        print self.player.pressed

    def draw(self):
        self.player.draw()

    def update(self, dt):
        speed = 100
        if self.player.pressed["up"] and not self.player.pressed["down"]:
            self.player.y += speed * dt
        elif self.player.pressed["down"] and not self.player.pressed["up"]:
            self.player.y -= speed * dt
        elif self.player.pressed["left"] and not self.player.pressed["right"]:
            self.player.x -= speed * dt
        elif self.player.pressed["right"] and not self.player.pressed["left"]:
            self.player.x += speed * dt
        self.player.x %= 800
        self.player.y %= 600
