import png
from math import sqrt, ceil, atan2, pi
from helpful import flatten, rel_color_func, gray_scale_color_func,\
    wind_color_func, coriolis_rotation, Climate, climate_color_func


class Map:
    def __init__(self, cells):
        self.cells = cells
        self.width = len(self.cells[0])
        self.height = len(self.cells)

    def render(self, path, color_func):
        p = [flatten(map(color_func, row)) for row in self.cells]
        f = open(path, 'wb')
        w = png.Writer(self.width, self.height)
        w.write(f, p)
        f.close()

    def correct_coordinate(self, x, y):
        while x < 0: x += self.width
        while x >= self.width: x -= self.width
        while y < 0: y += self.height
        while y >= self.height: y -= self.height
        return x, y

    def set(self, x, y, value):
        x, y = self.correct_coordinate(x, y)
        self.cells[y][x] = value

    def increment(self, x, y, value):
        x, y = self.correct_coordinate(x, y)
        self.cells[y][x] += value

    def get(self, x, y):
        x, y = self.correct_coordinate(x, y)
        return self.cells[y][x]

    def normalize(self, lower_bound, upper_bound, integers=True):
        min_value = min(flatten(self.cells))
        max_value = max(flatten(self.cells))
        d_before = max_value - min_value
        d_after = upper_bound - lower_bound
        def normalize_aux(raw):
            x = ((raw - min_value) * d_after / d_before) + lower_bound
            return (int(x) if integers else x)
        self.cells = [[normalize_aux(j) for j in i] for i in self.cells]

    @staticmethod
    def uniform_map(width, height, filling):
        return Map([[filling for _ in range(width)] for _ in range(height)])

    @staticmethod
    def uniform_map_of_size(other_map, filling):
        return Map.uniform_map(other_map.width, other_map.height, filling)


def relief_map(path):
    map_width = 0
    cells = []
    # populate 2d cells matrix with numbers from file
    # non-integers represent 0 (ocean)
    for row in open(path):
        row_cells = []
        for letter in row:
            if letter == '\n': continue
            try:
                cell = int(letter)
            except:
                cell = 0
            row_cells.append(cell)
        cells.append(row_cells)
        map_width = max(map_width, len(row_cells))

    # extend short lines with ocean cells
    for row in cells:
        while(len(row) < map_width): row.append(0)
    return Map(cells)


# summer means northern hemisphere is warmer
def pressure_map(rel_map, july=True):
    season_offset = int(rel_map.height / 16)
    if july:
        season_offset *= -1
    low_nodes = []
    high_nodes = []
    max_v_walk = int(rel_map.height / 7)


    # put in interior pressure zones
    x_gap = ceil(rel_map.width / 23)
    y_gap = ceil(rel_map.height / 19)
    for j in range(19):
        if j/19 < .1 or (j/19 > .45 and j/19 < .55) or j/19 > .9:
            continue
        for i in range(23):
            int_x = int(rel_map.width * i / 23)
            int_y = int(rel_map.height * j / 19)
            if rel_map.get(int_x, int_y) > 0 and \
                            rel_map.get(int_x+x_gap, int_y) > 0 and \
                            rel_map.get(int_x-x_gap, int_y) > 0 and \
                            rel_map.get(int_x, int_y+y_gap) > 0 and \
                            rel_map.get(int_x, int_y-y_gap) > 0:
                if (j/19 < .5 and july) or (j/19 > .5 and not july):
                    low_nodes.append((int_x, int_y))
                else:
                    high_nodes.append((int_x, int_y))


    # put in pressure bands
    for i in [1,2,3,4,5]:
        relevant_list = low_nodes if i%2==1 else high_nodes
        x_increment = ceil(rel_map.width / 47)
        x_pos = 1
        # offsets the start position vertically by a small amount
        flip_up = True
        y_axis = int(rel_map.height * i / 6 ) + season_offset
        while x_pos < rel_map.width:
            y_walk = int(max_v_walk/2) if flip_up else -int(max_v_walk/2)
            flip_up = not flip_up
            for w in range(max_v_walk):
                if rel_map.get(x_pos, y_axis + y_walk) > 0:
                    y_walk += -1 if july else 1
                    if y_axis + y_walk == 0 or y_axis + y_walk == rel_map.height - 1:
                        break
                else:
                    break

            relevant_list.append((x_pos, y_axis+y_walk))
            x_pos += x_increment

    pre_map = Map.uniform_map_of_size(rel_map, 0)
    for (x,y) in low_nodes:
        pre_map.set(x, y, 1)
    for (x,y) in high_nodes:
        pre_map.set(x, y, 2)
    pre_map.render('pressure_nodes.png', rel_color_func)

    def pressure_at(x, y):
        press = 0.0
        for (lx,ly) in low_nodes:
            dist = (min(abs(lx-x), rel_map.width-abs(lx-x))**2 + (ly-y)**2)
            # if dist > max_v_walk*3: continue
            press -= 1/(dist+max_v_walk)
        for (hx,hy) in high_nodes:
            dist = (min(abs(hx-x), rel_map.width-abs(hx-x))**2 + (hy-y)**2)
            # if dist > max_v_walk*3: continue
            press += 9.0/(dist+max_v_walk)
        if press > 0:
            return press**.3
        else:
            return -((-press)**.3)

    pressure_cells = [
        [pressure_at(x, y) for x in range(rel_map.width)] for y in range(rel_map.height)
    ]
    print(pressure_cells)
    pre_map = Map(pressure_cells)
    pre_map.normalize(0, 255, integers=True)
    return pre_map


