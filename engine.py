import pyglet

class Engine(object):
    def __init__(self):
        pyglet.resource.path = ['.', 'data']
        pyglet.resource.reindex()
        self.player_image = pyglet.resource.image("player.png")
        self.player_blink = pyglet.resource.image("player-not-amused.png")
        self.player = pyglet.sprite.Sprite(self.player_image, x = 400, y = 400)
        self.player.vx = 0
        self.player.vy = 0
        self.player.pressed = {
                "up" : False,
                "down" : False,
                "left" : False,
                "right" : False
                }

    def action(self, action):
        state, obj, action = action.split()
        if obj == "player":
            if state == "+" and action in ("up", "down", "left", "right"):
                self.player.pressed[action] = True
            elif state == "-" and action in ("up", "down", "left", "right"):
                self.player.pressed[action] = False
            elif state == "+" and action == "blink":
                self.player.image = self.player_blink
            elif state == "-" and action == "blink":
                self.player.image = self.player_image

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
