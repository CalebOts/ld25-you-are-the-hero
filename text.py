import pyglet

def do_nothing():
    pass

class Text(pyglet.text.Label):
    def __init__(self, text, size = 36, batch = None, on_select = do_nothing):
        self.sprite_type = "text"
        pyglet.text.Label.__init__(self,
                text,
                font_name='Times New Roman',
                font_size=size,
                x=200, y=200,
                anchor_x='center', anchor_y='center',
                batch = batch,
                color = (0, 0, 0, 255))
        self.on_select = on_select
        self.draw()
