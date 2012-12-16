import random
import pyglet
from text import Text
from player import Player

class RandomPool(object):
    def __init__(self, batch = None):
        self.batch = batch
        simage = pyglet.resource.image("black-block.png")
        # [probability, persistence, ((Class, [args], {kwargs}), ...)), ...]
        self.pool = [
                (1, True, ((pyglet.sprite.Sprite, [simage], {}),),),
                (1, False, ((Text, ["You are the hero!", 42], {}),),)]

    def __iter__(self):
        return self

    def __next__(self):
        objects = []
        probability, persistent, constructors = random.choice(self.pool)
        if probability > random.random():
            for init, args, kwargs in constructors:
                objects.append(init(*args, batch = self.batch, **kwargs))
            if not persistent:
                self.pool.remove((probability, persistent, constructors))
            return objects
        return []

    next = __next__

