from helpful import rel_color_func, gray_scale_color_func, wind_color_func, climate_color_func
from mapping import relief_map, pressure_map, wind_map, rain_map, heat_map, climate_map, Map



input_png = 'input.png'

print('calculating relief...')
rel_map = relief_map(input_png)
rel_map.render('00_relief.png', rel_color_func)
print('relief done')

print('calculating pressure systems...')
pre_map_jul = pressure_map(rel_map, july=True)
pre_map_jul.render('01_jul_pressure.png', gray_scale_color_func)
pre_map_jan = pressure_map(rel_map, july=False)
pre_map_jan.render('02_jan_pressure.png', gray_scale_color_func)
print('pressure systems done')

print('calculating wind systems...')
win_map_jul = wind_map(pre_map_jul)
win_map_jul.render('03_jul_wind.png', wind_color_func)
win_map_jan = wind_map(pre_map_jan)
win_map_jan.render('04_jan_wind.png', wind_color_func)
print('wind systems done')

print('calculating rain systems...')
rai_map_jul = rain_map(rel_map, win_map_jul)
rai_map_jul.render('05_jul_rain.png', gray_scale_color_func)
rai_map_jan = rain_map(rel_map, win_map_jan)
rai_map_jan.render('06_jan_rain.png', gray_scale_color_func)
print('rain systems done')

print('calculating heat maps...')
hea_map_jul = heat_map(rel_map, win_map_jul, rai_map_jul, july=True)
hea_map_jul.render('07_jul_heat.png', gray_scale_color_func)
hea_map_jan = heat_map(rel_map, win_map_jan, rai_map_jan, july=False)
hea_map_jan.render('08_jan_heat.png', gray_scale_color_func)
print('heat maps done')

print('calculating climates...')
cli_map = climate_map(rel_map, rai_map_jul, rai_map_jan, hea_map_jul, hea_map_jan)
cli_map.render('09_climate.png', climate_color_func)
print('climates done')