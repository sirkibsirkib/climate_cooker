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

    def get(self, x, y):
        x, y = self.correct_coordinate(x, y)
        return self.cells[y][x]

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
    for i in [2,3,4,6,7,8]:
        y_pos = int(rel_map.height * i / 10)
        for j in range(12):
            x_pos = int(rel_map.width*j/12)
            if rel_map.get(x_pos, y_pos) > 0 and \
                            rel_map.get(x_pos, y_pos) > 0 and \
                            rel_map.get(x_pos, y_pos) > 0 and \
                            rel_map.get(x_pos, y_pos) > 0 and \
                            rel_map.get(x_pos, y_pos) > 0:
                if (i < 5 and july) or (i >= 5 and not july):
                    low_nodes.append((x_pos, y_pos))
                else:
                    high_nodes.append((x_pos, y_pos))


    # put in pressure bands
    for i in [1,2,3,4,5]:
        relevant_list = low_nodes if i%2==1 else high_nodes
        x_increment = ceil(rel_map.width / 14)
        x_pos = 1
        y_axis = int(rel_map.height * i / 6 ) + season_offset



        while x_pos < rel_map.width:


            y_walk = 0
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
        [
            pressure_at(x, y) for x in range(rel_map.width)
        ] for y in range(rel_map.height)
    ]
    min_press = min(flatten(pressure_cells))
    max_press = max(flatten(pressure_cells))
    def normalize(raw):
        return int((raw - min_press) / (max_press - min_press) * 255)
    normalized = [[normalize(j) for j in i] for i in pressure_cells]
    return Map(normalized)

def wind_map(pre_map):
    cells = []
    max_power = 0
    for y in range(pre_map.height):
        row = []
        for x in range(pre_map.width):
            x_flow = pre_map.get(x-1 if x-1 >= 0 else pre_map.width-1, y) - pre_map.get((x+1)%pre_map.width, y)
            y_flow = pre_map.get(x, y-1 if y-1 >= 0 else pre_map.height-1) - pre_map.get(x, (y+1)%pre_map.height)

            rot = atan2(y_flow, x_flow) + coriolis_rotation(y / pre_map.height)
            power = sqrt(x_flow**2 + y_flow**2)
            max_power = max(max_power, power)
            row.append((rot, power))
        cells.append(row)
    cells = [
        [(rot, power/max_power) for (rot, power) in row] for row in cells
    ]
    return Map(cells)

def rain_map(rel_map, win_map):
    rai_map = Map.uniform_map_of_size(rel_map, 0)
    for y in range(rel_map.height):
        for x in range(rel_map.width):
            water = 1.0
            # TODO warm currents more water
            prev_height = 0
            if rel_map.get(x, y) != 0:
                # clouds start in the ocean
                continue

            # simulate a rain cloud starting at position
            cx, cy = x,y
            for i in range(6):
                (rot, pow) = win_map.get(cx, cy)
                if rot < 0: rot += 2*pi

                x_blown, y_blown = 0, 0
                if rot > 5/8*pi and rot < 11/8*pi:
                    x_blown = -1
                elif rot < 3/8*pi or rot > 13/8*pi:
                    x_blown = 1

                if rot > 1/8*pi and rot < 7/8*pi:
                    y_blown = -1
                elif rot > 15/8*pi and rot < 15/8*pi:
                    y_blown = 1

                cx += x_blown
                cy += y_blown

                # wrap around globe, break at poles
                if cx < 0: cx += rel_map.width
                elif cx == rel_map.width: cx -= rel_map.width

                if cy < 0 or cy == rel_map.height:
                    break

                new_height = rel_map.get(cx, cy)

                # deposit some of stored water here as rain
                deposit_fraction = max(0.0, 1-((.8)**(1+new_height-prev_height)))
                prev_height = new_height
                rai_map.set(cx, cy, min(10, rai_map.get(cx, cy) + water*deposit_fraction))
                water -= water * deposit_fraction
                if water < 0.26:
                    break
                if rel_map.get(cx, cy) == 0:
                    water += 1

    max_press = max(flatten(rai_map.cells))

    def normalize(raw):
        return int(raw / max_press * 255)

    normalized = [[normalize(j) for j in i] for i in rai_map.cells]
    return Map(normalized)

def heat_map(rel_map, win_map, rai_map, july=True):
    cells = []
    for y in range(rel_map.height):
        row = []
        for x in range(rel_map.width):
            heat_center = 0.4 if july else 0.6
            sun_heat = 1.0 / (0.3 + abs(heat_center - (y/rel_map.height))) - 1.5
            water_cooling = sum([
                rel_map.get(x, y) == 0,
                rel_map.get(x+1, y) == 0,
                rel_map.get(x, y+1) == 0,
                rel_map.get(x-1, y) == 0,
                rel_map.get(x, y-1) == 0,
            ])
            if water_cooling > 0: water_cooling += 2

            temp = (sun_heat - rel_map.get(x, y)/6) * 0.9**water_cooling
            row.append(temp)
        cells.append(row)

    min_press = min(flatten(cells))
    max_press = max(flatten(cells))

    def normalize(raw):
        return int((raw - min_press) / (max_press - min_press) * 255)

    normalized = [[normalize(j) for j in i] for i in cells]
    return Map(normalized)



def climate_map(rel_map, rai_jul, rai_jan, hea_jul, hea_jan):
    cells = []
    for y in range(rel_map.height):
        row = []
        for x in range(rel_map.width):
            if rel_map.get(x, y) == 0:
                continue




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

hea_map_jul = heat_map(rel_map, win_map_jul, rai_map_jul)
hea_map_jul.render('07_jul_heat.png', gray_scale_color_func)
hea_map_jan = heat_map(rel_map, win_map_jan, rai_map_jan)
hea_map_jan.render('08_jan_heat.png', gray_scale_color_func)

cli_map = climate_map