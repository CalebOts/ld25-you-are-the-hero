#!/usr/bin/env python2

import sys
sys.path = ['', 'pyglet-1.1.4'] + sys.path

import pyglet

window = pyglet.window.Window(width=800, height=600)

from pyglet.window import key

from engine import Engine

engine = Engine()

keymap = {
        key.E : "player up",
        key.S : "player left",
        key.D : "player down",
        key.F : "player right",
        key.SPACE : "player blink"
}

pyglet.gl.glClearColor(255, 255, 255, 255)

fps_counter = pyglet.clock.ClockDisplay()

@window.event
def on_key_press(sym, mod):
    print "Key press  :", sym, mod
    if sym in keymap:
        engine.action("+ " + keymap[sym])

@window.event
def on_key_release(sym, mod):
    print "Key release:", sym, mod
    if sym in keymap:
        engine.action("- " + keymap[sym])

@window.event
def on_draw():
    window.clear()
    engine.draw()
    fps_counter.draw()

pyglet.clock.schedule_interval(engine.update, 1.0 / 200.0)

pyglet.app.run()
