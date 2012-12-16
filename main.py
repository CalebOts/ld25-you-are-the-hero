#!/usr/bin/env python2

import sys
sys.path = ['', 'pyglet-1.1.4'] + sys.path

import pyglet

window = pyglet.window.Window(width=800, height=600)

from pyglet.window import key

from scene import Scene
import script

scene = Scene(window.width, window.height)
script.start(scene)

keymap = {
        key.E : "up",
        key.S : "left",
        key.D : "down",
        key.F : "right",
        key.UP: "up",
        key.DOWN: "down",
        key.LEFT: "left",
        key.RIGHT: "right",
        key.SPACE : "blink",
}

pyglet.gl.glClearColor(255, 255, 255, 255)

fps_counter = pyglet.clock.ClockDisplay()

@window.event
def on_resize(width, height):
    scene.resize(width, height)

@window.event
def on_key_press(sym, mod):
    print "Key press  :", sym, mod
    if sym in keymap:
        scene.action("+ " + keymap[sym])

@window.event
def on_key_release(sym, mod):
    print "Key release:", sym, mod
    if sym in keymap:
        scene.action("- " + keymap[sym])

@window.event
def on_draw():
    window.clear()
    scene.draw()
    fps_counter.draw()

pyglet.clock.schedule_interval(scene.update, 1.0 / 200.0)
pyglet.clock.schedule_interval(scene.random_event, 1.0)

pyglet.app.run()
