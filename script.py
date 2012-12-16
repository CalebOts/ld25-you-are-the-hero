
def scene1():
    pool.add(1, False, (Text, [], {"text":"title", "size": 16})
    pool.add(1, False, (Text, [], {"text": "YES"})
    pool.add(1, False, (Text, [], {"text": "NO"})

def load_events():
    pool.add(0.56, False, (Troll, {"on_death":lambda: print "the troll is dead"}
    pool.add(0.56, False, (Text, {"on_select": scene1})

