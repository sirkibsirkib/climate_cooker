from math import pi, atan2
import collections
from enum import Enum
import png


class Climate(Enum):
    TROPICAL_RAINFOREST, TROPICAL_MONSOON, SAVANNAH, HOT_DESERT,\
    HOT_STEPPE, COLD_DESERT, COLD_STEPPE, MARITIME_EAST_COAST,\
    MARITIME_WEST_COAST, MEDITERRANEAN,TEMPERATE_MONSOON,\
    LAUTENTIAN, SUBARCTIC, MANCHURIAN, SUBARCTIC_EAST,\
    TUNDRA, ICECAP, WATER, UNKNOWN = range(19)







class Cl(Enum):
    V_COLD, COLD, COOL, MILD, WARM, HOT, V_HOT = 10, 50, 70, 100, 120, 170, 230
    DRY, V_LOW, LOW, MODERATE, WET, V_WET = 0, 10, 25, 45, 90, 200

archetype_climates = [
        # enum                   s_temp    w_temp  s_rai   w_rai     strictness
        (Climate.TROPICAL_RAINFOREST, Cl.HOT, Cl.HOT, Cl.WET, Cl.WET, 0.360),
        (Climate.TROPICAL_MONSOON, Cl.HOT, Cl.MILD, Cl.WET, Cl.DRY, 0.444),
        (Climate.TEMPERATE_MONSOON, Cl.HOT, Cl.WARM, Cl.V_WET, Cl.DRY, 0.244),
        (Climate.SAVANNAH, Cl.HOT, Cl.WARM, Cl.WET, Cl.DRY, 0.355),
        (Climate.HOT_DESERT, Cl.V_HOT, Cl.WARM, Cl.DRY, Cl.DRY, 1.1),
        (Climate.HOT_STEPPE, Cl.HOT, Cl.WARM, Cl.DRY, Cl.DRY, 0.888),
        (Climate.COLD_DESERT, Cl.HOT, Cl.COLD, Cl.DRY, Cl.DRY, 1.0),
        (Climate.COLD_STEPPE, Cl.WARM, Cl.COLD, Cl.DRY, Cl.DRY, 0.555),
        (Climate.MARITIME_EAST_COAST, Cl.HOT, Cl.WARM, Cl.WET, Cl.MODERATE, 0.400),
        (Climate.MARITIME_WEST_COAST, Cl.WARM, Cl.COOL, Cl.WET, Cl.WET, 0.500),
        (Climate.MEDITERRANEAN, Cl.HOT, Cl.MILD, Cl.DRY, Cl.MODERATE, 0.777),
        (Climate.LAUTENTIAN, Cl.WARM, Cl.COLD, Cl.MODERATE, Cl.LOW, 0.555),
        (Climate.SUBARCTIC, Cl.MILD, Cl.V_COLD, Cl.MODERATE, Cl.V_LOW, 0.444),
        (Climate.MANCHURIAN, Cl.WARM, Cl.COLD, Cl.MODERATE, Cl.DRY, 0.488),
        (Climate.SUBARCTIC_EAST, Cl.MILD, Cl.V_COLD, Cl.LOW, Cl.DRY, 0.444),
        (Climate.TUNDRA, Cl.COLD, Cl.V_COLD, Cl.LOW, Cl.DRY, 0.777),
        (Climate.ICECAP, Cl.V_COLD, Cl.V_COLD, Cl.LOW, Cl.DRY, 0.555),
    ]


def classify(s_temp, w_temp, s_prec, w_prec):
    best = Climate.UNKNOWN
    best_distance = 9999
    for (climate, s_hea, w_hea, s_rai, w_rai, multiplier) in archetype_climates:
        distance = abs(s_temp - s_hea.value) + abs(w_temp - w_hea.value)\
                   + abs(s_prec - s_rai.value) + abs(w_prec - w_rai.value)
        distance *= multiplier
        if distance < best_distance:
            best = climate
            best_distance = distance
    return best

def flatten(iterable):
    for el in iterable:
        if isinstance(el, collections.Iterable) and not isinstance(el, str):
            yield from flatten(el)
        else:
            yield el


def rel_color_func(x):
    if x == 0: return [0,0,0]
    elif x == 1: return [255,255,255]
    elif x == 2: return [255,0,0]
    elif x == 3: return [0,255,0]
    elif x == 4: return [0,0,255]
    elif x == 5: return [0,255,255]
    elif x == 6: return [255,0,255]
    elif x == 7: return [255,255,0]

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
        return [86, 255, 71]
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
        return [243, 98, 180]
    elif value == Climate.MARITIME_WEST_COAST:
        return [180, 98, 180]
    elif value == Climate.MEDITERRANEAN:
        return [45, 186, 168]
    elif value == Climate.TEMPERATE_MONSOON:
        return [208, 248, 198]
    elif value == Climate.LAUTENTIAN:
        return [255, 100, 100]
    elif value == Climate.SUBARCTIC:
        return [87, 76, 255]
    elif value == Climate.MANCHURIAN:
        return [255, 174, 0]
    elif value == Climate.SUBARCTIC_EAST:
        return [110, 199, 210]
    elif value == Climate.TUNDRA:
        return [183, 190, 200]
    elif value == Climate.ICECAP:
        return [177, 247, 255]
    elif value == Climate.WATER:
        return [0, 0, 0]
    else:
        return [255, 0, 0]

def rgb_to_height(x):
    if x == [0,0,0]: return 0
    elif x == [255,255,255]: return 1
    elif x == [255,0,0]: return 2
    elif x == [0,255,0]: return 3
    elif x == [0,0,255]: return 4
    elif x == [0,255,255]: return 5
    elif x == [255,0,255]: return 6
    elif x == [255,255,0]: return 7
    print(x, 'just isn\'t known as a mapping to a height')
    quit(1)
