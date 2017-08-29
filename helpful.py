from math import pi, atan2
import collections

class Climate:
    TROPICAL_RAINFOREST, TROPICAL_MONSOON, SAVANNAH, HOT_DESERT,\
    HOT_STEPPE, COLD_DESERT, COLD_STEPPE, MARITIME_EAST_COAST,\
    MARITIME_WEST_COAST, MEDITERRANEAN,TEMPERATE_MONSOON,\
    LAUTENTIAN, SUBARCTIC, MANCHURIAN, SUBARCTIC_EAST,\
    TUNDRA, ICECAP, WATER = range(18)

    @staticmethod
    def classify(s_temp, w_temp, s_prec, w_prec):
        pass
        #temp
        # 0     50      100     140     170     200     250
        #   v.cold  cold    mild    warm    hot     v.hot

        #prec
        # 0     10      20     40           70     170       250
        #   dry     v.low   low     moderate  wet       v.wet

        s_vhot = s_temp > 180
        w_vhot = w_temp > 180
        s_hot = s_temp > 170 and s_temp <= 255
        w_hot = w_temp > 170 and w_temp <= 255
        s_warm = s_temp > 100 and s_temp <= 200
        w_warm = w_temp > 100 and w_temp <= 200
        s_mild = s_temp > 60 and s_temp <= 180
        w_mild = w_temp > 60 and w_temp <= 180
        s_cold = s_temp > 20 and s_temp <= 100
        w_cold = w_temp > 20 and w_temp <= 100
        s_vcold = s_temp <= 55
        w_vcold = w_temp <= 55

        s_vwet = s_prec > 130
        w_vwet = w_prec > 130
        s_wet = s_prec > 50 and s_prec <= 220
        w_wet = w_prec > 50 and w_prec <= 220
        s_moderate = s_prec > 10 and s_prec <= 90
        w_moderate = w_prec > 10 and w_prec <= 90
        s_low = s_prec > 15 and s_prec <= 50
        w_low = w_prec > 15 and w_prec <= 50
        s_vlow = s_prec > 5 and s_prec <= 35
        w_vlow = w_prec > 5 and w_prec <= 35
        s_dry= s_prec <= 30
        w_dry = w_prec <= 30


        description = ''
        if s_vhot: description += ' ' + 's_vhot'
        if w_vhot: description += ' ' + 'w_vhot'
        if s_hot: description += ' ' + 's_hot'
        if w_hot: description += ' ' + 'w_hot'
        if s_warm: description += ' ' + 's_warm'
        if w_warm: description += ' ' + 'w_warm'
        if s_mild: description += ' ' + 's_mild'
        if w_mild: description += ' ' + 'w_mild'
        if s_cold: description += ' ' + 's_cold'
        if w_cold: description += ' ' + 'w_cold'
        if s_vcold: description += ' ' + 's_vcold'
        if w_vcold: description += ' ' + 'w_vcold'


        if s_vwet: description += ' ' + 's_vwet'
        if w_vwet: description += ' ' + 'w_vwet'
        if s_wet: description += ' ' + 's_wet'
        if w_wet: description += ' ' + 'w_wet'
        if s_moderate: description += ' ' + 's_moderate'
        if w_moderate: description += ' ' + 'w_moderate'
        if s_low: description += ' ' + 's_low'
        if w_low: description += ' ' + 'w_low'
        if s_vlow: description += ' ' + 's_vlow'
        if w_vlow: description += ' ' + 'w_vlow'
        if s_dry: description += ' ' + 's_dry'
        if w_dry: description += ' ' + 'w_dry'

        if s_hot and w_hot and s_wet and w_wet:
            return Climate.TROPICAL_RAINFOREST
        elif s_hot and w_warm and s_vwet and w_dry:
            return Climate.TROPICAL_MONSOON
        elif s_hot and w_warm and s_wet and w_dry:
            return Climate.SAVANNAH
        elif s_vhot and w_warm and s_dry and w_dry:
            return Climate.HOT_DESERT
        elif s_hot and w_warm and (s_low or s_dry) and (w_low or w_dry):
            return Climate.HOT_STEPPE
        elif s_hot and w_cold and s_dry and w_dry:
            return Climate.COLD_DESERT
        elif s_warm and w_cold and (s_low or s_dry) and (w_low or w_dry):
            return Climate.COLD_STEPPE
        elif s_hot and (w_warm or w_mild) and s_wet and w_moderate:
            return Climate.MARITIME_EAST_COAST
        elif (s_warm or s_mild) and (w_mild or w_cold) and s_wet and w_wet:
            return Climate.MARITIME_WEST_COAST
        elif s_hot and w_mild and s_dry and w_moderate:
            return Climate.MEDITERRANEAN
        elif (s_hot or s_warm) and (w_mild or w_cold) and s_wet and w_dry:
            return Climate.TEMPERATE_MONSOON
        elif (s_warm or s_mild) and w_cold and s_moderate and w_low:
            return Climate.LAUTENTIAN
        elif (s_mild or s_cold) and w_vcold and s_moderate and w_vlow:
            return Climate.SUBARCTIC
        elif (s_warm or s_mild) and w_cold and s_moderate and w_dry:
            return Climate.MANCHURIAN
        elif (s_mild or s_cold) and w_vcold and s_moderate and w_dry:
            return Climate.SUBARCTIC_EAST
        elif s_cold and (w_cold or w_vcold) and s_low and w_dry:
            return Climate.TUNDRA
        elif s_vcold and w_vcold and (s_low or s_dry) and w_dry:
            return Climate.ICECAP


        print('couldnt classify temps:', s_temp, '/', w_temp, '   rain:', s_prec, '/', w_prec, description)
        return -999


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
    elif value == Climate.WATER:
        return [0, 0, 0]
    else:
        return [255, 0, 0]