def wind_map(pre_map):
    cells = []
    max_power = 0
    for y in range(pre_map.height):
        row = []
        for x in range(pre_map.width):
            x_flow = pre_map.get(x-1 if x-1 >= 0 else pre_map.width-1, y) - pre_map.get((x+1)%pre_map.width, y)
            y_flow = pre_map.get(x, y-1 if y-1 >= 0 else pre_map.height-1) - pre_map.get(x, (y+1)%pre_map.height)

            rot = 1.0 * atan2(y_flow, x_flow) + coriolis_rotation(y / pre_map.height)
            power = sqrt(x_flow**2.0 + y_flow**2.0)
            max_power = max(max_power, power)
            row.append((rot, power))
        cells.append(row)
    cells = [
        [(rot, power/max_power) for (rot, power) in row] for row in cells
    ]
    return Map(cells)


def rain_cloud(x, y, water, rel_map, win_map, rai_map, prev_height, depth_remaining):
    this_height = max(1, rel_map.get(x, y))
    (rot, pow) = win_map.get(x, y)
    deposit_fraction = max(0.0, 1-((1-(pow**.9))**(1+this_height-prev_height)))
    rai_map.increment(x, y, water*deposit_fraction)
    water *= (1-deposit_fraction)

    if depth_remaining == 0 or water < 0.03:
        rai_map.increment(x, y, water) # dump remainder
        return

    angle_sets = [
        (0.00*pi, 1, 0),    # right
        (0.25*pi, 1, -1),   # up-right
        (0.50*pi, 0, -1),   # up
        (0.75*pi, -1, -1),  # up-left
        (1.00*pi, -1, 0),   # left
        (1.25*pi, -1, 1),   # down-left
        (1.50*pi, 1, 0),    # down
        (1.75*pi, 1, 1),    # down-right
    ]

    spent_shares = 0
    recurse_clouds = []
    for (angle, go_x, go_y) in angle_sets:
        diff = min(
            abs(rot - angle),
            abs(rot - angle + pi*2),
            abs(rot - angle - pi*2)
        )
        if diff > pi/2.3:
            continue
        share = 1 / (diff + 0.1)
        spent_shares += share
        recurse_clouds.append((share, go_x, go_y))
    for (share, go_x, go_y) in recurse_clouds:
        x2, y2 = rel_map.correct_coordinate(x + go_x, y + go_y)
        rain_cloud(x2, y2, water*share/spent_shares, rel_map, win_map, rai_map, this_height, depth_remaining-1)


def rain_map(rel_map, win_map):
    rai_map = Map.uniform_map_of_size(rel_map, 0)
    for y in range(rel_map.height):
        for x in range(rel_map.width):
            if rel_map.get(x, y) != 0:
                # clouds start in the ocean
                continue
            rain_cloud(x, y, 1, rel_map, win_map, rai_map, 1, 10)

    rai_map.normalize(0, 255, integers=True)
    return rai_map

def heat_map(rel_map, win_map, rai_map, july=True):
    cells = []
    for y in range(rel_map.height):
        row = []
        for x in range(rel_map.width):
            heat_center = 0.4 if july else 0.6
            sun_heat = 1.0 / (0.25 + abs(heat_center - (y/rel_map.height))) - 1.3
            water_cooling = sum([
                rel_map.get(x, y) == 0,
                rel_map.get(x+1, y) == 0,
                rel_map.get(x, y+1) == 0,
                rel_map.get(x-1, y) == 0,
                rel_map.get(x, y-1) == 0,
            ])
            if water_cooling > 0: water_cooling += 1

            temp = (sun_heat - rel_map.get(x, y)/6) * 0.9**water_cooling
            row.append(temp)
        cells.append(row)
    hea_map = Map(cells)
    hea_map.normalize(0, 255, integers=True)
    return hea_map

def climate_map(rel_map, rai_jul, rai_jan, hea_jul, hea_jan):
    cells = []
    for y in range(rel_map.height):
        row = []
        for x in range(rel_map.width):
            if rel_map.get(x, y) == 0:
                row.append(Climate.WATER)
                continue
            classification = Climate.classify(hea_jul.get(x,y),
                                              hea_jan.get(x,y),
                                              rai_jul.get(x,y),
                                              rai_jan.get(x,y)) if y < rel_map.height / 2 else \
                    Climate.classify(hea_jan.get(x, y),
                                     hea_jul.get(x, y),
                                     rai_jan.get(x, y),
                                     rai_jul.get(x, y))
            row.append(classification)
        cells.append(row)
    return Map(cells)




# ======================================

rel_map = relief_map("map.txt")
rel_map.render('00_relief.png', rel_color_func)

pre_map_jul = pressure_map(rel_map, july=True)
pre_map_jul.render('01_jul_pressure.png', gray_scale_color_func)
pre_map_jan = pressure_map(rel_map, july=False)
pre_map_jan.render('02_jan_pressure.png', gray_scale_color_func)

win_map_jul = wind_map(pre_map_jul)
win_map_jul.render('03_jul_wind.png', wind_color_func)
win_map_jan = wind_map(pre_map_jan)
win_map_jan.render('04_jan_wind.png', wind_color_func)

rai_map_jul = rain_map(rel_map, win_map_jul)
rai_map_jul.render('05_jul_rain.png', gray_scale_color_func)
rai_map_jan = rain_map(rel_map, win_map_jan)
rai_map_jan.render('06_jan_rain.png', gray_scale_color_func)

hea_map_jul = heat_map(rel_map, win_map_jul, rai_map_jul, july=True)
hea_map_jul.render('07_jul_heat.png', gray_scale_color_func)
hea_map_jan = heat_map(rel_map, win_map_jan, rai_map_jan, july=False)
hea_map_jan.render('08_jan_heat.png', gray_scale_color_func)

cli_map = climate_map(rel_map, rai_map_jul, rai_map_jan, hea_map_jul, hea_map_jan)
cli_map.render('09_climate.png', climate_color_func)