from pyglet import clock
from random import randint

s = None


def start(scene):
    print "start"
    global s
    s = scene
    s.Title('You are the Hero', on_screen = True)
    s.Narration('All the villagers said', on_screen = True)
    s.Choice("I was eager", on_select = scene1, on_screen = True)
    s.Choice("I wasn't eager", on_select = scene1, on_screen = True)

def scene1():
    print "scene1"
    s.Narration('Sending me into the snow-storm')
    s.Narration('Without backup')
    s.Narration('Again')
    s.Narration('Alone')
    clock.schedule_interval(spawn_troll, 5)
    clock.schedule_once(scene2, 20)


def spawn_troll(dt):
    s.Troll()


def scene2(dt):
    print "scene2"
    s.Narration('Why me?')
    s.Narration('Alone')
    s.Narration('Why me?')
    s.Narration('Alone')
    s.Narration('This is not fair')
    clock.unschedule(spawn_troll)
    clock.schedule_interval(spawn_troll, 3)
    clock.schedule_once(scene3, 20)

def scene3(dt):
    print "scene3"
    clock.unschedule(spawn_troll)
    clock.schedule_interval(spawn_troll, 2)
    s.Choice("I had enough", on_select=pre_village)

def pre_village():
    s.Narration("This time")
    s.Narration("They will pay")
    s.Narration("They will pay")
    clock.schedule_once(village_scene, 20)

counter = 20
def decrement_counter():
    global counter
    counter -= 1
    if counter <= 0:
        ending()

def village_callback(dt):
    s.House()

def village_scene(dt):
    clock.unschedule(spawn_troll)
    s.Narration("This time")
    s.Narration("They will say")
    s.Title("You are the Villain")
    clock.schedule_interval(village_callback, 5)
    for i in range(counter + 4):
        s.Villager(on_death = decrement_counter)


def fade_out(dt):
    s.fade_out()

def ending():
    s.Title("But it was another village")
    s.Title("But it was another village")
    s.Narration("The end.")
    s.Narration("The end.")
    clock.schedule_once(fade_out, 10)
