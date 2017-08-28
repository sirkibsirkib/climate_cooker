from math import pi
import collections

class Climate:
    TROPICAL_RAINFOREST, TROPICAL_MONSOON, SAVANNAH, HOT_DESERT,\
    HOT_STEPPE, COLD_DESERT, COLD_STEPPE, MARITIME_EAST_COAST,\
    MARITIME_WEST_COAST, MEDITERRANEAN,TEMPERATE_MONSOON,\
    LAUTENTIAN, SUBARCTIC, MANCHURIAN, SUBARCTIC_EAST,\
    TUNDRA, ICECAP = range(17)

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

def climate_color_func(value):
    if value == Climate.TROPICAL_RAINFOREST:
        return [86, 155, 71]
    elif value == Climate.TROPICAL_MONSOON:
        return [255, 255, 255]
    elif value == Climate.SAVANNAH:
        return [186, 167, 37]
    elif value == Climate.HOT_DESERT:
        return [255, 249, 200]
    elif value == Climate.HOT_STEPPE:
        return [244, 229, 127]
    elif value == Climate.COLD_DESERT:
        return [138, 139, 159]
    elif value == Climate.COLD_STEPPE:
        return [210, 188, 220]
    elif value == Climate.MARITIME_EAST_COAST:
        return [255, 255, 255]
    elif value == Climate.MARITIME_WEST_COAST:
        return [255, 255, 255]
    elif value == Climate.MEDITERRANEAN:
        return [45, 186, 168]
    elif value == Climate.TEMPERATE_MONSOON:
        return [208, 248, 198]
    elif value == Climate.LAUTENTIAN:
        return [255, 255, 255]
    elif value == Climate.SUBARCTIC:
        return [87, 76, 255]
    elif value == Climate.MANCHURIAN:
        return [255, 255, 255]
    elif value == Climate.SUBARCTIC_EAST:
        return [110, 199, 210]
    elif value == Climate.TUNDRA:
        return [183, 190, 200]
    elif value == Climate.ICECAP:
        return [177, 247, 255]
    else:
        return [0, 0, 0]