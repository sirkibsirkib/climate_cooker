from climates import Climate

    ######################
    # FROM CELL TO COLOR #
    ######################

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



# returns abs() distance between two radii, the shortest way around the circle
def wrap_rad_abs(a, b):
    return min(
        abs(a-b),
        abs(a-b-2.0),
        abs(a-b+2.0),
    )

# rgb bumps occur at 0, 4/3pi and 2/3pi respectively
# when more than
def color_bump(rot_rads, bump_center):
    wra = wrap_rad_abs(rot_rads, bump_center)
    if wra <= .33333:
        return 1.0
    elif wra >= .66666:
        return 0.0
    else:
        return 1.0 - ((wra - .33333)*3.0)


def wind_color_func(rot_power):

    (rot, power) = rot_power
    assert power >= 0
    assert power <= 1
    col = [
        int(255.0 * color_bump(rot, 0.0) * power),
        int(255.0 * color_bump(rot, 1.33333) * power),
        int(255.0 * color_bump(rot, .66666) * power),
    ]
    return col


def climate_color_func(value):
    if value == Climate.TROPICAL_RAINFOREST:
        return [0, 200, 0]
    elif value == Climate.TROPICAL_MONSOON:
        return [0, 255, 255]
    elif value == Climate.SAVANNAH:
        return [255, 255, 0]
    elif value == Climate.HOT_DESERT:
        return [255, 255, 150]
    elif value == Climate.HOT_STEPPE:
        return [255, 150, 150]
    elif value == Climate.COLD_DESERT:
        return [100, 100, 200]
    elif value == Climate.COLD_STEPPE:
        return [50, 50, 100]
    elif value == Climate.MARITIME_EAST_COAST:
        return [255, 255, 0]
    elif value == Climate.MARITIME_WEST_COAST:
        return [100, 100, 0]
    elif value == Climate.MEDITERRANEAN:
        return [255, 0, 0]
    elif value == Climate.TEMPERATE_MONSOON:
        return [0, 170, 0]
    elif value == Climate.LAUTENTIAN:
        return [255, 100, 100]
    elif value == Climate.SUBARCTIC:
        return [87, 76, 255]
    elif value == Climate.MANCHURIAN:
        return [100, 255, 255]
    elif value == Climate.SUBARCTIC_EAST:
        return [150, 150, 255]
    elif value == Climate.TUNDRA:
        return [150, 150, 150]
    elif value == Climate.ICECAP:
        return [200, 200, 255]
    elif value == Climate.WATER:
        return [0, 0, 0]
    else:
        return [255, 0, 0]


    ######################
    # FROM COLOR TO CELL #
    ######################

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
