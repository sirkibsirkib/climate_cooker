import collections

def flatten(iterable):
    for el in iterable:
        if isinstance(el, collections.Iterable) and not isinstance(el, str):
            yield from flatten(el)
        else:
            yield el

def wrap_radians(x):
    while x < 0: x += 2
    while x > 2: x -= 2
    return x

def coriolis_rotation(southness):
    if southness < .5:
        return 2*-(.25 - abs(southness - .25))
    else:
        return 2*(.25 - abs(southness - .75))