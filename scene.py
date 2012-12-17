import pyglet
import random
from sprites import Player, Troll, Bullet, HaplessVillager
from random_pool import RandomPool

from text import Text, do_nothing


def collision(sprite1, sprite2):
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
        self.player = Player(x = width // 2, y = height // 2)
        self.bg_batch = pyglet.graphics.Batch()
        self.fg_batch = pyglet.graphics.Batch()
        self.random_pool = RandomPool(batch = self.bg_batch)
        pyglet.resource.path = ['.', 'data']
        pyglet.resource.reindex()
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
        sprite.batch = self.bg_batch
        try:
            if sprite.sprite_type == "bullet":
                self._bullets.append(sprite)
                sprite.batch = self.fg_batch
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
        try:
            sprite.delete()
        except AttributeError as e:
            print "Warning:", e

    def action(self, action):
        state, action = action.split()
        self.player.action(state, action)
        if state == "+" and action == "blink":
            self.Bullet()

    def draw(self):
        self.bg_batch.draw()
        self.player.draw()
        self.fg_batch.draw()
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
                if sprite in self._scenery or sprite in self._bullets:
                    self.remove_sprite(sprite)
                else: # wrap
                    if sprite.x < -bw:
                        sprite.x += self.width + 2 * bw
                        sprite.y += bw
                    if sprite.x > self.width + bw:
                        sprite.x -= self.width + 2 * bw
                        sprite.y -= bw
                    if sprite.y < -bw:
                        sprite.y += self.height + 2 * bw
                        sprite.x += bw
                    if sprite.y > self.height + bw:
                        sprite.y -= self.height + 2 * bw
                        sprite.x -= bw


        for bullet in self._bullets:
            bullet.update(dt)
            #if collision(bullet, self.player):
                #self.remove_sprite(bullet)
                #self.game_over()
            for npc in self._npcs:
                if collision(npc, bullet):
                    self.remove_sprite(npc)
                    self.remove_sprite(bullet)
                    npc.on_death()
        for npc in self._npcs:
            npc.update(self.get_state(), dt)
            if collision(npc, self.player):
                self.game_over()

        for text in self._labels:
            if collision(self.player, text):
                text.on_select()

    def get_state(self):
        return {"player": (self.player.x, self.player.y),
                "bullets": ((b.x, b.y) for b in self._bullets)}

    def random_event(self, dt):
        for obj in next(self.random_pool):
            (obj.x, obj.y) = self.random_offscreen_point()
            obj.batch = self.bg_batch
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
        for text in self._labels:
            text.color = (0, 0, 0, 128)
        self._scenery.extend(self._labels)
        self._labels = []

    def Title(self, text, on_screen = True):
        (x, y) = self.random_point(on_screen=on_screen)
        self.add_sprite(Text(text, 34, (0, 0, 0, 255),
                x=self.width * 0.5, y=self.height * 0.75,
                batch=self.bg_batch))


    def Narration(self, text, size=24, on_screen = False):
        (x, y) = self.random_point(on_screen=on_screen)
        self.add_sprite(Text(text, size, (0, 0, 0, 255),
                x=x, y=y, batch=self.bg_batch))

    def Choice(self, text, size=24, on_select = do_nothing, on_screen = False):
        (x, y) = self.random_point(on_screen=on_screen)
        t = Text(text, size, (0, 0, 255, 255),
                x = x, y = y,
                batch=self.bg_batch, on_select = None)
        def on_select_wrapper():
            t.color = (255, 0, 0, 255)
            self.fade_text()
            on_select()
        t.on_select = on_select_wrapper
        self.add_sprite(t)

    def Troll(self, on_death = do_nothing):
        (x, y) = self.random_point(on_screen=False)
        self.add_sprite(Troll(x, y, on_death = on_death))

    def Villager(self, on_death = do_nothing):
        (x, y) = self.random_point(on_screen=False)
        self.add_sprite(HaplessVillager(x, y, on_death = on_death))

    def House(self):
        (x, y) = self.random_point(on_screen=False)
        img = pyglet.resource.image("house.png")
        house = pyglet.sprite.Sprite(img, x=x, y=y)
        house.sprite_type = "scenery"
        self.add_sprite(house)

    def fade_out(self):
        pass

    def Bullet(self):
        x = self.player.x
        y = self.player.y
        vx = self.player.vx + self.player.last_vx * 0.5
        vy = self.player.vy + self.player.last_vy * 0.5
        self.add_sprite(Bullet(x, y, vx, vy))

    def game_over(self):
        self.Narration("And this is how it ends.", on_screen = True)
