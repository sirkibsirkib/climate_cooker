from math import pi
import collections

def flatten(iterable):
    for el in iterable:
        if isinstance(el, collections.Iterable) and not isinstance(el, str):
            yield from flatten(el)
        else:
            yield el

def rel_color_func(x):
    if x == 0: return [0,0,0]
    elif x == 1: return [100,0,0]
    elif x == 2: return [0,100,0]
    elif x == 3: return [0,0,100]
    elif x == 4: return [150,150,0]
    elif x == 5: return [150,0,150]
    elif x == 6: return [0,150,150]
    elif x == 7: return [200,200,200]

def gray_scale_color_func(x):
    c = int(x)
    return [c, c, c]

def wrap_rad_abs(a, b):
    x = abs(a-b)
    return min(x, 2.0-x)

def wind_bump_helper(rot, bump_center):
    wra = wrap_rad_abs(rot, bump_center)
    if wra <= .33333:
        return 255
    elif wra >= .66666:
        return 0
    else:
        return int(255.0 - (wra - .33333)*3.0*255.0)

def wind_color_func(rot_power):
    (rot, power) = rot_power
    if rot < 0:
        rot += 2
    col = [wind_bump_helper(rot, 0.0) * power,
            wind_bump_helper(rot, 1.33333) * power,
            wind_bump_helper(rot, .66666) * power]
    return col

def coriolis_rotation(southness):
    if southness < .5:
        return -(.25 - abs(southness - .25)) * pi
    else:
        return (.25 - abs(southness - .75)) * pi