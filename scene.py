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
        self.background_batch = pyglet.graphics.Batch()
        self.foreground_batch = pyglet.graphics.Batch()
        pyglet.resource.path = ['.', 'data']
        pyglet.resource.reindex()
        simage = pyglet.resource.image("player.png")
        self.sprites = [
                pyglet.sprite.Sprite(simage,
                    batch = self.background_batch, x=x, y=y)
                for x in range(0, 100, 10)
                for y in range(0, 100, 10)
                ]

    def action(self, action):
        state, action = action.split()
        self.player.action(state, action)

    def draw(self):
        self.background_batch.draw()
        self.player.draw()

    def update(self, dt):
        self.player.update(dt)
        for sprite in self.sprites:
            sprite.x -= self.player.vx * dt
            sprite.y -= self.player.vy * dt

    def resize(self, width, height):
        h = self.height
        w = self.width
        self.height = height
        self.width = width
        self.player.set_position(width // 2, height // 2)

        dy = (self.height - h) // 2
        dx = (self.width - w) // 2

        for sprite in self.sprites:
            sprite.x += dx
            sprite.y += dy
