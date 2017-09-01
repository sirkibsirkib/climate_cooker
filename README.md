# Climate Cooker
This python project is run with a png (or ascii txt) as input of a world map (in equirectangular projection).
The script then will generate a number of output maps (of the same dimension) for mapping atmospheric pressure, prevailiing winds, precipitation and average surface temperature.  For many of these maps, two versions are generated: one for "January" (summer in southern hemisphere) and "July" (summer in northern hemisphere). Ultimately, a map is generated for climate zones (as a function of the other information).

Details of how to interpret these maps can be found in the sections to follow.

The system's function is primary designed to approximate the instruction of [Geoff's Climate Cookbook](https://img.fireden.net/tg/image/1448/87/1448879578649.pdf).

## Input Map
The program is initialized with an input file representing an equirectangular projection of your world's relief. The individual requirements are given in subsections below. In either case, the resulting map should be approximately 2x as wide as it is high, and the width should not be lower than 50px, nor higher than 400px.

### PNG input
The most obvious choice for input map is a color png image with either 3 or 4 channels (or 'planes'); Any 4th (alpha) channel is disregarded. The coloring of the pixels will be interpreted as height. The coloring is interpreted as follows (also given in [r,g,b]):

color | rgb | interpretation
-------|------|------------------
black | [0,0,0] | water
white | [255,255,255] | height 1 (sea level)
red | [255,0,0] | height 2
green | [0,255,0] | height 3
blue | [0,0,255] | height 4
cyan | [0,255,255] | height 5
purple | [255,0,255] | height 6
yellow | [255,255,0] | height 7

### TXT input
The input map can be given as a txt file, with each line being interpreted as a horizontal row of cells, and each other character being interpreted as a cell. As with the png, the file provides height information. The table below details how to represent your map heights:

symbol(s) | interpretation
---------|----------
1 | height 1 (sea level)
2 | height 2
3 | height 3
4 | height 4
5 | height 5
6 | height 6
7 8 9 | height 7
anything else | height 0 (water)

## Interpreting Output Maps
### Relief Map
Identical format to input png image. This map is always generated, but it is especially useful to confirm that your input map was interpreted as expected.

### Pressure System Map
This map is rendered in grayscale. White and black represent highest and lowest barometric pressure respectively.

![Image of Relief Sample](https://github.com/sirkibsirkib/climate_cooker/blob/master/image_samples/01_pressure.png)

### Wind System Map
This map's pixels each encode two different values: direction and speed.
The rotation is mapped to hue, with all possible angles on the possible complete 2-radian circle being mapped to the color wheel (open some image manipulation program such as MS Paint or The GIMP for an interactive color wheel) angle 0 in red [255,0,0] maps to right/east, with the wheel rotating anticlockwise (the same orientation as is generally used in mathematics).

![Image of Wind Sample](https://github.com/sirkibsirkib/climate_cooker/blob/master/image_samples/03_wind.png)

The intensity of the color encodes the wind speed. The brightest color encodes maximum speed, and a black pixel has a speed of zero.

### Precipitation Map
Grayscale represents maximum and minimum values with white and black respectively.

![Image of Rain Sample](https://github.com/sirkibsirkib/climate_cooker/blob/master/image_samples/05_rain.png)


### Heat Map
White and black map to maximum and minimum heat respectively.

![Image of Heat Sample](https://github.com/sirkibsirkib/climate_cooker/blob/master/image_samples/07_heat.png)


### Climate Map
//TODO
