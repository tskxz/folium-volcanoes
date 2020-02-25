"""
Webmap with Folium
The webmap can view how many is the height of the volcanoes
Have the choropleth and GeoJson of the world
Contains Layer, popups of volcanoes
"""

import folium
import pandas

# Read the file
data = pandas.read_csv("Volcanoes.txt")

# Make a list of Coordinates
lat = list(data['LAT'])
lon = list(data['LON'])

# Make a lists
elev = list(data['ELEV'])
type = list(data['TYPE'])
status = list(data['STATUS'])
location = list(data['LOCATION'])
name = list(data['NAME'])



# Function which fill the color with green if not danger and red if danger
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


# Create the base map
base_map = folium.Map(location=[39.731527, -100.220763], min_zoom=3, zoom_start=4)

# Make a group of volcanoes and population
fgV = folium.FeatureGroup(name="Volcanoes on USA")
fgP = folium.FeatureGroup(name="Population of the world")

# HTML on popup on the volcanoes
html = """
<h4> %s volcano </h4>
<p> Height: %s </p>
<p> Type: %s </p>
<p> Location: %s </p>
<p> Status: %s </p>
"""

# Make the volcanoes points
for lt, ln, el, nm, ty, st, loc in zip(lat, lon, elev, name, type, status, location):
    iframe = folium.IFrame(html=html % (nm, str(el), ty, loc, st), width=200, height=200)
    fgV.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe), fill=True, radius=10,
                                      fill_color=color_producer(el), color='black', fill_opacity=1))

# Make the feature group of population
fgP.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                             style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                             else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                             else 'red'}))

# Add the groups to map
base_map.add_child(fgV)
base_map.add_child(fgP)
base_map.add_child(folium.LayerControl(position='topleft'))

# Save the html file
base_map.save('world.html')
