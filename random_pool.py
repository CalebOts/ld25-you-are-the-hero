import random
import pyglet
from player import Player

class RandomPool(object):
    def __init__(self):
        simage = pyglet.resource.image("black-block.png")
        self.pool = [(1, True, ((pyglet.sprite.Sprite, [simage], {}),),)]

    def __iter__(self):
        return self

    def __next__(self):
        objects = []
        probability, persistent, constructors = random.choice(self.pool)
        if probability > random.random():
            for init, args, kwargs in constructors:
                print init, args, kwargs
                objects.append(init(*args, **kwargs))
            if not persistent:
                self.pool.remove((probability, persistent, constructors))
            return objects
        return []

    next = __next__

