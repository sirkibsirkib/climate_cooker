import png
from math import sqrt, ceil, atan2, pi
import helpful
import climates
from climates import Climate
import color_funcs


class Map:
    def __init__(self, cells):
        self.cells = cells
        self.width = len(self.cells[0])
        self.height = len(self.cells)

    def render(self, path, color_func):
        p = [helpful.flatten(map(color_func, row)) for row in self.cells]
        f = open(path, 'wb')
        w = png.Writer(self.width, self.height)
        w.write(f, p)
        f.close()

    def correct_coordinate(self, x, y):
        # wrap over poles
        check_again = True
        while check_again:
            check_again = False
            if y < 0:
                y *= -1
                x += int(self.width/2)
                check_again = True
            if y >= self.height:
                y = self.height - y
                x -= int(self.width/2)
                check_again = True

        # wrap around edges
        while x < 0:
            x += self.width
        while x >= self.width:
            x -= self.width
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
        min_value = min(helpful.flatten(self.cells))
        max_value = max(helpful.flatten(self.cells))
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

def txt_to_map(path):
    map_width = 0
    cells = []
    warning = False
    # populate 2d cells matrix with numbers from file
    # non-integers represent 0 (ocean)
    for row in open(path):
        row_cells = []
        for symbol in row:
            if symbol == '\n': continue
            try:
                cell = int(symbol)
                if cell > 7:
                    cell = 7
                    warning = True
            except:
                cell = 0
            row_cells.append(cell)
        cells.append(row_cells)
        map_width = max(map_width, len(row_cells))
    if warning:
        print('WARNING:\tmountains higher than 7 will be considered as height 7')

    # extend short lines with ocean cells
    for row in cells:
        while(len(row) < map_width): row.append(0)
    return Map(cells)

###############################################################



def relief_map(path):
    reader = png.Reader(path)
    print('path', path)
    png_data = reader.read()
    cells = []
    planes = png_data[3]['planes']
    N = planes
    if planes != 3 and planes != 4:
        print('wtf give me pngs with 3 or 4 planes please')
        quit()
    for y in png_data[2]:
        l = list(y)
        row = [color_funcs.rgb_to_height(l[n:n + 3]) for n in range(0, len(l), N)]
        cells.append(row)
    return Map(cells)


# summer means northern hemisphere is warmer
def pressure_map(rel_map, july=True):
    season_offset = int(rel_map.height / 16)
    if july:
        season_offset *= -1
    low_nodes = []
    high_nodes = []
    max_v_walk = int(rel_map.height / 7)

    interior_x_nodes = int(rel_map.width/5)
    interior_y_nodes = int(rel_map.height/5)
    # put in interior pressure zones
    x_gap = ceil(rel_map.width / interior_x_nodes / 2)
    y_gap = ceil(rel_map.height / interior_y_nodes / 2)
    for j in range(interior_y_nodes):
        if j/interior_y_nodes < .1 or j/interior_y_nodes > .9:
            continue
        for i in range(interior_x_nodes):
            int_x = int(rel_map.width * i / interior_x_nodes)
            int_y = int(rel_map.height * j / interior_y_nodes)
            if rel_map.get(int_x, int_y) > 0 and \
                            rel_map.get(int_x+x_gap, int_y) > 0 and \
                            rel_map.get(int_x-x_gap, int_y) > 0 and \
                            rel_map.get(int_x, int_y+y_gap) > 0 and \
                            rel_map.get(int_x, int_y-y_gap) > 0:
                if (j/interior_y_nodes < .5 and july) or (j/interior_y_nodes > .5 and not july):
                    low_nodes.append((int_x, int_y))
                else:
                    high_nodes.append((int_x, int_y))


    # put in pressure bands
    band_x_nodes = int(rel_map.width/2)
    for i in [1,2,3,4,5]:
        relevant_list = low_nodes if i%2==1 else high_nodes
        x_increment = 2
        x_pos = 1
        # offsets the start position vertically by a small amount
        flip_up = True
        y_axis = int(rel_map.height * i / 6 ) + season_offset
        while x_pos < rel_map.width:
            y_walk = int(max_v_walk/6) if flip_up else -int(max_v_walk/6)
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
    pre_map.render('output/pressure_nodes_'+('july.png' if july else 'january.png'), color_funcs.rel_color_func)

    def pressure_at(x, y):
        press = 0.0
        for (lx,ly) in low_nodes:
            x_dist = min(abs(lx - x), rel_map.width - abs(lx - x))
            dist = (x_dist ** 2 + (ly - y) ** 2)
            press -= 3 / (dist + max_v_walk*2)
        for (hx,hy) in high_nodes:
            x_dist = min(abs(hx - x), rel_map.width - abs(hx - x))
            dist = (x_dist ** 2 + (hy - y) ** 2)
            press += 3 / (dist + max_v_walk*2)
        return press

    pressure_cells = [
        [pressure_at(x, y) for x in range(rel_map.width)] for y in range(rel_map.height)
    ]
    pre_map = Map(pressure_cells)
    pre_map.normalize(0, 255, integers=False)
    return pre_map


