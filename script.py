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
    s.Troll(on_death=pre_village)

def pre_village():
    s.Narration("This time")
    s.Narration("They will pay")
    s.Troll(on_death=village_scene)

def village_scene():
    s.Narration("This time")
    s.Narration("They will say")
    s.Title("You are the Villain")
    s.Villager()
    s.Villager()
    s.Villager()
    s.Villager()
    s.House()
    s.House()
    s.House()
    s.House()

def ending():
    s.Narration("And it wasn't even the same village")
    s.Narration("The end")
    s.Fadeout()

