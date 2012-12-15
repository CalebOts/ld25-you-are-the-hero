#!/usr/bin/env python2

if __name__ == "__main__":
    import sys
    sys.path = ['', 'pyglet-1.1.4'] + sys.path

    import pyglet

    print "pyglet version:", pyglet.version

    w = pyglet.window.Window()
    pyglet.app.run()
