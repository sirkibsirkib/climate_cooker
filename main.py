import png
from math import sqrt, ceil, atan2
from helpful import flatten, rel_color_func, gray_scale_color_func, wind_color_func, coriolis_rotation


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

    def set(self, x, y, value):
        self.cells[y][x] = value

    def get(self, x, y):
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
def pressure_map(rel_map, summer=True):
    season_offset = int(rel_map.height / 16)
    if summer:
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
                if (i < 5 and summer) or (i >= 5 and not summer):
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
                    y_walk += -1 if summer else 1
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
    print(pre_map.width, pre_map.height)

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

# ======================================

rel_map = relief_map("map.txt")
rel_map.render('00_relief.png', rel_color_func)

pre_map = pressure_map(rel_map, summer=True)
pre_map.render('01_pressure.png', gray_scale_color_func)

win_map = wind_map(pre_map)
win_map.render('02_wind.png', wind_color_func)
