import pyglet
import random
from player import Player
from random_pool import RandomPool

"""
    Scene:
        - if conditions met, add/remove event from pool
        - for each update, draw random event from pool, remove if necessary
        - draw events on screen

        - background -> bg
        - blockers -> bg,fg
        - npcs -> bg, fg
        - foreground -> fg
a       """
def check_collision(sprite1, sprite2):
    # x1 - w1 // 2 < x2 < x1 + w1 // 2
    # y1 - h1 // 2 < y2 < y1 + h1 // 2
    w1 = sprite1.width // 2
    h1 = sprite1.height // 2
    return (sprite1.x - w1 < sprite2.x < sprite1.x + w1 and
        sprite1.y  - h1 < sprite2.y < sprite1.y + h1)

class Scene(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer_width = 200
        self.random_pool = RandomPool()
        self.player = Player(x = width // 2, y = height // 2)
        self.batch = pyglet.graphics.Batch()
        pyglet.resource.path = ['.', 'data']
        pyglet.resource.reindex()
        simage = pyglet.resource.image("black-block.png")
        simage.anchor_x = simage.width // 2
        simage.anchor_y = simage.width // 2
        self._sprites = []
        self._scenery = []
        self._blockers = []
        self._bullets = []
        self._labels = []
        self._npcs = []
        self._collections = [self._sprites, self._scenery, self._blockers,
                self._bullets, self._labels, self._npcs]
        [self.add_sprite(
                pyglet.sprite.Sprite(simage, batch=self.batch, x=x, y=y))
                for x in range(0, 100, 10)
                for y in range(0, 100, 10)]
        print self._sprites

    def add_sprite(self, sprite):
        print sprite.x, sprite.y
        self._sprites.append(sprite)
        sprite.batch = self.batch
        try:
            if sprite.sprite_type == "bullet":
                self._bullets.append(sprite)
            elif sprite.sprite_type == "blocker":
                self._blockers.append(sprite)
            elif sprite.sprite_type == "npc":
                self._npcs.append(sprite)
            elif sprite.sprite_type == "text":
                self._labels.append
            else: # scenery
                self._scenery.append(sprite)
        except:
            self._scenery.append(sprite)

    def remove_sprite(self, sprite):
        for collection in self._collections:
            if sprite in collection:
                collection.remove(sprite)
        sprite.delete()

    def action(self, action):
        state, action = action.split()
        self.player.action(state, action)

    def draw(self):
        self.batch.draw()
        self.player.draw()

    def update(self, dt):
        self.player.update(dt)
        bw = self.buffer_width
        dx = self.player.vx * dt
        dy = self.player.vy * dt

        for sprite in self._sprites:
            sprite.x -= dx
            sprite.y -= dy

        for sprite in self._sprites:
            if (sprite.x < - bw or sprite.y < - bw or
                sprite.x > self.width + bw or sprite.y > self.height + bw):
                if sprite in self._scenery:
                    self.remove_sprite(sprite)
                else: # wrap
                    if sprite.x < -bw:
                        sprite.x += self.width + 2 * bw
                    if sprite.x > self.width + bw:
                        sprite.x -= self.width + 2 * bw
                    if sprite.y < -bw:
                        sprite.y += self.height + 2 * bw
                    if sprite.y > self.height + bw:
                        sprite.y -= self.height + 2 * bw


        for bullet in self._bullets:
            if collision(bullet, self.player):
                remove_sprite(bullet)
                remove_sprite(self.player)
            for npc in self._npcs:
                if collision(bullet, npc):
                    remove_sprite(npc)
                    remove_sprite(player)
        for npc in self._npcs:
            if collision(npc, player):
                remove_sprite(npc)
                remove_sprite(player)

    def random_event(self, dt):
        for obj in next(self.random_pool):
            (obj.x, obj.y) = self.random_offscreen_point()
            obj.batch = self.batch
            self.add_sprite(obj)

    def random_offscreen_point(self):
        bw = self.buffer_width
        side = random.randint(0,3)
        if side == 0: # north
            x = random.randint(0, self.width)
            y = random.randint(self.height, self.height + bw)
        elif side == 1: # east
            x = random.randint(-bw, 0)
            y = random.randint(0, self.height)
        elif side == 2: # south
            x = random.randint(0, self.width)
            y = random.randint(-bw, 0)
        else: # west
            x = random.randint(self.width, self.width + bw)
            y = random.randint(0, self.height)

        return x, y

    def resize(self, width, height):
        h = self.height
        w = self.width
        self.height = height
        self.width = width
        self.player.set_position(width // 2, height // 2)

        dy = (self.height - h) // 2
        dx = (self.width - w) // 2

        for sprite in self._scenery + self._npcs + self._bullets:
            sprite.x += dx
            sprite.y += dy

