# Climate Cooker
This python project is run with a png (or ascii txt) as input of a world map (in equirectangular projection).
The script then will generate a number of output maps (of the same dimension) for mapping atmospheric pressure, prevailiing winds, precipitation and average surface temperature. Ultimately, a map is generated for climate zones (as a function of the other information).

Details of how to interpret these maps can be found in the sections to follow.
## Input Map
The program is initialized with an input file representing an equirectangular projection of your world's relief. The individual requirements are given in subsections below. In either case, the resulting map should be approximately 2x as wide as it is high, and the width should not be lower than 50px, nor higher than 400px.

### PNG input
The most obvious choice for input map is a color png image with either 3 or 4 channels (or 'planes'); Any 4th (alpha) channel is disregarded. The coloring of the pixels will be interpreted as height. The coloring is interpreted as follows (also given in [r,g,b]):

color | rgb | interpretation
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
1 | height 1 (sea level)
2 | height 2
3 | height 3
4 | height 4
5 | height 5
6 | height 6
7 8 9 | height 7
anything else | height 0 (water)
