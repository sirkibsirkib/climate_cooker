from enum import Enum

class Climate(Enum):
    TROPICAL_RAINFOREST, TROPICAL_MONSOON, SAVANNAH, HOT_DESERT,\
    HOT_STEPPE, COLD_DESERT, COLD_STEPPE, MARITIME_EAST_COAST,\
    MARITIME_WEST_COAST, MEDITERRANEAN,TEMPERATE_MONSOON,\
    LAUTENTIAN, SUBARCTIC, MANCHURIAN, SUBARCTIC_EAST,\
    TUNDRA, ICECAP, WATER, UNKNOWN = range(19)

class Cl(Enum):
    V_COLD, COLD, COOL, MILD, WARM, HOT, V_HOT = 18, 50, 90, 130, 180, 200, 230
    DRY, V_LOW, LOW, MODERATE, WET, V_WET = 4, 20, 40, 70, 120, 200

archetype_climates = [
        # enum                   s_temp    w_temp  s_rai   w_rai     strictness
        (Climate.TROPICAL_RAINFOREST, Cl.HOT, Cl.HOT, Cl.WET, Cl.WET, 0.360),
        (Climate.TROPICAL_MONSOON, Cl.HOT, Cl.MILD, Cl.WET, Cl.DRY, 0.4),
        (Climate.TEMPERATE_MONSOON, Cl.HOT, Cl.WARM, Cl.V_WET, Cl.DRY, 0.23),
        (Climate.SAVANNAH, Cl.HOT, Cl.WARM, Cl.WET, Cl.DRY, 0.4),
        (Climate.HOT_DESERT, Cl.V_HOT, Cl.WARM, Cl.DRY, Cl.DRY, 1.1),
        (Climate.HOT_STEPPE, Cl.HOT, Cl.WARM, Cl.DRY, Cl.DRY, 1.1),
        (Climate.COLD_DESERT, Cl.HOT, Cl.COLD, Cl.DRY, Cl.DRY, 1.0),
        (Climate.COLD_STEPPE, Cl.WARM, Cl.COLD, Cl.DRY, Cl.DRY, 1.0),
        (Climate.MARITIME_EAST_COAST, Cl.HOT, Cl.WARM, Cl.WET, Cl.MODERATE, 0.400),
        (Climate.MARITIME_WEST_COAST, Cl.WARM, Cl.COOL, Cl.WET, Cl.WET, 0.500),
        (Climate.MEDITERRANEAN, Cl.HOT, Cl.MILD, Cl.DRY, Cl.MODERATE, 0.8),
        (Climate.LAUTENTIAN, Cl.WARM, Cl.COLD, Cl.MODERATE, Cl.LOW, 0.5),
        (Climate.SUBARCTIC, Cl.MILD, Cl.V_COLD, Cl.MODERATE, Cl.V_LOW, 0.444),
        (Climate.MANCHURIAN, Cl.WARM, Cl.COLD, Cl.MODERATE, Cl.DRY, 0.5),
        (Climate.SUBARCTIC_EAST, Cl.MILD, Cl.V_COLD, Cl.LOW, Cl.DRY, 0.777),
        (Climate.TUNDRA, Cl.COLD, Cl.V_COLD, Cl.LOW, Cl.DRY, 0.777),
        (Climate.ICECAP, Cl.V_COLD, Cl.V_COLD, Cl.LOW, Cl.DRY, 0.5),
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