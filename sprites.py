import pyglet
from pyglet.sprite import Sprite

pyglet.resource.path = ['.', 'data']
pyglet.resource.reindex()

def do_nothing(): pass

class Player(Sprite):
    def __init__(self, x, y):
        self.sprite_type = "player"
        img_left = pyglet.resource.image("player.png")
        img_right = img_left.get_transform(flip_x=True)
        img_blink_left = pyglet.resource.image("player-not-amused.png")
        img_blink_right = img_blink_left.get_transform(flip_x=True)
        self.speed = 100
        self.vx = 0
        self.vy = 0
        self.last_vx = self.vx
        self.last_vy = self.vy
        self.imgs = {
                ("left", False) : img_left,
                ("right", False) : img_right,
                ("left", True) : img_blink_left,
                ("right", True) : img_blink_right
                }
        for img in self.imgs.values():
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2

        self.facing = "left"
        self.blinking = False
        pyglet.sprite.Sprite.__init__(self, img_left, x = x, y = y)
        self.pressed = {
                "up" : False,
                "down" : False,
                "left" : False,
                "right" : False,
                "blink" : False
                }

    def action(self, state, action):
        if state == "+" and action in self.pressed:
            self.pressed[action] = True
            if action in ("left", "right"): self.facing = action
            if action == "blink": self.blinking = True
        elif state == "-" and action in self.pressed:
            self.pressed[action] = False
            if action == "blink": self.blinking = False
        self.image = self.imgs[self.facing, self.blinking]

    def update(self, dt):
        speed = self.speed
        if self.pressed["up"] and not self.pressed["down"]:
            self.vy = + speed
            self.last_vy = self.vy
        elif self.pressed["down"] and not self.pressed["up"]:
            self.vy = - speed
            self.last_vy = self.vy
        else:
            if self.vx != 0: self.last_vy = 0
            self.vy = 0
        if self.pressed["left"] and not self.pressed["right"]:
            self.vx = - speed
            self.last_vx = self.vx
        elif self.pressed["right"] and not self.pressed["left"]:
            self.vx = + speed
            self.last_vx = self.vx
        else:
            if self.vy != 0: self.last_vx = 0
            self.vx = 0

class Troll(Sprite):
    def __init__(self, x, y, on_death = do_nothing):
        self.sprite_type = "npc"
        img = pyglet.resource.image("player.png")
        self.speed = 100
        self.vx = 0
        self.vy = 0
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        self.on_death = on_death

        pyglet.sprite.Sprite.__init__(self, img, x = x, y = y)

    def update(self, state, dt):
        (px, py) = state["player"]
        speed = self.speed
        dx = px - self.x
        dy = py - self.y
        if dx > self.speed: dx = self.speed
        if dx < -self.speed: dx = -self.speed
        if dy > self.speed: dy = self.speed
        if dy < -self.speed: dy = -self.speed
        self.x += dx * dt
        self.y += dy * dt


class HaplessVillager(object):
    def __init__(self):
        self.sprite_type = "npc"

class Bullet(Sprite):
    def __init__(self, x, y, vx, vy, on_death = do_nothing):
        self.sprite_type = "bullet"
        img = pyglet.resource.image("player.png")
        self.speed = 100
        self.vx = vx
        self.vy = vy
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        self.on_death = on_death

        pyglet.sprite.Sprite.__init__(self, img, x = x, y = y)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

class Text(object):
    def __init__(self):
        self.sprite_type = "text"
