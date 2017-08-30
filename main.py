# from helpful import rel_color_func, gray_scale_color_func, wind_color_func, climate_color_func
# from mapping import relief_map, pressure_map, wind_map, rain_map, heat_map, climate_map, Map

import mapping
import color_funcs

def check_validity(rel_map):
    woh = rel_map.width / rel_map.height
    if abs(woh - 2.0) > .4:
        print('Map proportions are wonky! Aim for 2x as wide as high!')
        quit()
    if rel_map.width < 50:
        print('Map must be at least 50 pixels wide!')
        quit()
    if rel_map.width > 400:
        print('Map must be no more least 400 pixels wide!')
        quit()

input_png = 'earth.png'

print('calculating relief...')
rel_map = mapping.relief_map(input_png)
rel_map.render('output/00_relief.png', color_funcs.rel_color_func)
print('relief done')

check_validity(rel_map)

print('calculating pressure systems...')
pre_map_jul = mapping.pressure_map(rel_map, july=True)
pre_map_jul.render('output/01_jul_pressure.png', color_funcs.gray_scale_color_func)
pre_map_jan = mapping.pressure_map(rel_map, july=False)
pre_map_jan.render('output/02_jan_pressure.png', color_funcs.gray_scale_color_func)
print('pressure systems done')

print('calculating wind systems...')
win_map_jul = mapping.wind_map(pre_map_jul)
win_map_jul.render('output/03_jul_wind.png', color_funcs.wind_color_func)
win_map_jan = mapping.wind_map(pre_map_jan)
win_map_jan.render('output/04_jan_wind.png', color_funcs.wind_color_func)
print('wind systems done')

print('calculating rain systems...')
rai_map_jul = mapping.rain_map(rel_map, win_map_jul)
rai_map_jul.render('output/05_jul_rain.png', color_funcs.gray_scale_color_func)
rai_map_jan = mapping.rain_map(rel_map, win_map_jan)
rai_map_jan.render('output/06_jan_rain.png', color_funcs.gray_scale_color_func)
print('rain systems done')

print('calculating heat maps...')
hea_map_jul = mapping.heat_map(rel_map, win_map_jul, rai_map_jul, july=True)
hea_map_jul.render('output/07_jul_heat.png', color_funcs.gray_scale_color_func)
hea_map_jan = mapping.heat_map(rel_map, win_map_jan, rai_map_jan, july=False)
hea_map_jan.render('output/08_jan_heat.png', color_funcs.gray_scale_color_func)
print('heat maps done')

print('calculating climates...')
cli_map = mapping.climate_map(rel_map, rai_map_jul, rai_map_jan, hea_map_jul, hea_map_jan)
cli_map.render('output/09_climate.png', color_funcs.climate_color_func)
print('climates done')