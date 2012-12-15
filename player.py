import pyglet
from pyglet.sprite import Sprite

pyglet.resource.path = ['.', 'data']
pyglet.resource.reindex()


class Player(Sprite):
    def __init__(self, x, y):
        img_left = pyglet.resource.image("player.png")
        img_right = img_left.get_transform(flip_x=True)
        img_blink_left = pyglet.resource.image("player-not-amused.png")
        img_blink_right = img_blink_left.get_transform(flip_x=True)
        self.speed = 100
        self.vx = 0
        self.vy = 0
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
        speed = 100
        if self.pressed["up"] and not self.pressed["down"]:
            self.y += speed * dt
        elif self.pressed["down"] and not self.pressed["up"]:
            self.y -= speed * dt
        elif self.pressed["left"] and not self.pressed["right"]:
            self.x -= speed * dt
        elif self.pressed["right"] and not self.pressed["left"]:
            self.x += speed * dt