def wind_map(pre_map):
    cells = []
    max_power = 0
    for y in range(pre_map.height):
        if y == 0:
            cells.append([(1.5, 0.0) for _ in range(pre_map.width)])
            continue
        if y == pre_map.height - 1:
            cells.append([(0.5, 0.0) for _ in range(pre_map.width)])
            continue

        row = []
        for x in range(pre_map.width):
            # get() automatically wraps correctly
            x_flow = pre_map.get(x+1, y) - pre_map.get(x-1, y)
            y_flow = pre_map.get(x, y+1) - pre_map.get(x, y-1)
            # print(x_flow, y_flow)
            rot = atan2(y_flow, x_flow) + helpful.coriolis_rotation(y / pre_map.height)
            rot = helpful.wrap_radians(rot)

            power = sqrt(x_flow*x_flow + y_flow*y_flow)
            if power > max_power:
                max_power = power
            row.append((rot, power))
        cells.append(row)

    cells = [
        [(rot, power/max_power) for (rot, power) in row] for row in cells
    ]
    return Map(cells)


cell_angles = [
        (0.00*pi, 1, 0),    # right
        (0.25*pi, 1, -1),   # up-right
        (0.50*pi, 0, -1),   # up
        (0.75*pi, -1, -1),  # up-left
        (1.00*pi, -1, 0),   # left
        (1.25*pi, -1, 1),   # down-left
        (1.50*pi, 1, 0),    # down
        (1.75*pi, 1, 1),    # down-right
    ]

def rain_map(rel_map, win_map):
    rain_ticks = 30

    def rain_tick(x, y):
        (rot, pow) = win_map.get(x, y)
        if rel_map.get(x, y) == 0:
            rai_map.increment(x, y, win_map.get(x, y)[1]**.4)

        blown_water = .8 * (pow**.2) * rai_map.get(x, y)
        spent_shares = 0
        clouds = []
        for (angle, go_x, go_y) in cell_angles:
            diff = min(
                abs(rot - angle),
                abs(rot - angle + pi * 2),
                abs(rot - angle - pi * 2)
            )
            if diff > pi / 1.1:
                continue
            share = 1 / (diff + 0.25)
            spent_shares += share
            clouds.append((share, go_x, go_y))

        for (share, go_x, go_y) in clouds:
            x2, y2 = rel_map.correct_coordinate(x + go_x, y + go_y)
            cloud_water = blown_water * share / spent_shares
            rai_map.increment(x, y, -cloud_water)
            rai_map.increment(x2, y2, cloud_water)
        rai_map.set(x, y, rai_map.get(x, y)/2.0)

    # all water starts with 1.0 rain, all land with 0.
    rai_map = Map.uniform_map_of_size(rel_map, 0.0)

    for _ in range(rain_ticks):
        for y in range(rel_map.height):
            for x in range(rel_map.width):
                rain_tick(x, y)

    rai_map.normalize(0, 255, integers=False)
    return rai_map

def heat_map(rel_map, win_map, rai_map, july=True):
    cells = []
    for y in range(rel_map.height):
        row = []
        for x in range(rel_map.width):
            heat_center = 0.4 if july else 0.6
            sun_heat = 1.0 / (0.3 + abs(heat_center - (y/rel_map.height))) - 1.3
            water_cooling = sum([
                rel_map.get(x, y) == 0,
                rel_map.get(x+1, y) == 0,
                rel_map.get(x, y+1) == 0,
                rel_map.get(x-1, y) == 0,
                rel_map.get(x, y-1) == 0,
            ])
            if water_cooling > 0: water_cooling += 1

            temp = (sun_heat - rel_map.get(x, y)/5) * 0.9**water_cooling
            row.append(temp)
        cells.append(row)
    hea_map = Map(cells)
    hea_map.normalize(0, 255, integers=True)
    return hea_map

def climate_map(rel_map, rai_jul, rai_jan, hea_jul, hea_jan):
    cells = []
    pop = dict()
    for e in Climate:
        pop[e] = 0

    for y in range(rel_map.height):
        row = []
        for x in range(rel_map.width):
            if rel_map.get(x, y) == 0:
                row.append(Climate.WATER)
                continue
            classification = climates.classify(hea_jul.get(x,y),
                                              hea_jan.get(x,y),
                                              rai_jul.get(x,y),
                                              rai_jan.get(x,y)) if y < rel_map.height / 2 else \
                climates.classify(hea_jan.get(x, y),
                                     hea_jul.get(x, y),
                                     rai_jan.get(x, y),
                                     rai_jul.get(x, y))
            pop[classification] += 1
            row.append(classification)
        cells.append(row)
    print('\nClimate counts:')
    for (a, b) in pop.items():
        print(' ', b, a.name)
    return Map(cells)

