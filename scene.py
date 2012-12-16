import pyglet
import random
from player import Player
from random_pool import RandomPool

from text import Text, do_nothing

"""
Scene:
    - if conditions met, add/remove event from pool
    - for each update, draw random event from pool, remove if necessary
    - draw events on screen

    - background -> bg
    - blockers -> bg,fg
    - npcs -> bg, fg
    - foreground -> fg
"""

def collision(sprite1, sprite2):
    # x1 - w1 // 2 < x2 < x1 + w1 // 2
    # y1 - h1 // 2 < y2 < y1 + h1 // 2
    w1 = sprite1.width // 2
    h1 = sprite1.height // 2
    return (sprite1.x - w1 < sprite2.x < sprite1.x + w1 and
        sprite1.y  - h1 < sprite2.y < sprite1.y + h1)

def printfoo():
    print "foo"

class Scene(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer_width = 200
        self.player = Player(x = width // 2, y = height // 2)
        self.batch = pyglet.graphics.Batch()
        self.random_pool = RandomPool(batch = self.batch)
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

    def add_sprite(self, sprite):
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
                self._labels.append(sprite)
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
                    remove_sprite(self.player)
        for npc in self._npcs:
            if collision(npc, self.player):
                remove_sprite(npc)
                remove_sprite(self.player)

        for text in self._labels:
            if collision(self.player, text):
                text.on_select()



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

    def random_onscreen_point(self):
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        return x, y

    def random_point(self, on_screen = True):
        if on_screen:
            return self.random_onscreen_point()
        else:
            return self.random_offscreen_point()

    def resize(self, width, height):
        h = self.height
        w = self.width
        self.height = height
        self.width = width
        self.player.set_position(width // 2, height // 2)

        dy = (self.height - h) // 2
        dx = (self.width - w) // 2

        for sprite in self._sprites:
            sprite.x += dx
            sprite.y += dy

    def fade_text(self):
        self._scenery.extend(self._labels)
        self._labels = []

    def Title(self, text, on_screen = True):
        (x, y) = self.random_point(on_screen=on_screen)
        self.add_sprite(Text(text, 34, (0, 0, 0, 255),
                x=self.width * 0.5, y=self.height * 0.75,
                batch=self.batch))


    def Narration(self, text, size=24, on_screen = False):
        (x, y) = self.random_point(on_screen=on_screen)
        self.add_sprite(Text(text, size, (0, 0, 0, 255),
                x=x, y=y, batch=self.batch))

    def Choice(self, text, size=24, on_select = do_nothing, on_screen = False):
        (x, y) = self.random_point(on_screen=on_screen)
        t = Text(text, size, (0, 0, 255, 255),
                x = x, y = y,
                batch=self.batch, on_select = None)
        def on_select_wrapper():
            t.color = (255, 0, 0, 255)
            self.fade_text()
            on_select()
        t.on_select = on_select_wrapper
        self.add_sprite(t)

    def Troll(self, on_death): pass
    def Villager(self): pass
    def House(self): pass
    def FadeOut(self): pass
